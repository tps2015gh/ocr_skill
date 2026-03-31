"""
PDCA Loop Controller for OCR Skill
===================================

This module implements a Plan-Do-Check-Act (PDCA) cycle for continuous
improvement of OCR results, especially for complex Thai text.

Features:
- State persistence (survives AI crashes)
- Comprehensive logging
- Bug tracking file system
- Incremental improvement loop
- Multi-agent coordination

Usage:
    python pdca_controller.py
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class PDCAState(Enum):
    """PDCA Cycle States"""
    PLAN = "plan"
    DO = "do"
    CHECK = "check"
    ACT = "act"
    COMPLETE = "complete"


@dataclass
class TaskState:
    """Represents current task state (saved for crash recovery)"""
    task_id: str
    input_file: str
    current_state: str  # PDCAState value
    iteration: int
    ocr_output_file: str
    reviewed_output_file: str
    bugs: List[Dict[str, Any]]
    fixes_applied: List[Dict[str, Any]]
    quality_score: float
    target_quality: float
    last_updated: str
    logs: List[str]


class PDCAController:
    """
    PDCA Loop Controller for OCR improvement.
    
    This controller manages the continuous improvement cycle:
    1. PLAN: Identify issues in OCR output
    2. DO: Apply fixes and improvements
    3. CHECK: Review and validate results
    4. ACT: Standardize successful fixes
    
    State is saved after each step for crash recovery.
    """
    
    def __init__(self, workspace: str = "pdca_workspace"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # State file (survives crashes)
        self.state_file = self.workspace / "current_state.json"
        
        # Bug tracking file
        self.bugs_file = self.workspace / "bugs.json"
        
        # Log file
        self.log_file = self.workspace / "pdca.log"
        
        # Setup logging
        self._setup_logging()
        
        # Current state
        self.state: Optional[TaskState] = None
        
        self.logger.info("="*60)
        self.logger.info("PDCA Controller Initialized")
        self.logger.info(f"Workspace: {self.workspace.absolute()}")
        self.logger.info("="*60)
    
    def _setup_logging(self):
        """Setup comprehensive logging"""
        self.logger = logging.getLogger("PDCA")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(self.log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def create_task(self, task_id: str, input_file: str, 
                    target_quality: float = 0.95) -> TaskState:
        """
        Create a new PDCA task.
        
        Args:
            task_id: Unique task identifier
            input_file: Path to input PDF/image
            target_quality: Target quality score (0.0-1.0)
        
        Returns:
            TaskState object
        """
        self.logger.info(f"Creating new task: {task_id}")
        self.logger.info(f"Input file: {input_file}")
        self.logger.info(f"Target quality: {target_quality}")
        
        self.state = TaskState(
            task_id=task_id,
            input_file=input_file,
            current_state=PDCAState.PLAN.value,
            iteration=0,
            ocr_output_file=str(self.workspace / f"{task_id}_ocr.txt"),
            reviewed_output_file=str(self.workspace / f"{task_id}_reviewed.txt"),
            bugs=[],
            fixes_applied=[],
            quality_score=0.0,
            target_quality=target_quality,
            last_updated=datetime.now().isoformat(),
            logs=[]
        )
        
        self._save_state()
        self._init_bugs_file()
        
        return self.state
    
    def load_state(self) -> Optional[TaskState]:
        """
        Load state from file (for crash recovery).
        
        Returns:
            TaskState if exists, None otherwise
        """
        if not self.state_file.exists():
            self.logger.info("No saved state found")
            return None
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.state = TaskState(**data)
            self.logger.info(f"Loaded state for task: {self.state.task_id}")
            self.logger.info(f"Current PDCA phase: {self.state.current_state}")
            self.logger.info(f"Iteration: {self.state.iteration}")
            
            return self.state
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")
            return None
    
    def _save_state(self):
        """Save current state to file (called after each step)"""
        if not self.state:
            return
        
        self.state.last_updated = datetime.now().isoformat()
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.state), f, indent=2, ensure_ascii=False)
        
        self.logger.debug(f"State saved: {self.state.current_state}")
    
    def _init_bugs_file(self):
        """Initialize bugs tracking file"""
        bugs_data = {
            "task_id": self.state.task_id,
            "created_at": datetime.now().isoformat(),
            "bugs": [],
            "resolved_bugs": []
        }
        
        with open(self.bugs_file, 'w', encoding='utf-8') as f:
            json.dump(bugs_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Bugs file initialized: {self.bugs_file}")
    
    def add_bug(self, bug_type: str, description: str, 
                location: str = "", severity: str = "medium"):
        """
        Add a bug to tracking file.
        
        Args:
            bug_type: Type of bug (e.g., 'thai_vowel', 'number', 'spacing')
            description: Bug description
            location: Page/line location
            severity: low, medium, high, critical
        """
        if not self.state:
            raise RuntimeError("No active task")
        
        bug = {
            "id": f"BUG-{len(self.state.bugs) + 1:03d}",
            "type": bug_type,
            "description": description,
            "location": location,
            "severity": severity,
            "status": "open",
            "found_at": datetime.now().isoformat(),
            "fixed_at": None,
            "fix_description": None
        }
        
        self.state.bugs.append(bug)
        self._save_state()
        self._update_bugs_file(bug, "open")
        
        self.logger.warning(f"Bug added: {bug['id']} - {bug_type} ({severity})")
    
    def _update_bugs_file(self, bug: Dict, action: str):
        """Update bugs tracking file"""
        with open(self.bugs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if action == "open":
            data["bugs"].append(bug)
        elif action == "resolved":
            # Move from bugs to resolved_bugs
            for i, b in enumerate(data["bugs"]):
                if b["id"] == bug["id"]:
                    data["resolved_bugs"].append(bug)
                    data["bugs"].pop(i)
                    break
        
        with open(self.bugs_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def resolve_bug(self, bug_id: str, fix_description: str):
        """Mark a bug as resolved"""
        if not self.state:
            return
        
        for bug in self.state.bugs:
            if bug["id"] == bug_id:
                bug["status"] = "resolved"
                bug["fixed_at"] = datetime.now().isoformat()
                bug["fix_description"] = fix_description
                
                self.state.fixes_applied.append({
                    "bug_id": bug_id,
                    "fix": fix_description,
                    "applied_at": datetime.now().isoformat()
                })
                
                self._save_state()
                self._update_bugs_file(bug, "resolved")
                
                self.logger.info(f"Bug resolved: {bug_id} - {fix_description}")
                break
    
    def get_open_bugs(self) -> List[Dict]:
        """Get list of open bugs"""
        if not self.state:
            return []
        return [b for b in self.state.bugs if b["status"] == "open"]
    
    def update_quality_score(self, score: float):
        """Update current quality score"""
        if not self.state:
            return
        
        self.state.quality_score = score
        self._save_state()
        
        self.logger.info(f"Quality score updated: {score:.2%}")
    
    def next_phase(self) -> str:
        """
        Move to next PDCA phase.
        
        Returns:
            New phase name
        """
        if not self.state:
            raise RuntimeError("No active task")
        
        current = PDCAState(self.state.current_state)
        
        if current == PDCAState.PLAN:
            self.state.current_state = PDCAState.DO.value
        elif current == PDCAState.DO:
            self.state.current_state = PDCAState.CHECK.value
        elif current == PDCAState.CHECK:
            self.state.current_state = PDCAState.ACT.value
        elif current == PDCAState.ACT:
            # Check if we should continue
            self.state.iteration += 1
            open_bugs = self.get_open_bugs()
            
            if len(open_bugs) == 0 and self.state.quality_score >= self.state.target_quality:
                self.state.current_state = PDCAState.COMPLETE.value
                self.logger.info("✓ PDCA Cycle Complete - Target quality reached!")
            else:
                self.state.current_state = PDCAState.PLAN.value
                self.logger.info(f"Starting iteration {self.state.iteration + 1}")
        
        self._save_state()
        return self.state.current_state
    
    def is_complete(self) -> bool:
        """Check if PDCA cycle is complete"""
        return (self.state and 
                self.state.current_state == PDCAState.COMPLETE.value)
    
    def get_status(self) -> Dict:
        """Get current status summary"""
        if not self.state:
            return {"status": "no_task"}
        
        return {
            "task_id": self.state.task_id,
            "phase": self.state.current_state,
            "iteration": self.state.iteration,
            "quality": f"{self.state.quality_score:.2%}",
            "target": f"{self.state.target_quality:.2%}",
            "open_bugs": len(self.get_open_bugs()),
            "fixes_applied": len(self.state.fixes_applied),
            "is_complete": self.is_complete()
        }
    
    def log_action(self, action: str, details: str):
        """Log an action for dev team review"""
        if not self.state:
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": self.state.current_state,
            "iteration": self.state.iteration,
            "action": action,
            "details": details
        }
        
        self.state.logs.append(log_entry)
        self._save_state()
        
        self.logger.info(f"[{action}] {details}")


# Convenience function for running PDCA loop
def run_pdca_loop(input_file: str, task_id: str = None, 
                  target_quality: float = 0.95):
    """
    Run complete PDCA loop on a file.
    
    Args:
        input_file: Path to input PDF/image
        task_id: Optional task ID (auto-generated if not provided)
        target_quality: Target quality score
    """
    if task_id is None:
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    controller = PDCAController()
    
    # Try to load existing state (crash recovery)
    state = controller.load_state()
    
    if not state:
        # New task
        controller.create_task(task_id, input_file, target_quality)
        print(f"✓ Created new PDCA task: {task_id}")
    else:
        print(f"✓ Resumed PDCA task: {state.task_id}")
        print(f"  Phase: {state.current_state}")
        print(f"  Iteration: {state.iteration}")
        print(f"  Open bugs: {len(controller.get_open_bugs())}")
    
    # Main PDCA loop
    while not controller.is_complete():
        phase = controller.state.current_state
        iteration = controller.state.iteration
        
        print(f"\n{'='*60}")
        print(f"PDCA Phase: {phase.upper()} (Iteration {iteration})")
        print(f"{'='*60}")
        
        if phase == "plan":
            # PLAN: Identify issues
            print("\n[PLAN] Identifying OCR issues...")
            # This would be handled by AI agent
            controller.log_action("PLAN", "Identifying Thai text issues")
            controller.next_phase()
        
        elif phase == "do":
            # DO: Apply fixes
            print("\n[DO] Applying fixes...")
            # This would be handled by AI agent
            controller.log_action("DO", "Applying Thai text corrections")
            controller.next_phase()
        
        elif phase == "check":
            # CHECK: Review results
            print("\n[CHECK] Reviewing results...")
            # This would be handled by AI agent
            controller.log_action("CHECK", "Validating OCR quality")
            controller.next_phase()
        
        elif phase == "act":
            # ACT: Standardize
            print("\n[ACT] Standardizing fixes...")
            # This would be handled by AI agent
            controller.log_action("ACT", "Documenting successful fixes")
            controller.next_phase()
        
        # Print status
        status = controller.get_status()
        print(f"\nStatus: Quality={status['quality']}, " +
              f"Open Bugs={status['open_bugs']}, " +
              f"Fixes={status['fixes_applied']}")
    
    print(f"\n{'='*60}")
    print("✓ PDCA Cycle Complete!")
    print(f"{'='*60}")
    print(f"Final Quality: {controller.state.quality_score:.2%}")
    print(f"Total Iterations: {controller.state.iteration}")
    print(f"Total Fixes: {len(controller.state.fixes_applied)}")
    print(f"\nOutput files:")
    print(f"  OCR: {controller.state.ocr_output_file}")
    print(f"  Reviewed: {controller.state.reviewed_output_file}")
    print(f"  Logs: {controller.log_file}")
    print(f"  Bugs: {controller.bugs_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PDCA Loop Controller for OCR")
    parser.add_argument("input_file", help="Input PDF/image file")
    parser.add_argument("--task-id", default=None, help="Task ID")
    parser.add_argument("--quality", type=float, default=0.95, 
                       help="Target quality (0.0-1.0)")
    
    args = parser.parse_args()
    
    run_pdca_loop(args.input_file, args.task_id, args.quality)
