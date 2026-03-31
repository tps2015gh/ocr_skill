"""
Temp Work Generator - Continuous Agent Tasks
=============================================

Generates continuous tasks for AI agents to do.
Run this to see agents moving on the dashboard in real-time.

Usage:
    python ai_tools/temp_work.py
    
Then watch: http://localhost:8000
"""

import sys
import time
import random
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_tools import PDCATools


# Task definitions for each agent
TECH_LEAD_TASKS = [
    ("Planning sprint", "plan_week"),
    ("Reviewing code", "review_week"),
    ("Updating roadmap", "plan_week"),
    ("Meeting with team", "review_week"),
]

DEVELOPER_TASKS = [
    ("Writing feature", "write_code"),
    ("Fixing bug #123", "fix_bug"),
    ("Refactoring code", "write_code"),
    ("Adding tests", "write_code"),
    ("Debugging issue", "fix_bug"),
]

QA_TASKS = [
    ("Testing feature", "test_quality"),
    ("Running tests", "test_quality"),
    ("Verifying fix", "test_quality"),
    ("Quality check", "test_quality"),
]


def generate_temp_work(duration_seconds: int = 60):
    """
    Generate continuous work for all agents.
    
    Args:
        duration_seconds: How long to generate work (default: 60 seconds)
    """
    print("\n" + "="*60)
    print("🔄 TEMP WORK GENERATOR")
    print("="*60)
    print(f"Generating work for {duration_seconds} seconds...")
    print(f"Watch dashboard at: http://localhost:8000")
    print("="*60 + "\n")
    
    tools = PDCATools()
    
    start_time = time.time()
    iteration = 0
    
    try:
        while time.time() - start_time < duration_seconds:
            iteration += 1
            
            # Tech Lead work
            task_name, task_id = random.choice(TECH_LEAD_TASKS)
            print(f"[{iteration}] 🎯 Tech Lead: {task_name}")
            tools._log_activity("Tech Lead", "working", task_name, task_id)
            
            # Developer work
            task_name, task_id = random.choice(DEVELOPER_TASKS)
            print(f"[{iteration}] 💻 Developer: {task_name}")
            tools._log_activity("Developer", "working", task_name, task_id)
            
            # QA work
            task_name, task_id = random.choice(QA_TASKS)
            print(f"[{iteration}] ✅ QA: {task_name}")
            tools._log_activity("QA", "working", task_name, task_id)
            
            # Wait a bit before next task
            time.sleep(2)
            
            # Mark tasks as complete and return to rest
            print(f"[{iteration}] 😴 Agents returning to rest...")
            tools._log_activity("Tech Lead", "resting", "Resting", "")
            tools._log_activity("Developer", "resting", "Resting", "")
            tools._log_activity("QA", "resting", "Resting", "")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    
    print(f"\n✓ Generated {iteration} iterations of work")
    print("Check dashboard for agent activities!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate temp work for agents')
    parser.add_argument('--duration', type=int, default=60,
                       help='Duration in seconds (default: 60)')
    
    args = parser.parse_args()
    
    generate_temp_work(args.duration)


if __name__ == "__main__":
    main()
