"""
Agent Dashboard Web App - Task-based Real-time Monitoring
==========================================================

Web dashboard showing agents moving between task tables.

Usage:
    python ai_tools/web_dashboard.py
    
Then open: http://localhost:8000
"""

import os
import sys
import json
import threading
import time
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

# Dashboard data file
DASHBOARD_DATA = Path("dashboard_data.json")


class DashboardData:
    """Manage dashboard data"""
    
    def __init__(self):
        self.data = self._load()
    
    def _load(self):
        """Load dashboard data"""
        if DASHBOARD_DATA.exists():
            with open(DASHBOARD_DATA, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        import random
        # Random starting positions for each agent
        positions = [
            {"x": 80, "y": 350},
            {"x": 550, "y": 350},
            {"x": 300, "y": 380}
        ]
        random.shuffle(positions)
        
        return {
            "agents": {
                "Tech Lead": {"status": "idle", "x": positions[0]["x"], "y": positions[0]["y"], "task": "", "last_update": ""},
                "Developer": {"status": "idle", "x": positions[1]["x"], "y": positions[1]["y"], "task": "", "last_update": ""},
                "QA": {"status": "idle", "x": positions[2]["x"], "y": positions[2]["y"], "task": "", "last_update": ""}
            },
            "tasks": [
                {"id": "plan_week", "name": "1. Plan Week", "x": 100, "y": 80, "color": "#3498db", "queue": 0},
                {"id": "write_code", "name": "2. Write Code", "x": 280, "y": 80, "color": "#e74c3c", "queue": 0},
                {"id": "test_quality", "name": "3. Test Quality", "x": 460, "y": 80, "color": "#f1c40f", "queue": 0},
                {"id": "review_week", "name": "4. Review Week", "x": 190, "y": 200, "color": "#2ecc71", "queue": 0},
                {"id": "fix_bug", "name": "5. Fix Bug", "x": 370, "y": 200, "color": "#9b59b6", "queue": 0}
            ],
            "log": [],
            "stats": {
                "total_actions": 0,
                "current_week": 0,
                "quality": "0%"
            }
        }
    
    def _save(self):
        """Save dashboard data"""
        with open(DASHBOARD_DATA, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def update_agent(self, agent: str, status: str, task: str = "", task_id: str = ""):
        """Update agent status and position"""
        if agent not in self.data["agents"]:
            self.data["agents"][agent] = {"status": "idle", "x": 50, "y": 50, "task": "", "last_update": ""}
        
        # Find task position
        if task_id:
            for t in self.data["tasks"]:
                if t["id"] == task_id:
                    self.data["agents"][agent]["x"] = t["x"]
                    self.data["agents"][agent]["y"] = t["y"]
                    
                    # Update queue count
                    if status == "working":
                        t["queue"] = t.get("queue", 0) + 1
                    else:
                        t["queue"] = max(0, t.get("queue", 0) - 1)
                    break
        
        self.data["agents"][agent]["status"] = status
        self.data["agents"][agent]["task"] = task
        self.data["agents"][agent]["last_update"] = datetime.now().strftime("%H:%M:%S")
        
        # Add to log
        self.data["log"].insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent,
            "status": status,
            "task": task
        })
        
        # Keep last 50 logs
        if len(self.data["log"]) > 50:
            self.data["log"] = self.data["log"][:50]
        
        self.data["stats"]["total_actions"] += 1
        self._save()
    
    def get_data(self):
        """Get current dashboard data"""
        return self.data


# Global dashboard instance
dashboard = DashboardData()


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler for dashboard"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html().encode('utf-8'))
        
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(dashboard.get_data(), ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/update':
            # Parse query params
            from urllib.parse import parse_qs, urlparse
            params = parse_qs(urlparse(self.path).query)
            
            agent = params.get('agent', ['Unknown'])[0]
            status = params.get('status', ['idle'])[0]
            task = params.get('task', [''])[0]
            task_id = params.get('task_id', [''])[0]
            
            dashboard.update_agent(agent, status, task, task_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}, ensure_ascii=False).encode('utf-8'))
        
        else:
            super().do_GET()


def get_html():
    """Generate dashboard HTML"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>AI Agent Dashboard</title>
    <meta http-equiv="refresh" content="2">
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .workflow-arrow {
            position: absolute;
            font-size: 1.5em;
            color: #666;
            opacity: 0.5;
        }
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 20px;
        }
        .visualization {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            position: relative;
            height: 400px;
        }
        .task-table {
            position: absolute;
            width: 180px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            border: 2px solid;
            transition: all 0.3s ease;
        }
        .task-table:hover { transform: scale(1.05); }
        .task-name {
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .task-queue {
            font-size: 0.75em;
            color: #888;
        }
        .agent {
            position: absolute;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            transition: all 1s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            border: 3px solid #fff;
            animation: pulse 2s infinite;
            z-index: 10;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .agent-label {
            position: absolute;
            bottom: -20px;
            font-size: 0.6em;
            white-space: nowrap;
            background: rgba(0,0,0,0.7);
            padding: 2px 6px;
            border-radius: 8px;
        }
        .side-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .panel {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 15px;
        }
        .panel h2 {
            margin-bottom: 12px;
            font-size: 1.2em;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            padding-bottom: 8px;
        }
        .agent-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .agent-icon {
            font-size: 1.8em;
            width: 45px;
            text-align: center;
        }
        .agent-info { flex: 1; }
        .agent-name { font-weight: bold; margin-bottom: 3px; font-size: 0.95em; }
        .agent-status-text {
            font-size: 0.8em;
            color: #888;
        }
        .status-idle { color: #888; }
        .status-working { color: #2ecc71; }
        .status-busy { color: #f39c12; }
        .log-entry {
            padding: 6px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.8em;
        }
        .log-time { color: #888; margin-right: 8px; font-size: 0.9em; }
        .log-agent { font-weight: bold; margin-right: 8px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }
        .stat-card {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            font-size: 0.7em;
            color: #888;
            margin-top: 4px;
        }
        .controls {
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .controls h3 {
            font-size: 1em;
            margin-bottom: 10px;
        }
        .controls button {
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            margin: 4px;
            font-size: 0.8em;
            width: 100%;
        }
        .controls button:hover { background: #2980b9; }
        .task-list {
            max-height: 200px;
            overflow-y: auto;
        }
        .task-item {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .task-color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .task-info { flex: 1; }
        .task-label { font-weight: bold; font-size: 0.9em; }
        .task-queue-count { font-size: 0.75em; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Agent Dashboard</h1>
        <p class="subtitle">Real-time monitoring of AI agents improving OCR Skill</p>
        
        <div class="dashboard">
            <div class="visualization" id="vis">
                <!-- Workflow arrows -->
                <div class="workflow-arrow" style="left: 220px; top: 60px;">→</div>
                <div class="workflow-arrow" style="left: 400px; top: 60px;">→</div>
                <div class="workflow-arrow" style="left: 380px; top: 140px;">↘</div>
                <div class="workflow-arrow" style="left: 260px; top: 140px;">↙</div>
                
                <!-- Task tables -->
                <div class="task-table" id="task-plan_week" style="left: 10px; top: 60px; border-color: #3498db;">
                    <div class="task-name">1. Plan Week</div>
                    <div class="task-queue">0 in queue</div>
                </div>
                <div class="task-table" id="task-write_code" style="left: 190px; top: 60px; border-color: #e74c3c;">
                    <div class="task-name">2. Write Code</div>
                    <div class="task-queue">0 in queue</div>
                </div>
                <div class="task-table" id="task-test_quality" style="left: 370px; top: 60px; border-color: #f1c40f;">
                    <div class="task-name">3. Test Quality</div>
                    <div class="task-queue">0 in queue</div>
                </div>
                <div class="task-table" id="task-review_week" style="left: 100px; top: 180px; border-color: #2ecc71;">
                    <div class="task-name">4. Review Week</div>
                    <div class="task-queue">0 in queue</div>
                </div>
                <div class="task-table" id="task-fix_bug" style="left: 280px; top: 180px; border-color: #9b59b6;">
                    <div class="task-name">5. Fix Bug</div>
                    <div class="task-queue">0 in queue</div>
                </div>
                
                <!-- Agents will be added here -->
            </div>
            
            <div class="side-panel">
                <div class="panel">
                    <h2>Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value" id="stat-actions">0</div>
                            <div class="stat-label">Actions</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="stat-week">0</div>
                            <div class="stat-label">Week</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="stat-quality">0%</div>
                            <div class="stat-label">Quality</div>
                        </div>
                    </div>
                </div>
                
                <div class="panel">
                    <h2>Tasks</h2>
                    <div class="task-list" id="task-list">
                        <!-- Task items will be added here -->
                    </div>
                </div>
                
                <div class="panel">
                    <h2>Agents</h2>
                    <div id="agents-list">
                        <!-- Agent cards will be added here -->
                    </div>
                </div>
                
                <div class="panel">
                    <h2>Activity Log</h2>
                    <div id="log-list" style="max-height: 200px; overflow-y: auto;">
                        <!-- Log entries will be added here -->
                    </div>
                </div>
                
                <div class="controls">
                    <h3>Simulate Agents</h3>
                    <button onclick="simulateAgent('Tech Lead', 'Planning week', 'plan_week')">🎯 Tech Lead: Plan Week</button>
                    <button onclick="simulateAgent('Developer', 'Writing code', 'write_code')">💻 Developer: Write Code</button>
                    <button onclick="simulateAgent('QA', 'Testing quality', 'test_quality')">✅ QA: Test Quality</button>
                    <button onclick="simulateAgent('Tech Lead', 'Reviewing results', 'review_week')">📊 Tech Lead: Review</button>
                    <button onclick="simulateAgent('Developer', 'Fixing bug', 'fix_bug')">🐛 Developer: Fix Bug</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const agentIcons = {
            "Tech Lead": "\\u{1F3AF}",
            "Developer": "\\u{1F4BB}",
            "QA": "\\u{2705}"
        };
        
        function updateDashboard() {
            console.log('Updating dashboard...');
            fetch('/api/data?t=' + new Date().getTime())
                .then(r => r.json())
                .then(data => {
                    console.log('Data received:', data);
                    
                    // Update task queue counts
                    data.tasks.forEach(task => {
                        const table = document.getElementById('task-' + task.id);
                        if (table) {
                            const queueEl = table.querySelector('.task-queue');
                            if (queueEl) {
                                queueEl.textContent = (task.queue || 0) + ' working';
                            }
                        }
                    });
                    
                    // Remove old agents
                    document.querySelectorAll('.agent').forEach(e => e.remove());
                    
                    // Add agents
                    for (const [name, info] of Object.entries(data.agents)) {
                        const agent = document.createElement('div');
                        agent.className = 'agent';
                        agent.style.left = (info.x - 25) + 'px';
                        agent.style.top = (info.y - 25) + 'px';
                        agent.style.background = getStatusColor(info.status);
                        agent.innerHTML = `
                            ${agentIcons[name] || '\\u{1F916}'}
                            <div class="agent-label">${name}</div>
                        `;
                        document.getElementById('vis').appendChild(agent);
                    }
                    
                    // Update stats
                    document.getElementById('stat-actions').textContent = data.stats.total_actions;
                    document.getElementById('stat-week').textContent = data.stats.current_week || 0;
                    document.getElementById('stat-quality').textContent = data.stats.quality || '0%';
                    
                    // Update task list
                    const taskList = document.getElementById('task-list');
                    taskList.innerHTML = '';
                    data.tasks.forEach(task => {
                        taskList.innerHTML += `
                            <div class="task-item">
                                <div class="task-color" style="background: ${task.color}"></div>
                                <div class="task-info">
                                    <div class="task-label">${task.name}</div>
                                    <div class="task-queue-count">${task.queue || 0} working</div>
                                </div>
                            </div>
                        `;
                    });
                    
                    // Update agents list
                    const agentsList = document.getElementById('agents-list');
                    agentsList.innerHTML = '';
                    for (const [name, info] of Object.entries(data.agents)) {
                        agentsList.innerHTML += `
                            <div class="agent-card">
                                <div class="agent-icon">${agentIcons[name] || '\\u{1F916}'}</div>
                                <div class="agent-info">
                                    <div class="agent-name">${name}</div>
                                    <div class="agent-status-text status-${info.status}">${info.status} &bull; ${info.task || 'No task'}</div>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Update log
                    const logList = document.getElementById('log-list');
                    logList.innerHTML = '';
                    data.log.slice(0, 15).forEach(entry => {
                        logList.innerHTML += `
                            <div class="log-entry">
                                <span class="log-time">${entry.time}</span>
                                <span class="log-agent">${entry.agent}</span>
                                <span>${entry.task}</span>
                            </div>
                        `;
                    });
                });
        }
        
        function getStatusColor(status) {
            if (status === 'working') return '#2ecc71';
            if (status === 'busy') return '#f39c12';
            return '#95a5a6';
        }
        
        function simulateAgent(agent, task, taskId) {
            fetch(`/api/update?agent=${encodeURIComponent(agent)}&status=working&task=${encodeURIComponent(task)}&task_id=${taskId}`)
                .then(r => r.json())
                .then(() => {
                    setTimeout(() => {
                        fetch(`/api/update?agent=${encodeURIComponent(agent)}&status=idle&task=Done!&task_id=${taskId}`);
                    }, 2000);
                });
        }
        
        // Initial update and auto-refresh
        updateDashboard();
        setInterval(updateDashboard, 2000);
    </script>
</body>
</html>"""
    return html


def run_server(port=8000):
    """Run dashboard server"""
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"\\n{'='*60}")
    print(f"AI Agent Dashboard")
    print(f"{'='*60}")
    print(f"\\nOpening dashboard at: http://localhost:{port}")
    print(f"\\nPress Ctrl+C to stop\\n")
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n\\nDashboard stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
