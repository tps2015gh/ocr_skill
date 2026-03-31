"""
PDCA Loop Package for OCR Improvement
=====================================

This package implements a Plan-Do-Check-Act (PDCA) cycle for
continuous improvement of Thai OCR text quality.

Features:
- State persistence (survives AI crashes)
- Comprehensive logging
- Bug tracking file system
- Incremental improvement loop
- Multi-agent coordination

Quick Start:
    # Run full PDCA cycle
    python pdca/team_lead_agent.py --input document.pdf --target-quality 0.95
    
    # Resume after crash
    python pdca/team_lead_agent.py --resume

Components:
- PDCAController: Manages PDCA state and workflow
- ProgrammerAgent: Applies fixes to OCR text
- TeamLeadAgent: Coordinates the full cycle
"""

from .pdca_controller import PDCAController, PDCAState, TaskState
from .programmer_agent import ProgrammerAgent
from .team_lead_agent import TeamLeadAgent

__all__ = [
    'PDCAController',
    'PDCAState',
    'TaskState',
    'ProgrammerAgent',
    'TeamLeadAgent',
]

__version__ = '1.0.0'
