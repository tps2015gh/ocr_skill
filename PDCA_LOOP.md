# PDCA Loop Guide for Thai OCR Improvement

## 🎯 Purpose

This guide enables AI agents to continuously improve Thai OCR text quality through a **Plan-Do-Check-Act (PDCA)** cycle. Each AI agent can pick up where the previous one left off.

---

## 📋 Agent Roles

### 1. **Manager Agent** (Team Lead)
**Responsibilities:**
- Read this guide and current state
- Coordinate improvement cycle
- Decide when to stop
- Update state file

**Tools Available:**
- `ocr_skill` - For OCR processing
- This state file for progress tracking

---

### 2. **Programmer Agent** (OCR Specialist)
**Responsibilities:**
- Analyze OCR errors
- Apply Thai text fixes
- Improve quality score

**Skills:**
- Thai language understanding
- OCR error pattern recognition
- Text correction

---

### 3. **QA Agent** (Quality Assurance)
**Responsibilities:**
- Review fixed text
- Calculate quality score
- Identify remaining issues

**Checklist:**
- [ ] Thai vowels correct?
- [ ] Tone marks correct?
- [ ] Numbers formatted?
- [ ] Spacing proper?
- [ ] No OCR errors?

---

## 🔄 PDCA Cycle Steps

### Step 1: PLAN (Manager Agent)

**Read Current State:**
```
1. Open pdca_state.json
2. Check current_phase
3. Check iteration count
4. Review open_bugs
```

**Tasks:**
- [ ] Load current state (or create new)
- [ ] Review bugs from previous iteration
- [ ] Identify new issues
- [ ] Set priorities
- [ ] Update state: `current_phase = "do"`

**Example State Creation:**
```json
{
  "task_id": "thai_doc_001",
  "input_file": "input_pdf/document.pdf",
  "current_phase": "plan",
  "iteration": 1,
  "target_quality": 0.95,
  "current_quality": 0.0,
  "open_bugs": [],
  "fixes_applied": [],
  "logs": []
}
```

---

### Step 2: DO (Programmer Agent)

**Read Bug List:**
```
1. Open pdca_state.json
2. Read open_bugs array
3. Sort by priority
```

**Apply Fixes:**
```python
from ocr_skill import process_file
from ocr_skill.skill import OCRSkill

# Load OCR output
with open('output_txt/document.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Apply Thai text fixes
fixed_text = apply_thai_fixes(text, bugs)

# Save fixed version
with open('pdca_reviewed.txt', 'w', encoding='utf-8') as f:
    f.write(fixed_text)
```

**Common Thai Fixes:**
```python
def apply_thai_fixes(text, bugs):
    # 1. Fix vowel confusion
    text = re.sub(r'กระ(?!ร)', 'กระ', text)
    
    # 2. Fix tone marks
    text = re.sub(r'([ก-ฮ])่้', r'\1้', text)
    
    # 3. Fix Thai numerals → Arabic
    thai_nums = {'๑':'1','๒':'2','๓':'3','๔':'4','๕':'5',
                 '๖':'6','๗':'7','๘':'8','๙':'9','๐':'0'}
    for thai, arabic in thai_nums.items():
        text = text.replace(thai, arabic)
    
    # 4. Fix spacing
    text = re.sub(r'  +', ' ', text)
    
    # 5. Fix word boundaries
    text = text.replace('ประ เทศ', 'ประเทศ')
    text = text.replace('กรม ที่ ดิน', 'กรมที่ดิน')
    
    return text
```

**Update State:**
- [ ] Log fixes applied
- [ ] Mark bugs as resolved
- [ ] Update state: `current_phase = "check"`

---

### Step 3: CHECK (QA Agent)

**Calculate Quality:**
```python
def calculate_quality(text):
    score = 1.0
    
    # Deduct for errors
    if '[OCR Error' in text:
        score -= 0.1
    if re.search(r'  +', text):
        score -= 0.02
    if '???' in text:
        score -= 0.05
    
    # Bonus for Thai consistency
    thai_chars = len(re.findall(r'[\u0E00-\u0E7F]', text))
    if thai_chars > len(text) * 0.3:
        score += 0.05
    
    return max(0.0, min(1.0, score))
```

**Review Checklist:**
- [ ] Read `pdca_reviewed.txt`
- [ ] Calculate quality score
- [ ] Compare with target_quality
- [ ] Identify remaining issues
- [ ] Add new bugs if found

**Decision:**
```
IF quality >= target AND open_bugs == 0:
    → Move to ACT (finalize)
ELSE:
    → Move to PLAN (next iteration)
```

**Update State:**
- [ ] Update current_quality
- [ ] Update state: `current_phase = "act"` or `"plan"`

---

### Step 4: ACT (Manager Agent)

**If Quality Reached:**
- [ ] Mark task as complete
- [ ] Generate final report
- [ ] Save to `pdca_report.json`
- [ ] Update state: `current_phase = "complete"`

**If More Work Needed:**
- [ ] Increment iteration counter
- [ ] Document successful fixes
- [ ] Update state: `current_phase = "plan"`
- [ ] Next AI continues from here

**Final Report:**
```json
{
  "task_id": "thai_doc_001",
  "status": "complete",
  "final_quality": 0.96,
  "target_quality": 0.95,
  "total_iterations": 3,
  "total_fixes": 15,
  "output_file": "pdca_reviewed.txt",
  "completed_at": "2026-03-31T15:30:00"
}
```

---

## 📁 State File Format

**File:** `pdca_state.json`

```json
{
  "task_id": "thai_doc_001",
  "input_file": "input_pdf/document.pdf",
  "current_phase": "do",
  "iteration": 2,
  "target_quality": 0.95,
  "current_quality": 0.87,
  "open_bugs": [
    {
      "id": "BUG-003",
      "type": "thai_vowel",
      "description": "Vowel confusion in กระทรวง",
      "severity": "medium",
      "found_iteration": 2
    }
  ],
  "fixes_applied": [
    {
      "bug_id": "BUG-001",
      "fix": "Converted Thai numerals to Arabic",
      "applied_iteration": 1
    }
  ],
  "logs": [
    {
      "timestamp": "2026-03-31T14:30:00",
      "agent": "Manager",
      "action": "Started PDCA cycle",
      "phase": "plan"
    }
  ],
  "output_files": {
    "ocr": "output_txt/document.txt",
    "reviewed": "pdca_reviewed.txt"
  }
}
```

---

## 🐛 Bug Types

| Type | Description | Severity | Fix Pattern |
|------|-------------|----------|-------------|
| `thai_vowel` | Vowel confusion | medium | Context-based correction |
| `tone_mark` | Wrong tone mark | medium | Grammar rules |
| `number` | Thai vs Arabic numerals | low | Direct replacement |
| `spacing` | Extra/missing spaces | low | Regex cleanup |
| `word_boundary` | Incorrectly split words | medium | Dictionary lookup |
| `ocr_error` | OCR engine errors | high | Re-OCR or manual fix |

---

## 🚀 Quick Start

### For Manager Agent

```bash
# 1. Create initial state
echo '{
  "task_id": "task_001",
  "input_file": "input_pdf/doc.pdf",
  "current_phase": "plan",
  "iteration": 1,
  "target_quality": 0.95,
  "current_quality": 0.0,
  "open_bugs": [],
  "fixes_applied": [],
  "logs": []
}' > pdca_state.json

# 2. Run initial OCR
python src/ocr_processor.py

# 3. Start PDCA cycle
# Follow PLAN → DO → CHECK → ACT loop
```

### For Programmer Agent

```bash
# 1. Read state
cat pdca_state.json

# 2. Check open bugs
# 3. Apply fixes using ocr_skill
python -c "
from ocr_skill import process_file
result = process_file('input_pdf/doc.pdf')
text = result.get_all_text()
# Apply fixes to text
"

# 4. Update state
```

### For QA Agent

```bash
# 1. Read reviewed output
cat pdca_reviewed.txt

# 2. Calculate quality
# 3. Compare with target
# 4. Update state with quality score
```

---

## 💡 Tips for AI Agents

### Minimizing Token Usage

1. **Read only relevant sections** of state file
2. **Use ocr_skill** instead of re-implementing OCR
3. **Log only essential actions**
4. **Reference this guide** instead of re-explaining

### Crash Recovery

1. **Always read `pdca_state.json` first**
2. **Continue from `current_phase`**
3. **Check `iteration` count**
4. **Review `logs` for context**

### When to Stop

- ✅ Quality >= target_quality
- ✅ No open bugs
- ✅ Max iterations reached (default: 10)
- ✅ No more improvements possible

---

## 📊 Example PDCA Session

```
Iteration 1:
- PLAN: Found 5 bugs (3 Thai vowels, 2 spacing)
- DO: Fixed 3 bugs
- CHECK: Quality = 0.82 (target: 0.95)
- ACT: Continue to iteration 2

Iteration 2:
- PLAN: 2 remaining bugs + 1 new issue
- DO: Fixed all 3 bugs
- CHECK: Quality = 0.94 (target: 0.95)
- ACT: Continue to iteration 3

Iteration 3:
- PLAN: Minor tone mark issue
- DO: Fixed tone mark
- CHECK: Quality = 0.96 (target: 0.95) ✓
- ACT: Task complete!
```

---

## 📝 Log Entry Format

```json
{
  "timestamp": "2026-03-31T14:30:00",
  "agent": "Manager",
  "role": "Team Lead",
  "action": "Started PDCA cycle",
  "phase": "plan",
  "iteration": 1,
  "details": "Initial OCR completed, 5 bugs identified"
}
```

---

**Version:** 1.0.0  
**Last Updated:** March 31, 2026  
**Next Agent:** Read `pdca_state.json` and continue from `current_phase`
