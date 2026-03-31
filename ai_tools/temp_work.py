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
import urllib.request
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

DESIGNER_TASKS = [
    ("Designing UI", "write_code"),
    ("Creating mockup", "write_code"),
    ("Reviewing design", "review_week"),
    ("Fixing UX issue", "fix_bug"),
]

DEVOPS_TASKS = [
    ("Deploying app", "write_code"),
    ("Fixing pipeline", "fix_bug"),
    ("Monitoring logs", "test_quality"),
    ("Scaling servers", "write_code"),
]


def update_agent_position(agent: str, status: str, task: str, task_id: str = ""):
    """Directly update agent position on dashboard via API"""
    try:
        if status in ['resting', 'idle']:
            url = f"http://localhost:8000/api/update?agent={agent}&status={status}&task={task}"
        else:
            url = f"http://localhost:8000/api/update?agent={agent}&status={status}&task={task}&task_id={task_id}"
        
        urllib.request.urlopen(url, timeout=2)
        return True
    except Exception as e:
        print(f"  ⚠️ Dashboard update failed: {e}")
        return False


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
    
    # Test dashboard connection
    print("📡 Connecting to dashboard...")
    if not update_agent_position("Tech Lead", "resting", "Resting"):
        print("❌ Dashboard not responding!")
        print("   Start dashboard first: python ai_tools/web_dashboard.py")
        return
    print("✓ Dashboard connected!\n")
    
    start_time = time.time()
    iteration = 0
    
    try:
        while time.time() - start_time < duration_seconds:
            iteration += 1
            
            # Tech Lead work
            task_name, task_id = random.choice(TECH_LEAD_TASKS)
            print(f"[{iteration}] 🎯 Tech Lead: {task_name}")
            update_agent_position("Tech Lead", "working", task_name, task_id)
            
            # Developer work
            task_name, task_id = random.choice(DEVELOPER_TASKS)
            print(f"[{iteration}] 💻 Developer: {task_name}")
            update_agent_position("Developer", "working", task_name, task_id)
            
            # QA work
            task_name, task_id = random.choice(QA_TASKS)
            print(f"[{iteration}] ✅ QA: {task_name}")
            update_agent_position("QA", "working", task_name, task_id)
            
            # Designer work
            task_name, task_id = random.choice(DESIGNER_TASKS)
            print(f"[{iteration}] 🎨 Designer: {task_name}")
            update_agent_position("Designer", "working", task_name, task_id)
            
            # DevOps work
            task_name, task_id = random.choice(DEVOPS_TASKS)
            print(f"[{iteration}] ⚙️ DevOps: {task_name}")
            update_agent_position("DevOps", "working", task_name, task_id)
            
            # Wait while working
            time.sleep(3)
            
            # Mark tasks as complete and return to rest
            print(f"[{iteration}] 😴 Agents returning to rest...")
            update_agent_position("Tech Lead", "resting", "Resting")
            update_agent_position("Developer", "resting", "Resting")
            update_agent_position("QA", "resting", "Resting")
            update_agent_position("Designer", "resting", "Resting")
            update_agent_position("DevOps", "resting", "Resting")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    
    # Return all to rest
    update_agent_position("Tech Lead", "resting", "Resting")
    update_agent_position("Developer", "resting", "Resting")
    update_agent_position("QA", "resting", "Resting")
    
    print(f"\n✓ Generated {iteration} iterations of work")
    print("Agents returned to rest area!")


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
