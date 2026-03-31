"""
PDCA Dev Tools - Python helpers for AI agents
===============================================

Simple Python tools to help AI agents work efficiently
with minimal token usage.

Usage:
    from ai_tools.dev_tools import PDCATools
    tools = PDCATools()
    
    # Apply Thai fixes
    fixed = tools.apply_all_fixes(text)
    
    # Test quality
    quality = tools.calculate_quality(text)
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class PDCATools:
    """AI agent tools for PDCA workflow"""
    
    def __init__(self):
        self.log_file = Path("pdca_log.json")
        self.state = self._load_log()
        self._activities = []  # Store activities locally
    
    def _log_activity(self, agent: str, action: str, details: str = "", task_id: str = ""):
        """Log agent activity internally and update web dashboard"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "details": details
        }
        self._activities.append(activity)
        
        # Also save to pdca_log.json
        if "agent_activities" not in self.state:
            self.state["agent_activities"] = []
        self.state["agent_activities"].append(activity)
        
        # Keep last 100
        if len(self.state["agent_activities"]) > 100:
            self.state["agent_activities"] = self.state["agent_activities"][-100:]
        
        self._save_log()
        
        # Update web dashboard
        self._update_web_dashboard(agent, action, details, task_id)
    
    def _update_web_dashboard(self, agent: str, status: str, task: str, task_id: str):
        """Update web dashboard data"""
        try:
            import urllib.request
            
            # If agent is resting/idle, don't specify task_id so they stay at rest area
            if status in ['resting', 'idle']:
                url = f"http://localhost:8000/api/update?agent={agent}&status={status}&task={task}"
            else:
                url = f"http://localhost:8000/api/update?agent={agent}&status={status}&task={task}&task_id={task_id}"
            
            urllib.request.urlopen(url, timeout=1)
        except:
            pass  # Dashboard not running, that's ok
    
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
        Plan new week (Tech Lead agent)
        
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
        
        # Log agent activity
        self._log_activity(
            "Tech Lead",
            "planning",
            f"Week {week_num}: {focus}",
            task_id="plan_week"
        )
        
        print(f"✓ Week {week_num} planned")
        print(f"  Focus: {focus}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Goals: {len(goals)}")
    
    def review_week(self, quality_before: str, quality_after: str, 
                    improvement: str, notes: str = ""):
        """
        Review completed week (Tech Lead agent)
        
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
        
        # Log agent activity
        self._log_activity(
            "Tech Lead",
            "reviewing",
            f"Quality: {quality_before} → {quality_after} ({improvement})",
            task_id="review_week"
        )
        
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
    
    def apply_all_fixes(self, text: str, show_progress: bool = False) -> str:
        """
        Apply all Thai text fixes (Developer agent)
        
        Usage:
            fixed = tools.apply_all_fixes(ocr_text)
            fixed = tools.apply_all_fixes(ocr_text, show_progress=True)
        """
        original = text
        fixes_applied = []
        
        if show_progress:
            print("Applying Thai text fixes...")
        
        # Step 1: Numerals
        text = self.thai_numerals_fix(text)
        if text != original:
            fixes_applied.append("numerals")
            original = text
            if show_progress:
                print("  ✓ Numerals converted")
        
        # Step 2: Vowels
        text = self.thai_vowels_fix(text)
        if text != original:
            fixes_applied.append("vowels")
            original = text
            if show_progress:
                print("  ✓ Vowels corrected")
        
        # Step 3: Tone marks
        text = self.thai_tone_marks_fix(text)
        if text != original:
            fixes_applied.append("tone marks")
            original = text
            if show_progress:
                print("  ✓ Tone marks fixed")
        
        # Step 4: Legal terms
        text = self.legal_terms_fix(text)
        if text != original:
            fixes_applied.append("legal terms")
            if show_progress:
                print("  ✓ Legal terms corrected")
        
        # Basic cleanup
        text = re.sub(r'  +', ' ', text)
        
        if show_progress:
            print(f"Total fixes applied: {len(fixes_applied)} ({', '.join(fixes_applied)})")
        
        # Log agent activity
        if fixes_applied:
            self._log_activity(
                "Developer",
                "working",
                f"Applied: {', '.join(fixes_applied)}",
                task_id="write_code"
            )
        
        return text
    
    # ========== QA TOOLS ==========
    
    def batch_test(self, folder: str, pattern: str = "*.txt") -> List[Dict]:
        """
        Test multiple OCR output files (QA tool)
        
        Usage:
            results = tools.batch_test("output_txt")
        """
        from glob import glob
        
        files = glob(str(Path(folder) / pattern))
        results = []
        
        print(f"Testing {len(files)} files in {folder}...")
        
        for i, file in enumerate(files, 1):
            result = self.test_document(file)
            result['index'] = i
            results.append(result)
            
            # Show progress
            q = result.get('quality', 'N/A')
            print(f"  [{i}/{len(files)}] {Path(file).name}: {q}")
        
        # Summary
        avg_quality = sum(float(r.get('quality', '0%').replace('%', '')) 
                         for r in results if 'quality' in r) / len(results) if results else 0
        
        print(f"\nAverage quality: {avg_quality:.1f}%")
        
        return results
    
    def calculate_quality(self, text: str, log: bool = True) -> float:
        """
        Calculate OCR quality score (QA agent)
        
        Usage:
            score = tools.calculate_quality(ocr_text)
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
        
        # Log agent activity
        if log:
            self._log_activity(
                "QA",
                "testing",
                f"Quality: {score:.0%}",
                task_id="test_quality"
            )
        
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
    
    # ========== BATCH PROCESSING ==========
    
    def batch_process_files(self, input_folder: str, output_folder: str = "output_txt",
                           apply_fixes: bool = True, show_progress: bool = True) -> Dict:
        """
        Batch process multiple PDF files (Developer tool)
        
        Usage:
            results = tools.batch_process_files("input_pdf")
        """
        from glob import glob
        
        # Find all PDFs
        pdfs = glob(str(Path(input_folder) / "*.pdf"))
        
        if not pdfs:
            return {"error": "No PDF files found"}
        
        # Create output folder
        Path(output_folder).mkdir(exist_ok=True)
        
        results = {
            "total": len(pdfs),
            "processed": 0,
            "failed": 0,
            "files": []
        }
        
        print(f"Processing {len(pdfs)} PDF files...")
        
        for i, pdf in enumerate(pdfs, 1):
            pdf_name = Path(pdf).stem
            
            if show_progress:
                print(f"\n[{i}/{len(pdfs)}] {pdf_name}.pdf")
            
            try:
                # Run OCR
                from skill.ocr_skill import process_file
                result = process_file(pdf, show_progress=False)
                
                # Save output
                output_file = Path(output_folder) / f"{pdf_name}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.get_all_text())
                
                # Apply fixes if requested
                if apply_fixes:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                    fixed = self.apply_all_fixes(text, show_progress=False)
                    
                    if fixed != text:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(fixed)
                        if show_progress:
                            print(f"  ✓ Fixes applied")
                
                # Calculate quality
                with open(output_file, 'r', encoding='utf-8') as f:
                    quality = self.calculate_quality(f.read())
                
                results["processed"] += 1
                results["files"].append({
                    "name": pdf_name,
                    "output": str(output_file),
                    "quality": f"{quality:.0%}",
                    "pages": result.total_pages
                })
                
                if show_progress:
                    print(f"  ✓ Complete (Quality: {quality:.0%})")
                
            except Exception as e:
                results["failed"] += 1
                results["files"].append({
                    "name": pdf_name,
                    "error": str(e)
                })
                if show_progress:
                    print(f"  ✗ Failed: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"Batch Processing Complete")
        print(f"{'='*60}")
        print(f"Total: {results['total']} | Success: {results['processed']} | Failed: {results['failed']}")
        
        return results
    
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
        print("  batch-test <folder> - Test multiple files")
        print("  compare <f1> <f2>   - Compare two files")
        print("  batch-process       - Process all PDFs in folder")
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
    
    elif cmd == "batch-test":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py batch-test <folder>")
            return
        results = tools.batch_test(sys.argv[2])
    
    elif cmd == "batch-process":
        folder = sys.argv[2] if len(sys.argv) > 2 else "input_pdf"
        tools.batch_process_files(folder)
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
