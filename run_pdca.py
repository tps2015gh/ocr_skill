"""
PDCA Loop Runner for Complex Thai OCR
======================================

Simple executable script that runs the PDCA improvement cycle
with Manager, Programmer, and QA agents.

Usage:
    # Start new task
    python run_pdca.py --input input_pdf/document.pdf --target-quality 0.95
    
    # Resume existing task
    python run_pdca.py --resume
    
    # Run specific agent
    python run_pdca.py --agent manager --input document.pdf
    python run_pdca.py --agent programmer --resume
    python run_pdca.py --agent qa --resume
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class PDCAState:
    """Manages PDCA state file"""
    
    def __init__(self, state_file: str = "pdca_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load()
    
    def _load(self) -> Optional[Dict]:
        """Load state from file"""
        if not self.state_file.exists():
            return None
        
        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self):
        """Save state to file"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def create(self, task_id: str, input_file: str, target_quality: float = 0.95):
        """Create new state"""
        self.state = {
            "task_id": task_id,
            "input_file": input_file,
            "document_type": "thai_legal",
            "current_phase": "plan",
            "iteration": 1,
            "target_quality": target_quality,
            "current_quality": 0.0,
            "complexity_flags": {
                "has_tables": False,
                "has_english": False,
                "has_thai_numerals": False,
                "has_legal_terms": False
            },
            "open_bugs": [],
            "fixes_applied": [],
            "logs": [],
            "output_files": {
                "ocr": f"output_txt/{Path(input_file).stem}.txt",
                "reviewed": "pdca_reviewed.txt"
            }
        }
        self.save()
    
    def log(self, agent: str, action: str, phase: str = None):
        """Add log entry"""
        self.state["logs"].append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "phase": phase or self.state["current_phase"],
            "iteration": self.state["iteration"]
        })
        self.save()


class ThaiOCRFixes:
    """Thai text fix functions"""
    
    @staticmethod
    def fix_vowels(text: str) -> str:
        """Fix Thai vowel OCR errors"""
        fixes = [
            (r'กระ(?!ร)', 'กระ'),
            (r'จะ(?!ก)', 'จะ'),
            (r'([ก-ฮ])ั้', r'\1้ำ'),
        ]
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text)
        return text
    
    @staticmethod
    def fix_tone_marks(text: str) -> str:
        """Fix Thai tone mark stacking"""
        fixes = [
            (r'([ก-ฮ])่้', r'\1้'),
            (r'([ก-ฮ])้่', r'\1้'),
            (r'([ก-ฮ])้๊', r'\1้'),
            (r'([ก-ฮ])้๋', r'\1้'),
        ]
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text)
        return text
    
    @staticmethod
    def fix_numerals(text: str) -> str:
        """Convert Thai numerals to Arabic"""
        thai_to_arabic = {
            '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5',
            '๖': '6', '๗': '7', '๘': '8', '๙': '9', '๐': '0'
        }
        for thai, arabic in thai_to_arabic.items():
            text = text.replace(thai, arabic)
        return text
    
    @staticmethod
    def fix_legal_terms(text: str) -> str:
        """Fix Thai legal/government terms"""
        fixes = {
            'กรม ที่ ดิน': 'กรมที่ดิน',
            'กระทรวง มหาดไทย': 'กระทรวงมหาดไทย',
            'สัญญา จ้าง': 'สัญญาจ้าง',
            'ข้อ ตกลง': 'ข้อตกลง',
        }
        for wrong, correct in fixes.items():
            text = text.replace(wrong, correct)
        return text
    
    @staticmethod
    def fix_spacing(text: str) -> str:
        """Fix spacing issues"""
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'([a-zA-Z]) ([a-zA-Z])', r'\1\2', text)
        return text


def calculate_quality(text: str) -> float:
    """Calculate Thai OCR quality score"""
    score = 1.0
    
    # Deductions
    score -= min(len(re.findall(r'\[OCR Error', text)) * 0.1, 0.3)
    score -= min(len(re.findall(r'\?\?\?', text)) * 0.03, 0.15)
    score -= min(len(re.findall(r'  +', text)) * 0.01, 0.1)
    score -= min(len(re.findall(r'[่้๊๋]{2,}', text)) * 0.05, 0.15)
    
    # Bonuses
    thai_chars = len(re.findall(r'[\u0E00-\u0E7F]', text))
    if thai_chars / max(len(text), 1) > 0.3:
        score += 0.05
    
    return max(0.0, min(1.0, score))


def run_initial_ocr(input_file: str):
    """Run initial OCR on input file"""
    try:
        from ocr_skill import process_file
        result = process_file(input_file, show_progress=False)
        
        # Save OCR output
        output_txt = f"output_txt/{Path(input_file).stem}.txt"
        Path("output_txt").mkdir(exist_ok=True)
        
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result.get_all_text())
        
        print(f"✓ OCR complete: {output_txt}")
        print(f"  Pages: {result.total_pages}")
        print(f"  Characters: {len(result.get_all_text())}")
        
    except Exception as e:
        print(f"❌ OCR failed: {e}")


def run_manager(state: PDCAState, action: str = 'start'):
    """Manager Agent tasks"""
    print("\n" + "="*60)
    print("🎯 MANAGER AGENT")
    print("="*60)
    
    if action == 'start':
        print("Task: Initialize PDCA cycle")
        state.log("Manager", "Started PDCA cycle", "plan")
        print(f"✓ Task ID: {state.state['task_id']}")
        print(f"✓ Target quality: {state.state['target_quality']:.0%}")
        print(f"✓ Phase: {state.state['current_phase']}")
        
        # Run initial OCR
        print("\n  Running initial OCR...")
        run_initial_ocr(state.state['input_file'])
        
    elif action == 'review':
        print("Task: Review current state")
        s = state.state
        print(f"  Phase: {s['current_phase']}")
        print(f"  Iteration: {s['iteration']}")
        print(f"  Quality: {s['current_quality']:.0%} / {s['target_quality']:.0%}")
        print(f"  Open bugs: {len(s['open_bugs'])}")
        
    elif action == 'decide':
        print("Task: Decide next action")
        s = state.state
        if s['current_quality'] >= s['target_quality'] and len(s['open_bugs']) == 0:
            print("✓ Quality target reached!")
            s['current_phase'] = 'complete'
            state.log("Manager", "PDCA cycle complete", "complete")
        else:
            print(f"  Continuing to iteration {s['iteration'] + 1}")
            s['iteration'] += 1
            s['current_phase'] = 'plan'
            state.log("Manager", f"Starting iteration {s['iteration']}", "plan")
        
        state.save()


def run_programmer(state: PDCAState):
    """Programmer Agent tasks"""
    print("\n" + "="*60)
    print("💻 PROGRAMMER AGENT")
    print("="*60)
    
    # Read OCR output
    ocr_file = state.state['output_files']['ocr']
    if not Path(ocr_file).exists():
        print(f"❌ OCR output not found: {ocr_file}")
        print("   Run: python src/ocr_processor.py")
        return
    
    with open(ocr_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"✓ Read OCR output: {len(text)} characters")
    
    # Apply fixes
    fixes_applied = []
    original = text
    
    text = ThaiOCRFixes.fix_vowels(text)
    if text != original:
        fixes_applied.append("Thai vowel corrections")
        original = text
    
    text = ThaiOCRFixes.fix_tone_marks(text)
    if text != original:
        fixes_applied.append("Tone mark corrections")
        original = text
    
    text = ThaiOCRFixes.fix_numerals(text)
    if text != original:
        fixes_applied.append("Thai numeral conversion")
        original = text
    
    text = ThaiOCRFixes.fix_legal_terms(text)
    if text != original:
        fixes_applied.append("Legal term corrections")
        original = text
    
    text = ThaiOCRFixes.fix_spacing(text)
    if text != original:
        fixes_applied.append("Spacing fixes")
    
    # Save reviewed output
    reviewed_file = state.state['output_files']['reviewed']
    with open(reviewed_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✓ Applied fixes: {', '.join(fixes_applied) if fixes_applied else 'None needed'}")
    print(f"✓ Saved: {reviewed_file}")
    
    # Update state
    state.state['fixes_applied'].append({
        'iteration': state.state['iteration'],
        'fixes': fixes_applied,
        'timestamp': datetime.now().isoformat()
    })
    state.state['current_phase'] = 'check'
    state.log("Programmer", f"Applied {len(fixes_applied)} fix types", "do")
    state.save()


def run_qa(state: PDCAState):
    """QA Agent tasks"""
    print("\n" + "="*60)
    print("✅ QA AGENT")
    print("="*60)
    
    # Read reviewed output
    reviewed_file = state.state['output_files']['reviewed']
    if not Path(reviewed_file).exists():
        print(f"❌ Reviewed output not found: {reviewed_file}")
        return
    
    with open(reviewed_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Calculate quality
    quality = calculate_quality(text)
    state.state['current_quality'] = quality
    print(f"✓ Quality score: {quality:.0%}")
    print(f"✓ Target: {state.state['target_quality']:.0%}")
    
    # Identify remaining issues
    issues = []
    if re.search(r'[่้๊๋]{2,}', text):
        issues.append({'type': 'tone_mark', 'severity': 'high'})
    if re.search(r'  +', text):
        issues.append({'type': 'spacing', 'severity': 'low'})
    
    state.state['open_bugs'].extend(issues)
    print(f"✓ Remaining issues: {len(issues)}")
    
    # Update state
    state.state['current_phase'] = 'act'
    state.log("QA", f"Quality {quality:.0%}, {len(issues)} issues", "check")
    state.save()
    
    # Decision preview
    if quality >= state.state['target_quality']:
        print("\n✓ Quality target reached! Manager will finalize.")
    else:
        print(f"\n⚠ Quality below target. Continuing PDCA cycle.")


def main():
    parser = argparse.ArgumentParser(description="PDCA Loop Runner for Thai OCR")
    parser.add_argument('--input', help='Input PDF file')
    parser.add_argument('--target-quality', type=float, default=0.95, help='Target quality (0.0-1.0)')
    parser.add_argument('--resume', action='store_true', help='Resume existing task')
    parser.add_argument('--agent', choices=['manager', 'programmer', 'qa', 'auto'], 
                       default='auto', help='Run specific agent')
    
    args = parser.parse_args()
    
    # Initialize state
    state = PDCAState()
    
    # Create or resume
    if args.resume:
        if not state.state:
            print("❌ No saved state found. Start with --input")
            return
        print(f"✓ Resumed task: {state.state['task_id']}")
    else:
        if not args.input:
            print("❌ --input required for new task")
            return
        task_id = f"thai_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        state.create(task_id, args.input, args.target_quality)
        print(f"✓ Created task: {task_id}")
    
    # Run agents in sequence
    print("\n" + "="*60)
    print("🔄 STARTING PDCA CYCLE")
    print("="*60)
    
    # Phase: PLAN (Manager)
    if state.state['current_phase'] == 'plan':
        run_manager(state, 'review')
        run_manager(state, 'decide')
    
    # Phase: DO (Programmer)
    if state.state['current_phase'] == 'do':
        run_programmer(state)
    
    # Phase: CHECK (QA)
    if state.state['current_phase'] == 'check':
        run_qa(state)
    
    # Phase: ACT (Manager decision)
    if state.state['current_phase'] == 'act':
        run_manager(state, 'decide')
    
    # Print status
    print("\n" + "="*60)
    print("📊 STATUS")
    print("="*60)
    s = state.state
    print(f"Phase: {s['current_phase']}")
    print(f"Iteration: {s['iteration']}")
    print(f"Quality: {s['current_quality']:.0%} / {s['target_quality']:.0%}")
    print(f"Open bugs: {len(s['open_bugs'])}")
    print(f"Fixes applied: {len(s['fixes_applied'])}")
    
    if s['current_phase'] == 'complete':
        print("\n✅ PDCA CYCLE COMPLETE!")


if __name__ == "__main__":
    main()
