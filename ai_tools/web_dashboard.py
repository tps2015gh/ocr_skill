"""
Agent Dashboard Web App - Real-time Agent Monitoring
=====================================================

Simple web dashboard to see AI agents working in real-time.

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
        
        return {
            "agents": {
                "Tech Lead": {"status": "idle", "x": 50, "y": 50, "task": "", "last_update": ""},
                "Developer": {"status": "idle", "x": 50, "y": 50, "task": "", "last_update": ""},
                "QA": {"status": "idle", "x": 50, "y": 50, "task": "", "last_update": ""}
            },
            "nodes": [
                {"id": "plan", "name": "PLAN", "x": 100, "y": 100, "color": "#3498db"},
                {"id": "do", "name": "DO", "x": 300, "y": 100, "color": "#e74c3c"},
                {"id": "check", "name": "CHECK", "x": 300, "y": 300, "color": "#f1c40f"},
                {"id": "act", "name": "ACT", "x": 100, "y": 300, "color": "#2ecc71"}
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
            json.dump(self.data, f, indent=2)
    
    def update_agent(self, agent: str, status: str, task: str = "", node: str = ""):
        """Update agent status and position"""
        if agent not in self.data["agents"]:
            self.data["agents"][agent] = {"status": "idle", "x": 50, "y": 50, "task": "", "last_update": ""}
        
        # Find node position
        if node:
            for n in self.data["nodes"]:
                if n["id"] == node:
                    self.data["agents"][agent]["x"] = n["x"]
                    self.data["agents"][agent]["y"] = n["y"]
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
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_html().encode('utf-8'))
        
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dashboard.get_data()).encode('utf-8'))
        
        elif self.path == '/api/update':
            # Parse query params
            from urllib.parse import parse_qs, urlparse
            params = parse_qs(urlparse(self.path).query)
            
            agent = params.get('agent', ['Unknown'])[0]
            status = params.get('status', ['idle'])[0]
            task = params.get('task', [''])[0]
            node = params.get('node', [''])[0]
            
            dashboard.update_agent(agent, status, task, node)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        
        else:
            super().do_GET()


def get_html():
    """Generate dashboard HTML"""
    return '''<!DOCTYPE html>
<html>
<head>
    <title>🤖 AI Agent Dashboard</title>
    <meta http-equiv="refresh" content="2">
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
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 20px;
        }
        .visualization {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            position: relative;
            height: 500px;
        }
        .node {
            position: absolute;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .node:hover { transform: scale(1.1); }
        .agent {
            position: absolute;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            transition: all 1s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            border: 3px solid #fff;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .agent-status {
            position: absolute;
            bottom: -25px;
            font-size: 0.7em;
            white-space: nowrap;
            background: rgba(0,0,0,0.7);
            padding: 2px 8px;
            border-radius: 10px;
        }
        .agent-task {
            position: absolute;
            top: -25px;
            font-size: 0.6em;
            white-space: nowrap;
            background: rgba(0,0,0,0.7);
            padding: 2px 8px;
            border-radius: 10px;
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .side-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .panel {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
        }
        .panel h2 {
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
        }
        .agent-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .agent-icon {
            font-size: 2em;
            width: 50px;
            text-align: center;
        }
        .agent-info { flex: 1; }
        .agent-name { font-weight: bold; margin-bottom: 5px; }
        .agent-status-text {
            font-size: 0.85em;
            color: #888;
        }
        .status-idle { color: #888; }
        .status-working { color: #2ecc71; }
        .status-busy { color: #f39c12; }
        .log-entry {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.85em;
        }
        .log-time { color: #888; margin-right: 10px; }
        .log-agent { font-weight: bold; margin-right: 10px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .stat-card {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }
        .controls {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .controls button {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-size: 0.9em;
        }
        .controls button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Agent Dashboard</h1>
        <p class="subtitle">Real-time monitoring of AI agents improving OCR Skill</p>
        
        <div class="dashboard">
            <div class="visualization" id="vis">
                <!-- Nodes -->
                <div class="node" id="node-plan" style="left: 100px; top: 100px; background: #3498db;">PLAN</div>
                <div class="node" id="node-do" style="left: 300px; top: 100px; background: #e74c3c;">DO</div>
                <div class="node" id="node-check" style="left: 300px; bottom: 100px; background: #f1c40f;">CHECK</div>
                <div class="node" id="node-act" style="left: 100px; bottom: 100px; background: #2ecc71;">ACT</div>
                
                <!-- Agents will be added here -->
            </div>
            
            <div class="side-panel">
                <div class="panel">
                    <h2>📊 Statistics</h2>
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
                    <h2>👥 Agents</h2>
                    <div id="agents-list">
                        <!-- Agent cards will be added here -->
                    </div>
                </div>
                
                <div class="panel">
                    <h2>📝 Activity Log</h2>
                    <div id="log-list" style="max-height: 300px; overflow-y: auto;">
                        <!-- Log entries will be added here -->
                    </div>
                </div>
                
                <div class="controls">
                    <h3>🎮 Test Controls</h3>
                    <button onclick="simulateAgent('Tech Lead', 'Planning week', 'plan')">Simulate Tech Lead</button>
                    <button onclick="simulateAgent('Developer', 'Applying fixes', 'do')">Simulate Developer</button>
                    <button onclick="simulateAgent('QA', 'Testing quality', 'check')">Simulate QA</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const agentIcons = {
            "Tech Lead": "🎯",
            "Developer": "💻",
            "QA": "✅"
        };
        
        function updateDashboard() {
            fetch('/api/data')
                .then(r => r.json())
                .then(data => {
                    // Update agents visualization
                    const vis = document.getElementById('vis');
                    
                    // Remove old agents
                    document.querySelectorAll('.agent').forEach(e => e.remove());
                    
                    // Add agents
                    for (const [name, info] of Object.entries(data.agents)) {
                        const agent = document.createElement('div');
                        agent.className = 'agent';
                        agent.style.left = (info.x - 30) + 'px';
                        agent.style.top = (info.y - 30) + 'px';
                        agent.style.background = getStatusColor(info.status);
                        agent.innerHTML = `
                            ${agentIcons[name] || '🤖'}
                            <div class="agent-task">${info.task}</div>
                            <div class="agent-status">${info.status} • ${info.last_update}</div>
                        `;
                        vis.appendChild(agent);
                    }
                    
                    // Update stats
                    document.getElementById('stat-actions').textContent = data.stats.total_actions;
                    document.getElementById('stat-week').textContent = data.stats.current_week || 0;
                    document.getElementById('stat-quality').textContent = data.stats.quality || '0%';
                    
                    // Update agents list
                    const agentsList = document.getElementById('agents-list');
                    agentsList.innerHTML = '';
                    for (const [name, info] of Object.entries(data.agents)) {
                        agentsList.innerHTML += `
                            <div class="agent-card">
                                <div class="agent-icon">${agentIcons[name] || '🤖'}</div>
                                <div class="agent-info">
                                    <div class="agent-name">${name}</div>
                                    <div class="agent-status-text status-${info.status}">${info.status} • ${info.task}</div>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Update log
                    const logList = document.getElementById('log-list');
                    logList.innerHTML = '';
                    data.log.slice(0, 20).forEach(entry => {
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
        
        function simulateAgent(agent, task, node) {
            fetch(`/api/update?agent=${encodeURIComponent(agent)}&status=working&task=${encodeURIComponent(task)}&node=${node}`)
                .then(r => r.json())
                .then(() => {
                    setTimeout(() => {
                        fetch(`/api/update?agent=${encodeURIComponent(agent)}&status=idle&task=Done!&node=${node}`);
                    }, 2000);
                });
        }
        
        // Initial update and auto-refresh
        updateDashboard();
        setInterval(updateDashboard, 2000);
    </script>
</body>
</html>
'''


def run_server(port=8000):
    """Run dashboard server"""
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"\n{'='*60}")
    print(f"🤖 AI Agent Dashboard")
    print(f"{'='*60}")
    print(f"\nOpening dashboard at: http://localhost:{port}")
    print(f"\nPress Ctrl+C to stop\n")
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  Dashboard stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
