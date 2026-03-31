# PDCA Loop Guide for Complex Thai OCR Improvement

## 🎯 Purpose

This guide enables AI agents to continuously improve **Complex Thai OCR** text quality through a **Plan-Do-Check-Act (PDCA)** cycle. Each AI agent can pick up where the previous one left off.

**Target:** Complex Thai documents with:
- Mixed Thai-English text
- Tables and forms
- Legal/government terminology
- Thai numerals and special characters
- Complex vowel and tone mark combinations

---

## 📋 Agent Roles & Tasks

### 1. **Manager Agent** (Team Lead) 🎯

**Mission:** Coordinate the PDCA improvement cycle for complex Thai OCR

---

#### **Tasks:**

**Task 1.1: Initialize Task**
```bash
# Create state file
{
  "task_id": "thai_complex_001",
  "input_file": "input_pdf/legal_doc.pdf",
  "document_type": "thai_legal",
  "current_phase": "plan",
  "iteration": 1,
  "target_quality": 0.95,
  "current_quality": 0.0,
  "complexity_flags": {
    "has_tables": false,
    "has_english": false,
    "has_thai_numerals": false,
    "has_legal_terms": false
  },
  "open_bugs": [],
  "fixes_applied": [],
  "logs": []
}
```

**Task 1.2: Review Current State**
```bash
# Read pdca_state.json
cat pdca_state.json

# Check:
- current_phase (plan/do/check/act/complete)
- iteration count
- open_bugs count
- current_quality vs target_quality
```

**Task 1.3: Coordinate Agents**
```
IF phase == "plan":
    → Assign bug identification to Programmer
    → Set priority for complex Thai issues
    
ELSE IF phase == "do":
    → Monitor Programmer progress
    → Track fixes applied
    
ELSE IF phase == "check":
    → Assign QA review
    → Compare quality vs target
    
ELSE IF phase == "act":
    → Decide: continue or finalize
    → Document successful patterns
```

**Task 1.4: Update State**
```python
# After each phase, update state
state["current_phase"] = next_phase
state["logs"].append({
    "timestamp": datetime.now().isoformat(),
    "agent": "Manager",
    "action": action,
    "phase": current_phase,
    "iteration": iteration
})
save_state(state)
```

**Task 1.5: Decision Making**
```python
# Stop conditions
IF current_quality >= target_quality AND len(open_bugs) == 0:
    → Mark complete
    → Generate report
    
ELSE IF iteration >= max_iterations (10):
    → Mark stopped
    → Document remaining issues
    
ELSE:
    → Continue to next iteration
```

---

### 2. **Programmer Agent** (Thai OCR Specialist) 💻

**Mission:** Apply targeted fixes for complex Thai text issues

---

#### **Tasks:**

**Task 2.1: Read Bug List**
```bash
# Load state
with open('pdca_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# Get open bugs
bugs = state['open_bugs']

# Sort by priority (critical > high > medium > low)
priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
bugs.sort(key=lambda x: priority_order.get(x['severity'], 1), reverse=True)
```

**Task 2.2: Analyze Thai OCR Output**
```bash
# Read OCR output
with open(state['output_files']['ocr'], 'r', encoding='utf-8') as f:
    text = f.read()

# Analyze for complex Thai issues
analysis = {
    'thai_vowel_issues': len(re.findall(r'[ะัาิีุูเแโใไ]', text)),
    'tone_mark_issues': len(re.findall(r'[่้๊๋]', text)),
    'thai_numerals': len(re.findall(r'[๑๒๓๔๕๖๗๘๙๐]', text)),
    'spacing_issues': len(re.findall(r'  +', text)),
    'mixed_lang_issues': len(re.findall(r'[a-zA-Z]+[\u0E00-\u0E7F]+|[a-zA-Z]+', text)),
    'legal_terms': check_legal_terms(text)
}
```

**Task 2.3: Apply Thai-Specific Fixes**

**Fix 2.3.1: Thai Vowel Corrections**
```python
def fix_thai_vowels(text):
    """Fix common Thai vowel OCR errors"""
    fixes = [
        # Short/long vowel pairs
        (r'กระ(?!ร)', 'กระ'),  # Common prefix
        (r'จะ(?!ก)', 'จะ'),    # Common word
        (r'อะไร', 'อะไร'),      # What
        
        # Confused vowels
        (r'([ก-ฮ])ั้', r'\1้ำ'),  # Double vowel fix
        (r'([ก-ฮ])ี้', r'\1ี้'),  # Long i + tone
        
        # Common misrecognitions
        (r'เé', 'เé'),  # e + accent
        (r'แé', 'แé'),  # ae + accent
    ]
    
    for pattern, replacement in fixes:
        text = re.sub(pattern, replacement, text)
    
    return text
```

**Fix 2.3.2: Tone Mark Corrections**
```python
def fix_tone_marks(text):
    """Fix Thai tone mark stacking errors"""
    fixes = [
        # Remove double tone marks
        (r'([ก-ฮ])่้', r'\1้'),
        (r'([ก-ฮ])้่', r'\1้'),
        (r'([ก-ฮ])้๊', r'\1้'),
        (r'([ก-ฮ])้๋', r'\1้'),
        
        # Correct tone order
        (r'([ก-ฮ])([่้๊๋])([่้๊๋])', r'\1\2'),
    ]
    
    for pattern, replacement in fixes:
        text = re.sub(pattern, replacement, text)
    
    return text
```

**Fix 2.3.3: Thai Numeral Conversion**
```python
def fix_thai_numerals(text, convert_to_arabic=True):
    """Convert Thai numerals to Arabic (or vice versa)"""
    if convert_to_arabic:
        thai_to_arabic = {
            '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5',
            '๖': '6', '๗': '7', '๘': '8', '๙': '9', '๐': '0'
        }
        for thai, arabic in thai_to_arabic.items():
            text = text.replace(thai, arabic)
    return text
```

**Fix 2.3.4: Legal/Government Terms**
```python
def fix_legal_terms(text):
    """Fix common Thai legal/government term OCR errors"""
    legal_terms = {
        # Government
        'กรม ที่ ดิน': 'กรมที่ดิน',
        'กระทรวง มหาดไทย': 'กระทรวงมหาดไทย',
        'ราช การ': 'ราชการ',
        
        # Legal
        'สัญญา จ้าง': 'สัญญาจ้าง',
        'ข้อ ตกลง': 'ข้อตกลง',
        'คู่ สัญญา': 'คู่สัญญา',
        
        # Formal
        'ด้วย เหตุนี้': 'ด้วยเหตุนี้',
        'จึง ใคร่': 'จึงใคร่',
        'ยัง มิ': 'ยังมิ',
    }
    
    for wrong, correct in legal_terms.items():
        text = text.replace(wrong, correct)
    
    return text
```

**Fix 2.3.5: Mixed Thai-English**
```python
def fix_mixed_language(text):
    """Fix spacing issues in mixed Thai-English text"""
    # Add space between Thai and English
    text = re.sub(r'([\u0E00-\u0E7F])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])([\u0E00-\u0E7F])', r'\1 \2', text)
    
    # Remove space within English words
    text = re.sub(r'([a-zA-Z]) ([a-zA-Z])', r'\1\2', text)
    
    return text
```

**Task 2.4: Save Fixed Output**
```python
# Save reviewed/fixed version
with open('pdca_reviewed.txt', 'w', encoding='utf-8') as f:
    f.write(fixed_text)

# Log fixes applied
state['fixes_applied'].append({
    'iteration': state['iteration'],
    'fixes': fix_list,
    'timestamp': datetime.now().isoformat()
})

# Update state
state['current_phase'] = 'check'
save_state(state)
```

---

### 3. **QA Agent** (Quality Assurance) ✅

**Mission:** Review and validate Thai OCR quality

---

#### **Tasks:**

**Task 3.1: Load Reviewed Text**
```bash
# Read reviewed output
with open('pdca_reviewed.txt', 'r', encoding='utf-8') as f:
    text = f.read()
```

**Task 3.2: Calculate Quality Score**
```python
def calculate_thai_quality(text):
    """Calculate quality score for Thai OCR text"""
    score = 1.0
    
    # Deductions
    
    # 1. OCR errors (critical)
    ocr_errors = len(re.findall(r'\[OCR Error', text))
    score -= min(ocr_errors * 0.1, 0.3)
    
    # 2. Unknown sequences
    unknown = len(re.findall(r'\?\?\?', text))
    score -= min(unknown * 0.03, 0.15)
    
    # 3. Spacing issues
    spacing = len(re.findall(r'  +', text))
    score -= min(spacing * 0.01, 0.1)
    
    # 4. Thai vowel consistency
    # Check for common vowel confusion patterns
    vowel_issues = len(re.findall(r'[ะัา][ิีุู]', text))
    score -= min(vowel_issues * 0.02, 0.1)
    
    # 5. Tone mark stacking (error)
    tone_stack = len(re.findall(r'[่้๊๋]{2,}', text))
    score -= min(tone_stack * 0.05, 0.15)
    
    # Bonuses
    
    # 1. Thai script consistency
    thai_chars = len(re.findall(r'[\u0E00-\u0E7F]', text))
    thai_ratio = thai_chars / max(len(text), 1)
    if thai_ratio > 0.3:
        score += 0.05
    
    # 2. Legal term accuracy
    legal_terms_present = check_legal_terms_accuracy(text)
    if legal_terms_present > 0.9:
        score += 0.05
    
    # 3. Numeral consistency
    numeral_check = check_numeral_consistency(text)
    if numeral_check:
        score += 0.03
    
    return max(0.0, min(1.0, score))
```

**Task 3.3: Thai-Specific Quality Checks**
```python
def check_thai_quality_detailed(text):
    """Detailed Thai OCR quality checks"""
    checks = {
        'vowel_accuracy': True,
        'tone_accuracy': True,
        'numeral_format': True,
        'spacing_correct': True,
        'legal_terms_correct': True,
        'mixed_lang_correct': True,
    }
    
    # Check vowel stacking (error)
    if re.search(r'[ะัาิีุู]{2,}', text):
        checks['vowel_accuracy'] = False
    
    # Check tone mark stacking (error)
    if re.search(r'[่้๊๋]{2,}', text):
        checks['tone_accuracy'] = False
    
    # Check numeral consistency
    thai_nums = len(re.findall(r'[๑๒๓๔๕๖๗๘๙๐]', text))
    arabic_nums = len(re.findall(r'[1234567890]', text))
    if thai_nums > 0 and arabic_nums > 0:
        checks['numeral_format'] = False  # Mixed formats
    
    # Check spacing
    if re.search(r'  +', text):
        checks['spacing_correct'] = False
    
    # Check legal terms
    legal_errors = [
        'กรม ที่ ดิน',  # Should be กรมที่ดิน
        'กระทรวง มหาดไทย',  # Should be กระทรวงมหาดไทย
    ]
    for error in legal_errors:
        if error in text:
            checks['legal_terms_correct'] = False
    
    return checks
```

**Task 3.4: Identify Remaining Issues**
```python
def identify_remaining_issues(text, state):
    """Identify issues that still need fixing"""
    issues = []
    
    # Check for uncorrected Thai vowels
    if re.search(r'[ะัา][ิีุู]', text):
        issues.append({
            'type': 'thai_vowel',
            'description': 'Vowel stacking detected',
            'severity': 'medium',
            'location': 'throughout'
        })
    
    # Check for tone mark errors
    if re.search(r'[่้๊๋]{2,}', text):
        issues.append({
            'type': 'tone_mark',
            'description': 'Tone mark stacking detected',
            'severity': 'high',
            'location': 'throughout'
        })
    
    # Check for Thai numerals (if should be Arabic)
    thai_nums = re.findall(r'[๑๒๓๔๕๖๗๘๙๐]', text)
    if len(thai_nums) > 5:
        issues.append({
            'type': 'number',
            'description': f'Found {len(thai_nums)} Thai numerals',
            'severity': 'low',
            'location': 'throughout'
        })
    
    # Check for legal term errors
    legal_errors = check_legal_terms(text)
    if legal_errors:
        issues.append({
            'type': 'legal_term',
            'description': f'Legal term errors: {legal_errors}',
            'severity': 'high',
            'location': 'specific'
        })
    
    return issues
```

**Task 3.5: Update State with Quality**
```python
# Calculate quality
quality = calculate_thai_quality(text)
state['current_quality'] = quality

# Add new bugs if found
new_issues = identify_remaining_issues(text, state)
for issue in new_issues:
    issue['id'] = f"BUG-{len(state['open_bugs']) + 1:03d}"
    issue['found_iteration'] = state['iteration']
    issue['status'] = 'open'
    state['open_bugs'].append(issue)

# Decision
if quality >= state['target_quality'] and len(state['open_bugs']) == 0:
    state['current_phase'] = 'act'  # Finalize
else:
    state['current_phase'] = 'plan'  # Continue

save_state(state)
```

---

## 🔄 Complete PDCA Flow for Complex Thai

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLEX THAI OCR PDCA                     │
│                                                              │
│  ┌────────────┐                                             │
│  │ MANAGER    │                                             │
│  │ PLAN Phase │                                             │
│  │ - Create task                                           │
│  │ - Set target (0.95)                                     │
│  │ - Identify complexity                                   │
│  └─────┬──────┘                                             │
│        │                                                     │
│        ▼                                                     │
│  ┌────────────┐                                             │
│  │ PROGRAMMER │                                             │
│  │ DO Phase   │                                             │
│  │ - Fix Thai vowels                                       │
│  │ - Fix tone marks                                        │
│  │ - Convert numerals                                      │
│  │ - Fix legal terms                                       │
│  └─────┬──────┘                                             │
│        │                                                     │
│        ▼                                                     │
│  ┌────────────┐                                             │
│  │ QA         │                                             │
│  │ CHECK Phase│                                             │
│  │ - Calculate quality                                     │
│  │ - Check Thai specifics                                  │
│  │ - Identify remaining                                    │
│  └─────┬──────┘                                             │
│        │                                                     │
│        ▼                                                     │
│  ┌────────────┐                                             │
│  │ MANAGER    │                                             │
│  │ ACT Phase  │                                             │
│  │ - Quality >= 0.95?                                      │
│  │ - Bugs = 0?                                             │
│  │ - Continue or Stop                                      │
│  └─────┬──────┘                                             │
│        │                                                     │
│        └──────────────┐                                     │
│                       │                                     │
│        IF continue ←──┘                                     │
│        IF stop → Finalize                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Complex Thai Issue Priority

| Issue Type | Severity | Priority | Fix By |
|------------|----------|----------|--------|
| Tone mark stacking | Critical | 10 | Programmer |
| Legal term errors | High | 8 | Programmer |
| Thai vowel confusion | High | 7 | Programmer |
| Mixed language spacing | Medium | 5 | Programmer |
| Thai numerals | Low | 3 | Programmer |
| Minor spacing | Low | 2 | Programmer |

---

## 📁 State File for Complex Thai

```json
{
  "task_id": "thai_complex_001",
  "input_file": "input_pdf/legal_contract.pdf",
  "document_type": "thai_legal",
  "current_phase": "do",
  "iteration": 2,
  "target_quality": 0.95,
  "current_quality": 0.87,
  "complexity_flags": {
    "has_tables": true,
    "has_english": true,
    "has_thai_numerals": true,
    "has_legal_terms": true
  },
  "open_bugs": [
    {
      "id": "BUG-005",
      "type": "legal_term",
      "description": "กรม ที่ ดิน should be กรมที่ดิน",
      "severity": "high",
      "found_iteration": 2,
      "status": "open"
    }
  ],
  "fixes_applied": [
    {
      "iteration": 1,
      "fixes": [
        "Converted 15 Thai numerals to Arabic",
        "Fixed 8 tone mark stacking errors",
        "Corrected 3 legal terms"
      ],
      "timestamp": "2026-03-31T15:30:00"
    }
  ],
  "logs": [
    {
      "timestamp": "2026-03-31T15:00:00",
      "agent": "Manager",
      "action": "Started PDCA cycle",
      "phase": "plan",
      "iteration": 1
    }
  ],
  "output_files": {
    "ocr": "output_txt/legal_contract.txt",
    "reviewed": "pdca_reviewed.txt"
  }
}
```

---

## 🚀 Quick Start for Complex Thai

### Manager Agent Starts:
```bash
# 1. Create state for complex Thai
{
  "task_id": "thai_complex_001",
  "input_file": "input_pdf/legal_doc.pdf",
  "document_type": "thai_legal",
  "current_phase": "plan",
  "iteration": 1,
  "target_quality": 0.95,
  "current_quality": 0.0,
  "open_bugs": [],
  "fixes_applied": [],
  "logs": []
} > pdca_state.json

# 2. Run initial OCR
python src/ocr_processor.py

# 3. Begin PDCA cycle
```

### Programmer Agent Continues:
```bash
# 1. Read state
cat pdca_state.json

# 2. Apply Thai-specific fixes
python -c "
from ocr_skill import process_file
result = process_file('input_pdf/legal_doc.pdf')
text = result.get_all_text()

# Apply complex Thai fixes
text = fix_thai_vowels(text)
text = fix_tone_marks(text)
text = fix_legal_terms(text)

with open('pdca_reviewed.txt', 'w', encoding='utf-8') as f:
    f.write(text)
"

# 3. Update state
```

### QA Agent Reviews:
```bash
# 1. Calculate Thai quality
python -c "
quality = calculate_thai_quality(open('pdca_reviewed.txt').read())
print(f'Quality: {quality:.2%}')
"

# 2. Update state with quality score
# 3. Identify remaining issues
```

---

**Version:** 2.0.0 (Complex Thai Focus)  
**Last Updated:** March 31, 2026  
**Next Agent:** Read `pdca_state.json` and continue from `current_phase`
