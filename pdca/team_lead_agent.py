"""
Team Lead Agent - PDCA Loop Coordinator
========================================

This agent coordinates the PDCA improvement cycle, managing
the programmer agent and ensuring continuous improvement.

Responsibilities:
1. Initialize PDCA tasks
2. Coordinate agent workflow
3. Monitor progress
4. Handle crash recovery
5. Generate reports

Usage:
    python team_lead_agent.py --input input.pdf --target-quality 0.95
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdca.pdca_controller import PDCAController, PDCAState
from pdca.programmer_agent import ProgrammerAgent


class TeamLeadAgent:
    """
    Team Lead Agent for OCR improvement coordination.
    
    Manages the full PDCA cycle with crash recovery support.
    """
    
    def __init__(self, workspace: str = "pdca_workspace"):
        self.controller = PDCAController(workspace)
        self.workspace = Path(workspace)
        self.logger = self.controller.logger
        
        # Agent team
        self.programmer = None
        
        self.logger.info("="*60)
        self.logger.info("Team Lead Agent Initialized")
        self.logger.info("="*60)
    
    def start_task(self, input_file: str, task_id: str = None,
                   target_quality: float = 0.95) -> Dict:
        """
        Start a new OCR improvement task.
        
        Args:
            input_file: Input PDF/image file
            task_id: Optional task ID
            target_quality: Target quality score
        
        Returns:
            Task summary
        """
        self.logger.info(f"Starting new task: {input_file}")
        
        # Create task
        state = self.controller.create_task(task_id, input_file, target_quality)
        
        # Initialize programmer agent
        self.programmer = ProgrammerAgent(self.controller)
        
        return {
            "task_id": state.task_id,
            "input_file": state.input_file,
            "target_quality": f"{target_quality:.2%}",
            "workspace": str(self.workspace.absolute())
        }
    
    def resume_task(self, task_id: str = None) -> Optional[Dict]:
        """
        Resume existing task (crash recovery).
        
        Args:
            task_id: Optional task ID to resume
        
        Returns:
            Task summary or None
        """
        state = self.controller.load_state()
        
        if not state:
            self.logger.warning("No task to resume")
            return None
        
        if task_id and state.task_id != task_id:
            self.logger.error(f"Task ID mismatch: {state.task_id} vs {task_id}")
            return None
        
        # Initialize programmer agent
        self.programmer = ProgrammerAgent(self.controller)
        
        self.logger.info(f"Resumed task: {state.task_id}")
        self.logger.info(f"Phase: {state.current_state}")
        self.logger.info(f"Iteration: {state.iteration}")
        
        return {
            "task_id": state.task_id,
            "phase": state.current_state,
            "iteration": state.iteration,
            "open_bugs": len(self.controller.get_open_bugs()),
            "quality": f"{state.quality_score:.2%}"
        }
    
    def run_pdca_cycle(self, max_iterations: int = 10) -> Dict:
        """
        Run complete PDCA improvement cycle.
        
        Args:
            max_iterations: Maximum iterations before stopping
        
        Returns:
            Final status
        """
        state = self.controller.state
        
        if not state:
            return {"error": "No active task"}
        
        self.logger.info(f"Starting PDCA cycle (max {max_iterations} iterations)")
        
        iteration = 0
        
        while not self.controller.is_complete():
            iteration += 1
            
            if iteration > max_iterations:
                self.logger.warning(f"Max iterations ({max_iterations}) reached")
                break
            
            # Get current phase
            phase = self.controller.state.current_state
            
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"PDCA Cycle {iteration} - Phase: {phase.upper()}")
            self.logger.info(f"{'='*60}")
            
            try:
                if phase == PDCAState.PLAN.value:
                    self._plan_phase()
                elif phase == PDCAState.DO.value:
                    self._do_phase()
                elif phase == PDCAState.CHECK.value:
                    self._check_phase()
                elif phase == PDCAState.ACT.value:
                    self._act_phase()
                
                # Move to next phase
                self.controller.next_phase()
                
                # Log progress
                status = self.controller.get_status()
                self.controller.log_action(
                    "CYCLE_PROGRESS",
                    f"Phase={phase}, Quality={status['quality']}, " +
                    f"Bugs={status['open_bugs']}"
                )
                
            except Exception as e:
                self.logger.error(f"Error in {phase} phase: {e}")
                self.controller.log_action("ERROR", f"Phase {phase}: {str(e)}")
                # Save state for recovery
                self.controller._save_state()
                raise
        
        # Generate final report
        return self._generate_report()
    
    def _plan_phase(self):
        """PLAN: Identify issues in OCR output"""
        self.logger.info("[PLAN] Analyzing OCR output for issues...")
        
        # Read OCR output
        state = self.controller.state
        if not Path(state.ocr_output_file).exists():
            # Run initial OCR if not done
            self._run_initial_ocr()
        
        # Analyze for common Thai OCR issues
        self._identify_thai_issues()
        
        # Log bugs found
        bugs = self.controller.get_open_bugs()
        self.logger.info(f"Identified {len(bugs)} issues")
    
    def _do_phase(self):
        """DO: Apply fixes"""
        self.logger.info("[DO] Applying fixes...")
        
        if not self.programmer:
            self.programmer = ProgrammerAgent(self.controller)
        
        # Process file and apply fixes
        result = self.programmer.process_file()
        
        self.logger.info(f"Fixes applied: {result.get('fixes_applied', 0)}")
        self.logger.info(f"Quality: {result.get('quality_score', 0):.2%}")
    
    def _check_phase(self):
        """CHECK: Review results"""
        self.logger.info("[CHECK] Reviewing results...")
        
        state = self.controller.state
        
        # Read reviewed output
        if Path(state.reviewed_output_file).exists():
            with open(state.reviewed_output_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Calculate quality
            quality = self.programmer.calculate_quality(text)
            self.controller.update_quality_score(quality)
            
            self.logger.info(f"Current quality: {quality:.2%}")
            self.logger.info(f"Target quality: {state.target_quality:.2%}")
            
            # Check if we need more iterations
            if quality < state.target_quality:
                remaining_bugs = len(self.controller.get_open_bugs())
                self.logger.info(f"Remaining issues: {remaining_bugs}")
    
    def _act_phase(self):
        """ACT: Standardize successful fixes"""
        self.logger.info("[ACT] Standardizing fixes...")
        
        state = self.controller.state
        
        # Document successful fixes
        fixes = state.fixes_applied
        self.logger.info(f"Total fixes this iteration: {len(fixes)}")
        
        # Save fix patterns for future use
        self._save_fix_patterns(fixes)
    
    def _run_initial_ocr(self):
        """Run initial OCR on input file"""
        from ocr_skill import process_file
        
        state = self.controller.state
        
        self.logger.info(f"Running initial OCR on: {state.input_file}")
        
        try:
            result = process_file(state.input_file, show_progress=False)
            
            # Save OCR output
            with open(state.ocr_output_file, 'w', encoding='utf-8') as f:
                f.write(result.get_all_text())
            
            self.logger.info(f"OCR complete: {state.ocr_output_file}")
            
            # Add initial quality estimate
            quality = self.programmer.calculate_quality(result.get_all_text())
            self.controller.update_quality_score(quality)
            
        except Exception as e:
            self.logger.error(f"OCR failed: {e}")
            self.controller.add_bug(
                "critical",
                f"OCR processing failed: {str(e)}",
                severity="critical"
            )
    
    def _identify_thai_issues(self):
        """Identify common Thai OCR issues"""
        state = self.controller.state
        
        if not Path(state.ocr_output_file).exists():
            return
        
        with open(state.ocr_output_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Check for common issues
        
        # 1. Thai vowel issues
        if re.search(r'[ะัาิีุู]', text):
            # Check for potential vowel confusion
            self.controller.add_bug(
                "thai_vowel",
                "Thai vowels detected - may need context-based correction",
                severity="medium"
            )
        
        # 2. Tone mark issues
        if re.search(r'[่้๊๋]', text):
            self.controller.add_bug(
                "tone_mark",
                "Tone marks detected - verify correctness",
                severity="medium"
            )
        
        # 3. Thai numerals
        thai_nums = re.findall(r'[๑๒๓๔๕๖๗๘๙๐]', text)
        if thai_nums:
            self.controller.add_bug(
                "number",
                f"Found {len(thai_nums)} Thai numerals - convert to Arabic?",
                severity="low"
            )
        
        # 4. Spacing issues
        if re.search(r'  +', text):
            self.controller.add_bug(
                "spacing",
                "Multiple consecutive spaces detected",
                severity="low"
            )
        
        # 5. OCR errors
        if re.search(r'\[OCR Error', text):
            self.controller.add_bug(
                "ocr_error",
                "OCR errors present in output",
                severity="high"
            )
    
    def _save_fix_patterns(self, fixes: List[Dict]):
        """Save successful fix patterns for reuse"""
        patterns_file = self.workspace / "fix_patterns.json"
        
        patterns = []
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
        
        for fix in fixes:
            patterns.append({
                "timestamp": datetime.now().isoformat(),
                "fix": fix
            })
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved {len(fixes)} fix patterns")
    
    def _generate_report(self) -> Dict:
        """Generate final task report"""
        state = self.controller.state
        
        report = {
            "task_id": state.task_id,
            "status": "complete" if self.controller.is_complete() else "stopped",
            "final_quality": f"{state.quality_score:.2%}",
            "target_quality": f"{state.target_quality:.2%}",
            "total_iterations": state.iteration,
            "total_fixes": len(state.fixes_applied),
            "remaining_bugs": len(self.controller.get_open_bugs()),
            "output_files": {
                "ocr": state.ocr_output_file,
                "reviewed": state.reviewed_output_file,
                "logs": str(self.controller.log_file),
                "bugs": str(self.controller.bugs_file)
            },
            "completed_at": datetime.now().isoformat()
        }
        
        # Save report
        report_file = self.workspace / f"{state.task_id}_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Report saved: {report_file}")
        
        return report


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Team Lead Agent - PDCA Coordinator")
    parser.add_argument("--input", help="Input PDF/image file")
    parser.add_argument("--task-id", help="Task ID to resume")
    parser.add_argument("--target-quality", type=float, default=0.95,
                       help="Target quality (0.0-1.0)")
    parser.add_argument("--max-iterations", type=int, default=10,
                       help="Maximum PDCA iterations")
    parser.add_argument("--resume", action="store_true",
                       help="Resume existing task")
    
    args = parser.parse_args()
    
    # Initialize team lead
    team_lead = TeamLeadAgent()
    
    if args.resume or args.task_id:
        # Resume existing task
        task = team_lead.resume_task(args.task_id)
        if not task:
            print("No task to resume. Start a new task with --input")
            return
        print(f"✓ Resumed task: {task['task_id']}")
    else:
        # Start new task
        if not args.input:
            print("Error: --input required for new task")
            return
        
        task = team_lead.start_task(
            args.input,
            task_id=args.task_id,
            target_quality=args.target_quality
        )
        print(f"✓ Started task: {task['task_id']}")
    
    # Run PDCA cycle
    print(f"\nStarting PDCA improvement cycle...")
    print(f"Target quality: {args.target_quality:.2%}")
    print(f"Max iterations: {args.max_iterations}")
    
    result = team_lead.run_pdca_cycle(args.max_iterations)
    
    # Print summary
    print(f"\n{'='*60}")
    print("PDCA Cycle Complete")
    print(f"{'='*60}")
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Final Quality: {result.get('final_quality', 'N/A')}")
    print(f"Total Iterations: {result.get('total_iterations', 0)}")
    print(f"Total Fixes: {result.get('total_fixes', 0)}")
    print(f"\nOutput files:")
    for key, value in result.get('output_files', {}).items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
