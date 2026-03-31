"""
PDCA Dev Tools - Python helpers for small team
===============================================

Simple Python tools to help the dev team work efficiently
with minimal token usage.

Usage:
    python dev_tools.py plan          # Tech Lead planning
    python dev_tools.py status        # Check current status
    python dev_tools.py test          # QA testing
    python dev_tools.py report        # Generate weekly report
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class PDCATools:
    """Dev team tools for PDCA workflow"""
    
    def __init__(self):
        self.log_file = Path("pdca_log.json")
        self.state = self._load_log()
    
    def _load_log(self) -> Dict:
        """Load pdca_log.json"""
        if not self.log_file.exists():
            return {
                "project": "OCR Skill",
                "team_size": 3,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "weeks": []
            }
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_log(self):
        """Save pdca_log.json"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    # ========== TECH LEAD TOOLS ==========
    
    def plan_week(self, focus: str, tasks: List[str], goals: List[str]):
        """
        Plan new week (Tech Lead)
        
        Usage:
            tools.plan_week(
                focus="Thai numeral conversion",
                tasks=["Add numeral converter", "Write tests", "Update docs"],
                goals=["Improve accuracy by 5%"]
            )
        """
        week_num = len(self.state["weeks"]) + 1
        
        week_data = {
            "week": week_num,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "focus": focus,
            "tasks": [{"task": t, "status": "todo"} for t in tasks],
            "goals": goals,
            "status": "in_progress"
        }
        
        self.state["weeks"].append(week_data)
        self._save_log()
        
        print(f"✓ Week {week_num} planned")
        print(f"  Focus: {focus}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Goals: {len(goals)}")
    
    def review_week(self, quality_before: str, quality_after: str, 
                    improvement: str, notes: str = ""):
        """
        Review completed week (Tech Lead)
        
        Usage:
            tools.review_week(
                quality_before="87%",
                quality_after="92%",
                improvement="+5%",
                notes="Numeral conversion working well"
            )
        """
        if not self.state["weeks"]:
            print("❌ No weeks to review")
            return
        
        current_week = self.state["weeks"][-1]
        current_week["end_date"] = datetime.now().strftime("%Y-%m-%d")
        current_week["results"] = {
            "quality_before": quality_before,
            "quality_after": quality_after,
            "improvement": improvement,
            "notes": notes
        }
        current_week["status"] = "complete"
        
        self._save_log()
        
        print(f"✓ Week {current_week['week']} reviewed")
        print(f"  Quality: {quality_before} → {quality_after}")
        print(f"  Improvement: {improvement}")
    
    # ========== DEVELOPER TOOLS ==========
    
    def thai_numerals_fix(self, text: str) -> str:
        """
        Fix Thai numerals (Developer tool)
        
        Usage:
            fixed = tools.thai_numerals_fix("๑๒๓๔๕")
            # Returns: "12345"
        """
        thai_nums = {
            '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5',
            '๖': '6', '๗': '7', '๘': '8', '๙': '9', '๐': '0'
        }
        for thai, arabic in thai_nums.items():
            text = text.replace(thai, arabic)
        return text
    
    def thai_vowels_fix(self, text: str) -> str:
        """
        Fix Thai vowel stacking (Developer tool)
        
        Usage:
            fixed = tools.thai_vowels_fix("กระทั้")
        """
        fixes = [
            (r'([ก-ฮ])ั้', r'\1้ำ'),
            (r'กระ(?!ร)', 'กระ'),
            (r'จะ(?!ก)', 'จะ'),
        ]
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text)
        return text
    
    def thai_tone_marks_fix(self, text: str) -> str:
        """
        Fix Thai tone mark stacking (Developer tool)
        
        Usage:
            fixed = tools.thai_tone_marks_fix("หน้า้ที่")
        """
        fixes = [
            (r'([ก-ฮ])่้', r'\1้'),
            (r'([ก-ฮ])้่', r'\1้'),
            (r'([ก-ฮ])้๊', r'\1้'),
            (r'([ก-ฮ])้๋', r'\1้'),
        ]
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text)
        return text
    
    def legal_terms_fix(self, text: str) -> str:
        """
        Fix Thai legal terms (Developer tool)
        
        Usage:
            fixed = tools.legal_terms_fix("กรม ที่ ดิน")
            # Returns: "กรมที่ดิน"
        """
        fixes = {
            'กรม ที่ ดิน': 'กรมที่ดิน',
            'กระทรวง มหาดไทย': 'กระทรวงมหาดไทย',
            'สัญญา จ้าง': 'สัญญาจ้าง',
            'ข้อ ตกลง': 'ข้อตกลง',
            'คู่ สัญญา': 'คู่สัญญา',
        }
        for wrong, correct in fixes.items():
            text = text.replace(wrong, correct)
        return text
    
    def apply_all_fixes(self, text: str) -> str:
        """
        Apply all Thai text fixes (Developer tool)
        
        Usage:
            fixed = tools.apply_all_fixes(ocr_text)
        """
        text = self.thai_numerals_fix(text)
        text = self.thai_vowels_fix(text)
        text = self.thai_tone_marks_fix(text)
        text = self.legal_terms_fix(text)
        
        # Basic cleanup
        text = re.sub(r'  +', ' ', text)
        
        return text
    
    # ========== QA TOOLS ==========
    
    def calculate_quality(self, text: str) -> float:
        """
        Calculate OCR quality score (QA tool)
        
        Usage:
            score = tools.calculate_quality(ocr_text)
            # Returns: 0.0 to 1.0
        """
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
    
    def test_document(self, filepath: str) -> Dict:
        """
        Test OCR output file (QA tool)
        
        Usage:
            results = tools.test_document("output_txt/doc.txt")
        """
        if not Path(filepath).exists():
            return {"error": f"File not found: {filepath}"}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        quality = self.calculate_quality(text)
        
        # Count issues
        issues = {
            'ocr_errors': len(re.findall(r'\[OCR Error', text)),
            'unknown_chars': len(re.findall(r'\?\?\?', text)),
            'spacing_issues': len(re.findall(r'  +', text)),
            'tone_stacking': len(re.findall(r'[่้๊๋]{2,}', text)),
            'thai_numerals': len(re.findall(r'[๑๒๓๔๕๖๗๘๙๐]', text)),
        }
        
        return {
            "file": filepath,
            "characters": len(text),
            "quality": f"{quality:.0%}",
            "issues": issues
        }
    
    def compare_outputs(self, file1: str, file2: str) -> Dict:
        """
        Compare two OCR outputs (QA tool)
        
        Usage:
            comparison = tools.compare_outputs("before.txt", "after.txt")
        """
        with open(file1, 'r', encoding='utf-8') as f:
            text1 = f.read()
        with open(file2, 'r', encoding='utf-8') as f:
            text2 = f.read()
        
        q1 = self.calculate_quality(text1)
        q2 = self.calculate_quality(text2)
        
        return {
            "file1": {"path": file1, "quality": f"{q1:.0%}"},
            "file2": {"path": file2, "quality": f"{q2:.0%}"},
            "improvement": f"{(q2-q1)*100:+.1f}%"
        }
    
    # ========== REPORTING TOOLS ==========
    
    def status(self):
        """Show current status"""
        print("\n" + "="*60)
        print("📊 OCR Skill - PDCA Status")
        print("="*60)
        
        print(f"\nProject: {self.state['project']}")
        print(f"Team size: {self.state['team_size']}")
        print(f"Started: {self.state['start_date']}")
        
        if self.state["weeks"]:
            current = self.state["weeks"][-1]
            print(f"\nCurrent Week: {current.get('week', 'N/A')}")
            print(f"Focus: {current.get('focus', 'N/A')}")
            print(f"Status: {current.get('status', 'N/A')}")
            
            if "results" in current:
                r = current["results"]
                print(f"\nResults:")
                print(f"  Quality: {r.get('quality_before', 'N/A')} → {r.get('quality_after', 'N/A')}")
                print(f"  Improvement: {r.get('improvement', 'N/A')}")
        else:
            print("\nNo weeks logged yet. Start with: python dev_tools.py plan")
        
        print()
    
    def report(self):
        """Generate full report"""
        print("\n" + "="*60)
        print("📈 OCR Skill - Progress Report")
        print("="*60)
        
        if not self.state["weeks"]:
            print("\nNo data yet")
            return
        
        print(f"\nTotal weeks: {len(self.state['weeks'])}")
        print(f"Completed: {sum(1 for w in self.state['weeks'] if w.get('status') == 'complete')}")
        
        # Calculate overall improvement
        completed = [w for w in self.state["weeks"] if w.get("status") == "complete"]
        if completed:
            first = completed[0].get("results", {})
            last = completed[-1].get("results", {})
            
            print(f"\nQuality Progress:")
            print(f"  Start: {first.get('quality_before', 'N/A')}")
            print(f"  Current: {last.get('quality_after', 'N/A')}")
            
            # Total improvement
            try:
                start_q = float(first.get('quality_before', '0').replace('%', ''))
                end_q = float(last.get('quality_after', '0').replace('%', ''))
                print(f"  Total: {end_q - start_q:+.1f}%")
            except:
                pass
        
        print("\nWeekly Summary:")
        for week in self.state["weeks"]:
            status_icon = "✓" if week.get("status") == "complete" else "○"
            print(f"  {status_icon} Week {week.get('week')}: {week.get('focus', 'N/A')}")
        
        print()


# CLI Interface
def main():
    tools = PDCATools()
    
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  status              - Show current status")
        print("  report              - Generate full report")
        print("  plan                - Plan new week (interactive)")
        print("  review              - Review completed week")
        print("  test <file>         - Test OCR output file")
        print("  compare <f1> <f2>   - Compare two files")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        tools.status()
    
    elif cmd == "report":
        tools.report()
    
    elif cmd == "plan":
        print("\n=== Plan New Week ===\n")
        focus = input("Focus: ")
        tasks = input("Tasks (comma-separated): ").split(",")
        goals = input("Goals (comma-separated): ").split(",")
        tools.plan_week(focus.strip(), [t.strip() for t in tasks], [g.strip() for g in goals])
    
    elif cmd == "review":
        print("\n=== Review Week ===\n")
        before = input("Quality before: ")
        after = input("Quality after: ")
        improvement = input("Improvement: ")
        notes = input("Notes: ")
        tools.review_week(before, after, improvement, notes)
    
    elif cmd == "test":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py test <file>")
            return
        result = tools.test_document(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == "compare":
        if len(sys.argv) < 4:
            print("Usage: python dev_tools.py compare <file1> <file2>")
            return
        result = tools.compare_outputs(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
