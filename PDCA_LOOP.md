# Dev Team PDCA Guide - Continuous Product Improvement

## 🎯 Purpose

This guide helps a **small development team** continuously improve the OCR Skill product through **Plan-Do-Check-Act** cycles.

**Think of it as:** A small company with 3 developers, each with specific roles, working together to make the product better over time.

---

## 👥 Team Roles

### 1. Tech Lead (Manager)

**Who:** Senior developer / Team lead

**Responsibilities:**
- Review project status
- Prioritize issues
- Assign tasks
- Review pull requests
- Decide when to release

**Files to check:**
- `README.md` - Product documentation
- `pdca_log.json` - Progress tracking
- GitHub Issues - User feedback

---

### 2. Developer (Programmer)

**Who:** Core developer

**Responsibilities:**
- Fix bugs
- Implement improvements
- Write tests
- Update code
- Document changes

**Files to work on:**
- `ocr_skill/` - Main package
- `src/` - Core processor
- `examples/` - Usage examples

---

### 3. QA Engineer (Tester)

**Who:** Quality assurance developer

**Responsibilities:**
- Test new features
- Verify bug fixes
- Check documentation
- Test on real documents
- Report issues

**Files to check:**
- `output_txt/` - OCR results
- `output_md/` - Markdown results
- Test documents in `input_pdf/`

---

## 🔄 PDCA Cycle (Weekly Sprint)

### Week 1 Example

#### Monday - PLAN (Tech Lead)

**Task:** Review and plan improvements

```bash
# 1. Check current status
git log --oneline -10
git status

# 2. Review last week's progress
cat pdca_log.json

# 3. Identify areas to improve
# Example findings:
# - Thai numeral conversion needed
# - Legal terms not handled well
# - Documentation outdated
```

**Update pdca_log.json:**
```json
{
  "week": 1,
  "start_date": "2026-03-31",
  "focus": "Thai text improvements",
  "tasks": [
    {
      "id": 1,
      "task": "Add Thai numeral conversion",
      "assigned_to": "Developer",
      "status": "todo"
    },
    {
      "id": 2,
      "task": "Fix legal term handling",
      "assigned_to": "Developer",
      "status": "todo"
    },
    {
      "id": 3,
      "task": "Test on 5 Thai documents",
      "assigned_to": "QA",
      "status": "todo"
    }
  ],
  "goals": [
    "Improve Thai OCR accuracy by 5%",
    "Add numeral conversion feature",
    "Update documentation"
  ]
}
```

---

#### Tuesday-Thursday - DO (Developer)

**Task:** Implement improvements

**Developer workflow:**
```bash
# 1. Create feature branch
git checkout -b feature/thai-numerals

# 2. Implement fix in ocr_skill/__init__.py
def fix_thai_numerals(text):
    thai_nums = {'๑':'1','๒':'2','๓':'3','๔':'4','๕':'5',
                 '๖':'6','๗':'7','๘':'8','๙':'9','๐':'0'}
    for thai, arabic in thai_nums.items():
        text = text.replace(thai, arabic)
    return text

# 3. Test locally
python examples/01_basic_usage.py

# 4. Commit changes
git add ocr_skill/__init__.py
git commit -m "Add Thai numeral conversion"

# 5. Push for review
git push origin feature/thai-numerals
```

---

#### Friday - CHECK (QA)

**Task:** Test and verify

**QA workflow:**
```bash
# 1. Pull latest changes
git pull origin feature/thai-numerals

# 2. Test on real documents
python src/ocr_processor.py

# 3. Check output quality
cat output_txt/document.txt

# 4. Verify numeral conversion worked
# Before: ๑๒๓๔๕
# After:  12345 ✓

# 5. Report results
# Update pdca_log.json with test results
```

**Update pdca_log.json:**
```json
{
  "week": 1,
  "end_date": "2026-04-04",
  "results": {
    "tasks_completed": 3,
    "tests_passed": true,
    "quality_improvement": "+5.2%",
    "issues_found": 1
  }
}
```

---

#### Friday Afternoon - ACT (Tech Lead)

**Task:** Review and decide next steps

```bash
# 1. Review QA results
cat pdca_log.json

# 2. If quality good → Merge to main
git checkout main
git merge feature/thai-numerals
git push origin main

# 3. Plan next week
# Based on results, decide:
# - Continue improvements?
# - Fix remaining issues?
# - Release new version?
```

**Decision:**
- ✅ Quality improved from 87% → 92%
- ✅ Numeral conversion working
- ⚠️ 1 issue: Legal terms still need work

**Next week focus:** Legal term improvements

---

## 📊 Progress Tracking (pdca_log.json)

```json
{
  "project": "OCR Skill",
  "team_size": 3,
  "start_date": "2026-03-31",
  
  "week_1": {
    "focus": "Thai text improvements",
    "tasks_completed": 3,
    "quality_before": "87%",
    "quality_after": "92%",
    "improvement": "+5%"
  },
  
  "week_2": {
    "focus": "Legal terms",
    "tasks_completed": 2,
    "quality_before": "92%",
    "quality_after": "94%",
    "improvement": "+2%"
  },
  
  "week_3": {
    "focus": "Documentation",
    "tasks_completed": 4,
    "quality_before": "94%",
    "quality_after": "95%",
    "improvement": "+1%"
  },
  
  "overall": {
    "total_weeks": 3,
    "total_tasks": 9,
    "quality_start": "87%",
    "quality_current": "95%",
    "total_improvement": "+8%"
  }
}
```

---

## 📋 Team Meeting Template

### Weekly Meeting Agenda (30 mins)

**1. Review Last Week (10 mins)**
- What did we complete?
- What issues were found?
- Quality metrics?

**2. Plan This Week (10 mins)**
- What's the focus?
- Who does what?
- Expected outcomes?

**3. Blockers (5 mins)**
- Any issues?
- Need help?

**4. Action Items (5 mins)**
- Assign tasks
- Set deadlines

---

## 🎯 Long-term Goals

### Month 1: Foundation
- [x] Basic OCR working
- [ ] Thai numeral conversion ✓ (Week 1)
- [ ] Legal term handling (Week 2)
- [ ] Documentation update (Week 3)

### Month 2: Quality
- [ ] 95% accuracy on Thai documents
- [ ] Handle complex layouts
- [ ] Add table detection

### Month 3: Features
- [ ] Handwriting support (PaddleOCR)
- [ ] Cloud API integration
- [ ] Batch processing improvements

### Month 4: Release
- [ ] Version 1.0.0
- [ ] PyPI publication
- [ ] User documentation

---

## 💡 Tips for Small Team

### Work Smart

1. **Small iterations** - Improve a little each week
2. **Test on real docs** - Use actual Thai documents
3. **Track progress** - Update pdca_log.json weekly
4. **Celebrate wins** - Note every improvement

### Communication

```
# Use simple status updates
Monday: "Starting work on Thai numerals"
Wednesday: "Numeral conversion implemented, testing"
Friday: "✓ Complete - Quality +5%"
```

### Quality Over Speed

```
Better to fix 1 bug properly than 5 bugs quickly.
Better to improve 1% each week than 10% once.
```

---

## 📁 Files to Maintain

| File | Purpose | Updated By |
|------|---------|------------|
| `pdca_log.json` | Progress tracking | Tech Lead |
| `README.md` | Documentation | Developer |
| `CHANGELOG.md` | Version history | Tech Lead |
| `test_results/` | QA reports | QA Engineer |

---

## 🚀 Quick Start for New Team

### Day 1: Setup

```bash
# Clone repo
git clone https://github.com/tps2015gh/ocr_skill.git
cd ocr_skill

# Install dependencies
pip install -r requirements.txt

# Test OCR
python src/ocr_processor.py
```

### Day 2: First Task

```bash
# Tech Lead assigns task
# Example: "Fix Thai vowel confusion"

# Developer implements
git checkout -b feature/vowel-fix
# ... implement fix ...
git commit -m "Fix Thai vowels"

# QA tests
python src/ocr_processor.py
# ... verify quality ...
```

### Day 3-5: Continue

```bash
# Repeat cycle
# Small improvements daily
# Weekly review every Friday
```

---

## 📊 Example: 4-Week Sprint

### Week 1: Thai Numerals
- **Before:** 87% quality
- **Fix:** Numeral conversion
- **After:** 92% quality
- **Time:** 3 days

### Week 2: Legal Terms
- **Before:** 92% quality
- **Fix:** Legal term dictionary
- **After:** 94% quality
- **Time:** 4 days

### Week 3: Tone Marks
- **Before:** 94% quality
- **Fix:** Tone mark stacking
- **After:** 95% quality
- **Time:** 3 days

### Week 4: Documentation
- **Before:** Outdated docs
- **Fix:** Update all examples
- **After:** Complete docs
- **Time:** 2 days

**Total Improvement:** 87% → 95% in 4 weeks! 🎉

---

**Version:** 4.0.0 (Small Team Guide)  
**Last Updated:** March 31, 2026

**Remember:** Small team, steady progress, quality product! 🚀
