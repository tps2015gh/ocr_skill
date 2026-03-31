# AI Agent PDCA Guide

## 🎯 Purpose

Guide for **AI agents** to continuously improve OCR Skill through PDCA cycles.

---

## 🚀 Quick Start (AI Agents)

```python
# Import tools
from ai_tools import PDCATools
from skill import process_file

# Initialize
tools = PDCATools()

# Plan week (Tech Lead agent)
tools.plan_week(
    focus="Thai numeral conversion",
    tasks=["Add converter", "Write tests"],
    goals=["Improve accuracy 5%"]
)

# Apply fixes (Developer agent)
fixed = tools.apply_all_fixes(text)

# Test quality (QA agent)
quality = tools.calculate_quality(text)
```

---

## 👥 Agent Roles

### Tech Lead Agent
```python
from ai_tools import PDCATools
tools = PDCATools()

# Check status
tools.status()

# Plan week
tools.plan_week(focus, tasks, goals)

# Review week
tools.review_week("87%", "92%", "+5%")
```

### Developer Agent
```python
from ai_tools import PDCATools
tools = PDCATools()

# Apply Thai fixes
fixed = tools.apply_all_fixes(text, show_progress=True)

# Specific fixes
fixed = tools.thai_numerals_fix(text)
fixed = tools.thai_vowels_fix(text)
fixed = tools.thai_tone_marks_fix(text)
fixed = tools.legal_terms_fix(text)
```

### QA Agent
```python
from ai_tools import PDCATools
tools = PDCATools()

# Test single file
result = tools.test_document("output_txt/doc.txt")

# Batch test
results = tools.batch_test("output_txt")

# Compare
comparison = tools.compare_outputs("before.txt", "after.txt")
```

---

## 📁 Project Structure

```
ocr_skill/
├── ai_tools/           # AI agent tools
│   ├── __init__.py
│   ├── dev_tools.py    # PDCATools class
│   └── PDCA_LOOP.md    # This guide
├── skill/              # OCR skill package
│   ├── __init__.py
│   └── ocr_skill/      # OCR processor
├── input_pdf/          # Input files
├── output_txt/         # OCR output
└── output_md/          # Markdown output
```

---

## 🔄 PDCA Cycle (AI Agents)

```
1. PLAN  → Tech Lead: tools.plan_week()
2. DO    → Developer: tools.apply_all_fixes()
3. CHECK → QA: tools.calculate_quality()
4. ACT   → Tech Lead: tools.review_week()
```

---

## 💡 Token Efficiency

**DO:**
```python
# Reuse tools
from ai_tools import PDCATools
tools = PDCATools()
fixed = tools.apply_all_fixes(text)
```

**DON'T:**
```python
# Don't reimplement
def fix_thai_numerals(text):
    thai_nums = {'๑':'1', ...}  # Wastes tokens
```

---

**Version:** 5.0.0 (AI Agent Focus)
