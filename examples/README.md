# OCR Skill Examples

This folder contains examples showing how to use the OCR Skill package.

## Examples

### 01_basic_usage.py
Simplest way to process a file with OCR.

```bash
python examples/01_basic_usage.py
```

### 02_custom_config.py
Using custom configuration settings (DPI, languages, output directories).

```bash
python examples/02_custom_config.py
```

### 03_skill_usage.py
Using the OCR Skill interface - perfect for AI agent integration.

```bash
python examples/03_skill_usage.py
```

### 04_agent_integration.py
Full AI agent integration example with document analysis tools.

```bash
python examples/04_agent_integration.py
```

## Quick Reference

### Process a single file
```python
from ocr_skill import process_file
result = process_file("document.pdf")
text = result.get_all_text()
```

### Use OCR Skill
```python
from ocr_skill.skill import OCRSkill
ocr = OCRSkill()
text = ocr.extract_text("document.pdf")
```

### Custom configuration
```python
from ocr_skill import OCRProcessor
processor = OCRProcessor(languages='eng', dpi=200)
result = processor.process_file_simple("image.png")
```

## Supported Formats

- **Documents**: PDF
- **Images**: JPG, JPEG, PNG, BMP, TIFF, GIF

## Languages

Default: `tha+eng` (Thai + English)

Other options:
- `eng` - English only
- `tha` - Thai only
- See Tesseract documentation for full language list
