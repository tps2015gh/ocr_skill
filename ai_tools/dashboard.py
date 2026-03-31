"""
Agent Dashboard - Monitor AI Agent Activities
==============================================

Simple dashboard to monitor what each AI agent is doing.

Usage:
    python ai_tools/dashboard.py      # Show dashboard
    python ai_tools/dashboard.py live # Live monitoring
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class AgentDashboard:
    """Dashboard to monitor AI agent activities"""
    
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
                "weeks": [],
                "agent_activities": []
            }
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_log(self):
        """Save pdca_log.json"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def log_agent_action(self, agent: str, action: str, details: str = ""):
        """Log an agent action"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "details": details
        }
        
        if "agent_activities" not in self.state:
            self.state["agent_activities"] = []
        
        self.state["agent_activities"].append(activity)
        
        # Keep last 100 activities
        if len(self.state["agent_activities"]) > 100:
            self.state["agent_activities"] = self.state["agent_activities"][-100:]
        
        self._save_log()
    
    def show(self):
        """Show dashboard"""
        print("\n" + "="*70)
        print("🤖 AI AGENT DASHBOARD - OCR Skill Project")
        print("="*70)
        print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Project Overview
        print("\n📊 PROJECT OVERVIEW")
        print("-"*70)
        print(f"Project: {self.state.get('project', 'N/A')}")
        print(f"Started: {self.state.get('start_date', 'N/A')}")
        print(f"Total Weeks: {len(self.state.get('weeks', []))}")
        
        # Current Week Status
        weeks = self.state.get("weeks", [])
        if weeks:
            current = weeks[-1]
            print(f"\n📅 CURRENT WEEK ({current.get('week', 'N/A')})")
            print("-"*70)
            print(f"Focus: {current.get('focus', 'N/A')}")
            print(f"Status: {current.get('status', 'N/A')}")
            print(f"Start: {current.get('start_date', 'N/A')}")
            
            if "end_date" in current:
                print(f"End: {current['end_date']}")
            
            # Tasks
            tasks = current.get("tasks", [])
            if tasks:
                print(f"\nTasks ({len(tasks)}):")
                for task in tasks:
                    status_icon = "✓" if task.get("status") == "done" else "○"
                    print(f"  {status_icon} {task.get('task', 'N/A')}")
            
            # Results
            if "results" in current:
                r = current["results"]
                print(f"\nResults:")
                print(f"  Quality: {r.get('quality_before', 'N/A')} → {r.get('quality_after', 'N/A')}")
                print(f"  Improvement: {r.get('improvement', 'N/A')}")
        
        # Agent Activities
        print(f"\n🤖 AGENT ACTIVITIES")
        print("-"*70)
        
        activities = self.state.get("agent_activities", [])
        
        if not activities:
            print("No agent activities logged yet.")
            print("\nAgents can log actions with:")
            print("  dashboard.log_agent_action('Tech Lead', 'plan_week', 'Week 1 planned')")
            print("  dashboard.log_agent_action('Developer', 'apply_fixes', 'Thai numerals fixed')")
            print("  dashboard.log_agent_action('QA', 'test_output', 'Quality: 92%')")
        else:
            # Group by agent
            agents = {}
            for activity in activities:
                agent = activity.get("agent", "Unknown")
                if agent not in agents:
                    agents[agent] = []
                agents[agent].append(activity)
            
            for agent, agent_activities in agents.items():
                print(f"\n{self._get_agent_icon(agent)} {agent} ({len(agent_activities)} actions)")
                
                # Show last 5 activities
                for activity in agent_activities[-5:]:
                    ts = activity.get("timestamp", "")[:16].replace("T", " ")
                    action = activity.get("action", "")
                    details = activity.get("details", "")
                    print(f"  [{ts}] {action}: {details}")
        
        # File Status
        print(f"\n📁 OUTPUT FILES STATUS")
        print("-"*70)
        
        output_txt = Path("output_txt")
        output_md = Path("output_md")
        
        if output_txt.exists():
            txt_files = list(output_txt.glob("*.txt"))
            print(f"output_txt/: {len(txt_files)} files")
            for f in txt_files[-3:]:
                size = f.stat().st_size / 1024
                print(f"  - {f.name} ({size:.1f} KB)")
        
        if output_md.exists():
            md_files = list(output_md.glob("*.md"))
            print(f"output_md/: {len(md_files)} files")
        
        # Quick Stats
        print(f"\n⚡ QUICK STATS")
        print("-"*70)
        
        if activities:
            # Most active agent
            agent_counts = {}
            for activity in activities:
                agent = activity.get("agent", "Unknown")
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
            
            if agent_counts:
                most_active = max(agent_counts, key=agent_counts.get)
                print(f"Most Active Agent: {most_active} ({agent_counts[most_active]} actions)")
            
            # Last activity
            last = activities[-1]
            print(f"Last Activity: {last.get('timestamp', 'N/A')[:16].replace('T', ' ')}")
            print(f"  Agent: {last.get('agent', 'N/A')}")
            print(f"  Action: {last.get('action', 'N/A')}")
        
        print("\n" + "="*70)
        print("Commands:")
        print("  python ai_tools/dashboard.py        - Show dashboard")
        print("  python ai_tools/dashboard.py live   - Live monitoring")
        print("  python ai_tools/dashboard.py clear  - Clear activity log")
        print("\nAgent Logging:")
        print("  dashboard.log_agent_action('Tech Lead', 'plan_week', 'Week 1 planned')")
        print("  dashboard.log_agent_action('Developer', 'apply_fixes', 'Thai numerals fixed')")
        print("  dashboard.log_agent_action('QA', 'calculate_quality', 'Quality: 92%')")
        print("="*70 + "\n")
    
    def _get_agent_icon(self, agent: str) -> str:
        """Get emoji icon for agent"""
        icons = {
            "Tech Lead": "🎯",
            "Developer": "💻",
            "QA": "✅",
            "Batch": "📦"
        }
        return icons.get(agent, "🤖")
    
    def live_monitor(self):
        """Live monitoring mode"""
        import time
        
        print("🔴 LIVE MONITORING MODE")
        print("Press Ctrl+C to stop\n")
        
        last_count = len(self.state.get("agent_activities", []))
        
        try:
            while True:
                time.sleep(2)
                
                # Reload log
                self.state = self._load_log()
                current_count = len(self.state.get("agent_activities", []))
                
                if current_count > last_count:
                    # New activity
                    new_activities = self.state["agent_activities"][last_count:]
                    
                    for activity in new_activities:
                        ts = activity.get("timestamp", "")[:16].replace("T", " ")
                        agent = activity.get("agent", "Unknown")
                        action = activity.get("action", "")
                        details = activity.get("details", "")
                        
                        icon = self._get_agent_icon(agent)
                        print(f"[{ts}] {icon} {agent}: {action} - {details}")
                    
                    last_count = current_count
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped live monitoring")
    
    def clear_log(self):
        """Clear activity log"""
        confirm = input("Clear all agent activities? (y/n): ")
        if confirm.lower() == 'y':
            self.state["agent_activities"] = []
            self._save_log()
            print("✓ Activity log cleared")
        else:
            print("✗ Cancelled")


def main():
    dashboard = AgentDashboard()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "live":
            dashboard.live_monitor()
        elif cmd == "clear":
            dashboard.clear_log()
        else:
            print(f"Unknown command: {cmd}")
    else:
        dashboard.show()


if __name__ == "__main__":
    main()
