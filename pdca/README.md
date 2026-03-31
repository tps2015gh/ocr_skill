# PDCA Loop for OCR Improvement

## Overview

This PDCA (Plan-Do-Check-Act) system provides **continuous improvement** for Thai OCR text quality with **crash recovery** support.

---

## 🔄 What is PDCA?

**PDCA Cycle:**
1. **PLAN** - Identify OCR issues and bugs
2. **DO** - Apply targeted fixes
3. **CHECK** - Review and validate results
4. **ACT** - Standardize successful fixes

The cycle repeats until target quality is reached.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Crash Recovery** | State saved after each step - next AI can continue |
| **Comprehensive Logging** | All actions logged for dev team review |
| **Bug Tracking** | JSON-based bug tracking file |
| **Incremental Updates** | Fix by fix improvement |
| **Quality Metrics** | Automated quality scoring |
| **Multi-Agent** | Team Lead + Programmer coordination |

---

## 📁 Files Created

```
pdca_workspace/
├── current_state.json      # Task state (crash recovery)
├── bugs.json               # Bug tracking file
├── pdca.log                # Comprehensive log file
├── fix_patterns.json       # Successful fix patterns
├── {task_id}_ocr.txt       # Initial OCR output
├── {task_id}_reviewed.txt  # Reviewed/fixed output
└── {task_id}_report.json   # Final report
```

---

## 🚀 Quick Start

### Run Full PDCA Cycle

```bash
# Basic usage
python pdca/team_lead_agent.py --input document.pdf --target-quality 0.95

# With custom task ID
python pdca/team_lead_agent.py --input document.pdf --task-id my_task_001

# Limit iterations
python pdca/team_lead_agent.py --input document.pdf --max-iterations 5
```

### Resume After Crash

```bash
# Resume latest task
python pdca/team_lead_agent.py --resume

# Resume specific task
python pdca/team_lead_agent.py --task-id my_task_001 --resume
```

---

## 📊 Usage Examples

### Example 1: Basic Usage

```bash
# Process a Thai document
python pdca/team_lead_agent.py --input input_pdf/contract.pdf

# Output:
# ✓ Started task: task_20260331_143022
# Starting PDCA improvement cycle...
# Target quality: 95.00%
# Max iterations: 10
#
# ============================================================
# PDCA Cycle 1 - Phase: PLAN
# ============================================================
# [PLAN] Analyzing OCR output for issues...
# Identified 5 issues
#
# ============================================================
# PDCA Cycle 1 - Phase: DO
# ============================================================
# [DO] Applying fixes...
# Fixes applied: 3
# Quality: 87.50%
# ...
```

### Example 2: Programmatic Usage

```python
from pdca import TeamLeadAgent

# Initialize
team_lead = TeamLeadAgent()

# Start task
task = team_lead.start_task(
    input_file="document.pdf",
    task_id="thai_doc_001",
    target_quality=0.95
)

# Run PDCA cycle
result = team_lead.run_pdca_cycle(max_iterations=10)

# Check results
print(f"Final Quality: {result['final_quality']}")
print(f"Total Fixes: {result['total_fixes']}")
print(f"Output: {result['output_files']['reviewed']}")
```

### Example 3: Crash Recovery

```python
from pdca import PDCAController

# Load existing state (after crash)
controller = PDCAController()
state = controller.load_state()

if state:
    print(f"Resumed task: {state.task_id}")
    print(f"Phase: {state.current_state}")
    print(f"Open bugs: {len(controller.get_open_bugs())}")
    
    # Continue from where it stopped
    # ... continue processing
```

---

## 🔧 Components

### PDCAController

Manages the PDCA state and workflow.

```python
from pdca import PDCAController

controller = PDCAController()

# Create task
state = controller.create_task(
    task_id="task_001",
    input_file="doc.pdf",
    target_quality=0.95
)

# Add bug
controller.add_bug(
    bug_type="thai_vowel",
    description="Vowel confusion detected",
    location="page 3, line 15",
    severity="medium"
)

# Resolve bug
controller.resolve_bug("BUG-001", "Applied vowel correction")

# Update quality
controller.update_quality_score(0.92)

# Move to next phase
next_phase = controller.next_phase()
```

### ProgrammerAgent

Applies fixes to OCR text.

```python
from pdca import ProgrammerAgent, PDCAController

controller = PDCAController()
programmer = ProgrammerAgent(controller)

# Analyze bugs
bugs = programmer.analyze_bugs()

# Apply fix
with open("ocr_output.txt", 'r', encoding='utf-8') as f:
    text = f.read()

fixed_text, success = programmer.apply_fix(bugs[0], text)

# Calculate quality
quality = programmer.calculate_quality(fixed_text)
```

### TeamLeadAgent

Coordinates the full PDCA cycle.

```python
from pdca import TeamLeadAgent

team_lead = TeamLeadAgent()

# Start task
task = team_lead.start_task("document.pdf")

# Run cycle
result = team_lead.run_pdca_cycle(max_iterations=10)

# Get report
print(f"Status: {result['status']}")
print(f"Final Quality: {result['final_quality']}")
```

---

## 📝 Log File Format

The `pdca.log` file contains timestamped entries:

```
2026-03-31 14:30:22 - PDCA - INFO - ============================================================
2026-03-31 14:30:22 - PDCA - INFO - PDCA Controller Initialized
2026-03-31 14:30:22 - PDCA - INFO - ============================================================
2026-03-31 14:30:23 - PDCA - INFO - Creating new task: task_001
2026-03-31 14:30:23 - PDCA - INFO - Input file: document.pdf
2026-03-31 14:30:23 - PDCA - INFO - Target quality: 0.95
2026-03-31 14:30:24 - PDCA - WARNING - Bug added: BUG-001 - thai_vowel (medium)
2026-03-31 14:30:25 - PDCA - INFO - [PLAN] Identifying Thai text issues
2026-03-31 14:30:26 - PDCA - INFO - [DO] Applying Thai text corrections
2026-03-31 14:30:27 - PDCA - INFO - Bug resolved: BUG-001 - Applied vowel correction
```

---

## 🐛 Bug Tracking File Format

The `bugs.json` file tracks all bugs:

```json
{
  "task_id": "task_001",
  "created_at": "2026-03-31T14:30:23",
  "bugs": [
    {
      "id": "BUG-001",
      "type": "thai_vowel",
      "description": "Thai vowels detected - may need context-based correction",
      "location": "page 2",
      "severity": "medium",
      "status": "open",
      "found_at": "2026-03-31T14:30:24",
      "fixed_at": null,
      "fix_description": null
    }
  ],
  "resolved_bugs": []
}
```

---

## 🎯 State File Format

The `current_state.json` file enables crash recovery:

```json
{
  "task_id": "task_001",
  "input_file": "document.pdf",
  "current_state": "do",
  "iteration": 2,
  "ocr_output_file": "pdca_workspace/task_001_ocr.txt",
  "reviewed_output_file": "pdca_workspace/task_001_reviewed.txt",
  "bugs": [...],
  "fixes_applied": [...],
  "quality_score": 0.87,
  "target_quality": 0.95,
  "last_updated": "2026-03-31T14:35:00",
  "logs": [...]
}
```

---

## 🛠️ Customization

### Add Custom Fix Patterns

Edit `programmer_agent.py`:

```python
def _load_thai_patterns(self) -> Dict:
    return {
        # Add your custom patterns
        'custom': {
            'wrong_pattern': 'correct_pattern',
        }
    }
```

### Add Bug Types

Edit `programmer_agent.apply_fix()`:

```python
if bug['type'] == 'my_custom_type':
    fixed_text, success = self._fix_custom_type(fixed_text, bug)
```

### Adjust Quality Scoring

Edit `programmer_agent.calculate_quality()`:

```python
def calculate_quality(self, text: str) -> float:
    score = 1.0
    
    # Add your custom scoring logic
    # ...
    
    return max(0.0, min(1.0, score))
```

---

## 📊 Quality Metrics

Quality score (0.0-1.0) is calculated based on:

| Factor | Impact |
|--------|--------|
| OCR errors | -10% each |
| Multiple spaces | -2% each |
| Unrecognized chars | -5% each |
| Unknown sequences | -3% each |
| Thai script consistency | +5% bonus |

---

## ⚠️ Troubleshooting

### Task Not Found

```
Error: No active task
```

**Solution:** Start a new task with `--input`

### Crash Recovery Not Working

```
Error: Failed to load state
```

**Solution:** Check `pdca_workspace/current_state.json` exists and is valid JSON

### Quality Not Improving

**Solution:** 
1. Check `bugs.json` for open bugs
2. Review `pdca.log` for fix failures
3. Add custom fix patterns for your document type

---

## 📚 Related Documentation

- Main README: `README.md`
- Deployment Guide: `DEPLOYMENT.md`
- Advanced OCR: `ADVANCED_OCR.md`
- Agent CLI Integration: `AGENT_CLI_INTEGRATION.md`

---

**Version:** 1.0.0  
**Last Updated:** March 31, 2026
