"""
Programmer Agent for OCR Improvement
=====================================

This agent works within the PDCA loop to incrementally improve
Thai OCR text quality.

Responsibilities:
1. Read bug reports
2. Analyze OCR output
3. Apply targeted fixes
4. Document changes
5. Update quality metrics

Usage:
    python programmer_agent.py --task-id TASK_ID
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdca.pdca_controller import PDCAController


class ProgrammerAgent:
    """
    AI Programmer Agent for OCR text improvement.
    
    This agent reads bugs, analyzes OCR output, and applies
    targeted fixes for Thai text issues.
    """
    
    def __init__(self, controller: PDCAController):
        self.controller = controller
        self.logger = controller.logger
        self.workspace = controller.workspace
        
        # Thai text patterns for common OCR errors
        self.thai_fix_patterns = self._load_thai_patterns()
        
        self.logger.info("Programmer Agent initialized")
    
    def _load_thai_patterns(self) -> Dict:
        """Load common Thai OCR error patterns"""
        return {
            # Thai vowels that are often misrecognized
            'vowels': {
                'ะ': ['ะ', 'ั', 'า'],  # Short/long a
                'ิ': ['ิ', 'ี'],  # i / ii
                'ุ': ['ุ', 'ู'],  # u / uu
                'เ': ['เ', 'แ'],  # e / ae
                'โ': ['โ', 'ใ', 'ไ'],  # o / ai
            },
            # Tone marks
            'tones': {
                '่': ['่', '้', '๊', '๋'],
                '้': ['้', '่', '๊', '๋'],
            },
            # Common number confusions
            'numbers': {
                '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5',
                '๖': '6', '๗': '7', '๘': '8', '๙': '9', '๐': '0',
            },
            # Common character confusions
            'confusables': {
                'ก': ['ก', 'ภ'],
                'ง': ['ง', 'พ'],
                'ต': ['ต', 'ด'],
                'ถ': ['ถ', 'ท'],
            }
        }
    
    def analyze_bugs(self) -> List[Dict]:
        """
        Analyze open bugs and prioritize fixes.
        
        Returns:
            List of bugs with priority scores
        """
        bugs = self.controller.get_open_bugs()
        
        # Add priority scores
        for bug in bugs:
            priority = self._calculate_priority(bug)
            bug['priority'] = priority
        
        # Sort by priority (highest first)
        bugs.sort(key=lambda x: x['priority'], reverse=True)
        
        self.logger.info(f"Analyzing {len(bugs)} bugs")
        for bug in bugs[:5]:  # Show top 5
            self.logger.info(f"  {bug['id']}: {bug['type']} (priority: {bug['priority']})")
        
        return bugs
    
    def _calculate_priority(self, bug: Dict) -> int:
        """Calculate bug fix priority (1-10)"""
        severity_scores = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
        
        base_score = severity_scores.get(bug['severity'], 4)
        
        # Boost priority for certain bug types
        type_boost = {
            'thai_vowel': 2,
            'tone_mark': 2,
            'number': 1,
            'spacing': 1,
            'word_boundary': 2,
        }
        
        return base_score + type_boost.get(bug['type'], 0)
    
    def apply_fix(self, bug: Dict, text: str) -> Tuple[str, bool]:
        """
        Apply fix for a specific bug.
        
        Args:
            bug: Bug dictionary
            text: Current OCR text
        
        Returns:
            Tuple of (fixed_text, success)
        """
        self.logger.info(f"Applying fix for {bug['id']}: {bug['type']}")
        
        fixed_text = text
        success = False
        
        try:
            if bug['type'] == 'thai_vowel':
                fixed_text, success = self._fix_thai_vowel(fixed_text, bug)
            elif bug['type'] == 'tone_mark':
                fixed_text, success = self._fix_tone_mark(fixed_text, bug)
            elif bug['type'] == 'number':
                fixed_text, success = self._fix_numbers(fixed_text, bug)
            elif bug['type'] == 'spacing':
                fixed_text, success = self._fix_spacing(fixed_text, bug)
            elif bug['type'] == 'word_boundary':
                fixed_text, success = self._fix_word_boundaries(fixed_text, bug)
            else:
                fixed_text, success = self._apply_custom_fix(fixed_text, bug)
            
            if success:
                self.controller.resolve_bug(bug['id'], f"Applied {bug['type']} fix")
                self.logger.info(f"✓ Fix successful for {bug['id']}")
            else:
                self.logger.warning(f"✗ Fix failed for {bug['id']}")
        
        except Exception as e:
            self.logger.error(f"Error applying fix: {e}")
            success = False
        
        return fixed_text, success
    
    def _fix_thai_vowel(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Fix Thai vowel recognition errors"""
        # Example: Fix common vowel confusions
        patterns = [
            (r'กระ(?!ร)', 'กระ'),  # Common prefix
            (r'การ(?=[\sฯ])', 'การ'),  # Common word
        ]
        
        fixed = text
        applied = False
        
        for pattern, replacement in patterns:
            new_fixed = re.sub(pattern, replacement, fixed)
            if new_fixed != fixed:
                applied = True
                fixed = new_fixed
        
        return fixed, applied
    
    def _fix_tone_mark(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Fix Thai tone mark errors"""
        # Tone mark corrections based on context
        fixed = text
        applied = False
        
        # Common tone mark patterns
        tone_patterns = [
            (r'([ก-ฮ])่้', r'\1้'),  # Double tone mark
            (r'([ก-ฮ])้่', r'\1้'),
        ]
        
        for pattern, replacement in tone_patterns:
            new_fixed = re.sub(pattern, replacement, fixed)
            if new_fixed != fixed:
                applied = True
                fixed = new_fixed
        
        return fixed, applied
    
    def _fix_numbers(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Convert Thai numerals to Arabic if needed"""
        thai_nums = self.thai_fix_patterns['numbers']
        
        fixed = text
        applied = False
        
        for thai, arabic in thai_nums.items():
            if thai in fixed:
                fixed = fixed.replace(thai, arabic)
                applied = True
        
        return fixed, applied
    
    def _fix_spacing(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Fix spacing issues in Thai text"""
        fixed = text
        applied = False
        
        # Remove multiple spaces
        new_fixed = re.sub(r'  +', ' ', fixed)
        if new_fixed != fixed:
            applied = True
            fixed = new_fixed
        
        # Fix space before punctuation
        new_fixed = re.sub(r' +([,\.!?;:])', r'\1', fixed)
        if new_fixed != fixed:
            applied = True
            fixed = new_fixed
        
        return fixed, applied
    
    def _fix_word_boundaries(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Fix word boundary detection"""
        # Thai doesn't use spaces between words, but OCR may add them
        fixed = text
        applied = False
        
        # Common incorrectly split words
        split_words = [
            (r'ประ เทศ', 'ประเทศ'),
            (r'ไทย', 'ไทย'),
            (r'กรม ที่ ดิน', 'กรมที่ดิน'),
        ]
        
        for wrong, correct in split_words:
            if wrong in fixed:
                fixed = fixed.replace(wrong, correct)
                applied = True
        
        return fixed, applied
    
    def _apply_custom_fix(self, text: str, bug: Dict) -> Tuple[str, bool]:
        """Apply custom fix based on bug description"""
        # Use bug description to guide fix
        description = bug.get('description', '').lower()
        location = bug.get('location', '')
        
        # Simple heuristic fixes based on description keywords
        if 'double' in description and 'space' in description:
            text, _ = self._fix_spacing(text, bug)
            return text, True
        
        if 'thai' in description and 'character' in description:
            text, _ = self._fix_thai_vowel(text, bug)
            return text, True
        
        return text, False
    
    def calculate_quality(self, text: str) -> float:
        """
        Calculate text quality score.
        
        Factors:
        - Character error rate (estimated)
        - Spacing issues
        - Unrecognized characters
        - Thai script consistency
        """
        if not text:
            return 0.0
        
        # Start with perfect score
        score = 1.0
        
        # Deduct for error indicators
        error_patterns = [
            (r'\[OCR Error', 0.1),  # OCR errors
            (r'  +', 0.02),  # Multiple spaces
            (r'', 0.05),  # Unrecognized chars
            (r'\?\?\?', 0.03),  # Unknown sequences
        ]
        
        for pattern, deduction in error_patterns:
            matches = len(re.findall(pattern, text))
            score -= min(matches * deduction, 0.2)  # Cap each at 20%
        
        # Bonus for Thai script consistency
        thai_chars = len(re.findall(r'[\u0E00-\u0E7F]', text))
        if thai_chars > len(text) * 0.3:  # At least 30% Thai
            score += 0.05
        
        return max(0.0, min(1.0, score))
    
    def process_file(self) -> Dict:
        """
        Process OCR output file and apply all fixes.
        
        Returns:
            Processing summary
        """
        state = self.controller.state
        
        # Read OCR output
        if not Path(state.ocr_output_file).exists():
            self.logger.error(f"OCR output not found: {state.ocr_output_file}")
            return {"error": "OCR output not found"}
        
        with open(state.ocr_output_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        self.logger.info(f"Read OCR output: {len(text)} characters")
        
        # Analyze bugs
        bugs = self.analyze_bugs()
        
        # Apply fixes
        fixes_applied = 0
        for bug in bugs:
            text, success = self.apply_fix(bug, text)
            if success:
                fixes_applied += 1
        
        # Calculate quality
        quality = self.calculate_quality(text)
        self.controller.update_quality_score(quality)
        
        # Save reviewed output
        with open(state.reviewed_output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        self.logger.info(f"Saved reviewed output: {state.reviewed_output_file}")
        
        return {
            "input_chars": len(text),
            "bugs_analyzed": len(bugs),
            "fixes_applied": fixes_applied,
            "quality_score": quality,
            "output_file": state.reviewed_output_file
        }


def run_programmer_agent(task_id: str = None):
    """
    Run programmer agent for a task.
    
    Args:
        task_id: Task ID to resume (or load latest)
    """
    controller = PDCAController()
    
    # Load state
    state = controller.load_state()
    if not state:
        print("No active PDCA task found. Run pdca_controller.py first.")
        return
    
    if task_id and state.task_id != task_id:
        print(f"Task mismatch. Expected {task_id}, found {state.task_id}")
        return
    
    # Initialize agent
    agent = ProgrammerAgent(controller)
    
    print(f"\n{'='*60}")
    print(f"Programmer Agent - Task: {state.task_id}")
    print(f"Phase: {state.current_state}")
    print(f"Iteration: {state.iteration}")
    print(f"Open bugs: {len(controller.get_open_bugs())}")
    print(f"{'='*60}\n")
    
    # Process file
    result = agent.process_file()
    
    print(f"\n{'='*60}")
    print("Processing Complete")
    print(f"{'='*60}")
    print(f"Bugs analyzed: {result.get('bugs_analyzed', 0)}")
    print(f"Fixes applied: {result.get('fixes_applied', 0)}")
    print(f"Quality score: {result.get('quality_score', 0):.2%}")
    print(f"Output: {result.get('output_file', 'N/A')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Programmer Agent for OCR Improvement")
    parser.add_argument("--task-id", default=None, help="Task ID to process")
    
    args = parser.parse_args()
    
    run_programmer_agent(args.task_id)
