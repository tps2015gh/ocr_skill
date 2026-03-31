# OCR Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Thai & English](https://img.shields.io/badge/lang-Thai%20%26%20English-green.svg)](https://github.com/tps2015gh/ocr_skill)

A powerful OCR (Optical Character Recognition) processor supporting **Thai and English** languages. 
This project processes **PDF and Image files** (JPG, PNG, BMP, TIFF, GIF) and converts them to text 
and markdown formats with page-by-page separation.

**Now available as a reusable Python package!** Install and use in any project.

---

## 📋 Features

- **Multi-language Support**: Thai (tha) + English (eng) OCR
- **Multiple Input Formats**: PDF, JPG, JPEG, PNG, BMP, TIFF, GIF
- **Batch Processing**: Process multiple files automatically
- **Progress Tracking**: Real-time progress display during processing
- **Dual Output**: Generate both TXT and MD (Markdown) formats
- **Page Separation**: Each page is clearly separated in output files
- **Memory Efficient**: Optimized for processing large files
- **Configurable**: Easy-to-edit configuration file
- **🔌 Reusable Skill**: Easy integration into other projects
- **🤖 AI Agent Ready**: Built-in support for AI agent tool integration
- **🔄 PDCA Loop**: Agent-guided continuous improvement for complex Thai OCR (see `PDCA_LOOP.md`)

---

## 🏗️ Project Structure

```
ocr_skill/
├── ocr_skill/            # Reusable package (import this!)
│   ├── __init__.py       # Main exports: process_file, OCRProcessor
│   ├── skill.py          # OCRSkill class for AI agents
│   └── models.py         # Data models
├── config/               # Configuration files
│   └── config.ini        # OCR settings
├── examples/             # Usage examples
│   ├── 01_basic_usage.py
│   ├── 02_custom_config.py
│   ├── 03_skill_usage.py
│   ├── 04_agent_integration.py
│   └── README.md
├── src/                  # Source code (internal)
│   ├── __init__.py
│   └── ocr_processor.py  # Core OCR processor
├── input_pdf/            # Input files (PDF, JPG, PNG, etc.) - gitignored
├── output_txt/           # TXT output files - gitignored
├── output_md/            # MD output files - gitignored
├── scripts/              # Utility scripts
│   └── run_ocr.bat       # Windows batch script
├── .gitignore            # Git ignore rules
├── setup.py              # Package installation
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── PDCA_LOOP.md          # Agent guide for continuous improvement
```

---

## 🚀 Installation

### Prerequisites

1. **Python 3.8+** (32-bit or 64-bit)
2. **Tesseract OCR** with Thai and English language packs

### Step 1: Install Tesseract OCR

#### Option A: Using Chocolatey (Recommended)
```powershell
# Run PowerShell as Administrator
choco install tesseract --add-package-parameters "/Langs=tha,eng" -y
```

#### Option B: Manual Installation
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. During installation, select Thai and English language packs
3. Default installation path: `C:\Program Files\Tesseract-OCR`

### Step 2: Install Python Dependencies

```bash
cd D:\dev\ai_ocr_GML_OCR
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pymupdf pytesseract pillow
```

---

## 📖 Usage

### Quick Start (Windows)

Double-click `scripts\run_ocr.bat` or run:

```bash
scripts\run_ocr.bat
```

### Command Line

```bash
python src\ocr_processor.py
```

### Configuration

Edit `config\config.ini` to customize settings:

```ini
[ocr]
# Languages for OCR (Thai + English)
languages = tha+eng

# DPI for rendering (150 recommended for balance)
dpi = 150

[output]
# Output directories
txt_output_dir = output_txt
md_output_dir = output_md

[processing]
# Number of largest files to process
process_top_files = 3

# Show progress bar
show_progress = true
```

---

## 📤 Input/Output

### Input
- Place files in `input_pdf/` folder
- **Supported formats**: PDF, JPG, JPEG, PNG, BMP, TIFF, GIF
- The processor automatically finds all supported files
- Processes the 3 largest files by default (configurable in `config.ini`)

### Output
- **TXT Format**: `output_txt/` - Plain text with page separators
- **MD Format**: `output_md/` - Markdown with formatted pages

#### Example Output Structure

**TXT File:**
```
Original File: document.pdf
Processed: 2026-03-31 15:30:00
================================================================================

================================================================================
Page 1
================================================================================

[OCR text content...]

================================================================================
Page 2
================================================================================

[OCR text content...]
```

**MD File:**
```markdown
# OCR Output: document.pdf

**Processed:** 2026-03-31 15:30:00

**Original File:** `document.pdf`

---

## Page 1

```
[OCR text content...]
```

---
```

---

## 🧪 Processed Files

The following files have been processed:

| File | Pages | Output TXT | Output MD |
|------|-------|------------|-----------|
| 04-ใบเสนอราคาและเอกสารแนบท้าย.pdf | 392 | ✅ | ✅ |
| 02-ขอบเขตของงานฯ.pdf | 62 | ✅ | ✅ |
| ประกาศนียบัตรฯ Cybersecurity.pdf | 1 | ✅ | ✅ |

---

## 🔌 Integration Guide (Use as a Skill)

This OCR processor can be easily integrated into other projects as a reusable skill.

### Method 1: Install as Python Package (Recommended)

```bash
# Navigate to project directory
cd D:\dev\ai_ocr_GML_OCR

# Install as editable package
pip install -e .

# Now you can import from anywhere!
python -c "from ocr_skill import process_file; print('Installed!')"
```

### Method 2: Copy Package to Your Project

```bash
# Copy the ocr_skill folder to your project
cp -r ocr_skill/ /your/project/path/

# Then import in your code
from ocr_skill import process_file
```

### Quick Integration

#### Method 1: Simple Function
```python
from ocr_skill import process_file

# Process a file
result = process_file("document.pdf")
text = result.get_all_text()
print(text)
```

#### Method 2: OCR Skill (Recommended for AI Agents)
```python
from ocr_skill.skill import OCRSkill

# Initialize skill
ocr = OCRSkill(languages='tha+eng')

# Extract text
text = ocr.extract_text("document.pdf")

# Or get full result
result = ocr.scan("image.png")
print(f"Pages: {result.total_pages}")
print(f"Output: {result.txt_output}")
```

#### Method 3: Custom Configuration
```python
from ocr_skill import OCRProcessor

# Create processor with custom settings
processor = OCRProcessor(
    languages='eng',      # English only
    dpi=200,              # Higher quality
    txt_output_dir='output',
    show_progress=True
)

result = processor.process_file_simple("document.pdf")
```

### AI Agent Tool Integration

```python
from ocr_skill.skill import OCRSkill

class MyAgent:
    def __init__(self):
        self.ocr = OCRSkill()
    
    def read_document(self, file_path):
        """Tool: Read document with OCR"""
        return self.ocr.extract_text(file_path)
    
    def analyze_document(self, file_path):
        """Tool: Analyze document structure"""
        result = self.ocr.scan(file_path, return_dict=True)
        return {
            'pages': result['total_pages'],
            'type': result['file_type'],
            'text': result['pages'][0]['text'] if result['pages'] else ''
        }
```

### Batch Processing

```python
from ocr_skill.skill import OCRSkill

ocr = OCRSkill()

# Process multiple files
files = ["doc1.pdf", "doc2.png", "doc3.jpg"]
results = ocr.scan_batch(files)

for result in results:
    print(f"{result.file_path}: {result.total_pages} pages")
```

### Output Formats

```python
result = ocr.scan("document.pdf")

# Get all text
all_text = result.get_all_text()

# Get specific page
page_1 = result.get_page_text(1)

# Get as dictionary
data = result.to_dict()

# Save to files
result.save_txt("output/result.txt")
result.save_md("output/result.md")
```

---

## 🛠️ Troubleshooting

### Tesseract Not Found
If you get "tesseract is not recognized" error:
1. Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR`
2. Check if `tesseract.exe` exists in that folder
3. Add to PATH manually or restart your terminal

### Memory Errors
If you encounter memory errors with large PDFs:
1. Lower the DPI in `config\config.ini` (try 100 or 72)
2. Process fewer files at once
3. Use 64-bit Python instead of 32-bit

### Thai Language Not Recognized
Ensure Thai language pack is installed:
```
C:\Program Files\Tesseract-OCR\tessdata\tha.traineddata
```

---

## 👥 Project Team

### Human Team
| Role | Responsibilities |
|------|------------------|
| **Supervisor Director** | Project oversight, requirements definition, final approval |

### AI Agent Team
This project was developed using a multi-agent approach:

| Role | Responsibilities |
|------|------------------|
| **Lead Tech** | Architecture design, technology selection, code review |
| **System Engineer & DevOps** | Environment setup, dependencies, git configuration |
| **Programmer** | Implementation, testing, optimization |
| **QA** | Quality assurance, output verification |

---

## 🤖 About the AI Assistant

### Model: Qwen Code (قwen)
**Developed by Alibaba Group**

#### My Role in This Project:
1. **Project Setup**: Created folder structure and git configuration
2. **Dependency Management**: Installed and configured OCR libraries
3. **Code Development**: Wrote the OCR processor script with progress tracking
4. **Processing**: Executed batch OCR on 3 large PDF files (455 pages total)
5. **Documentation**: Created comprehensive README and usage instructions

#### My Opinion on This Solution:

**Strengths:**
- ✅ **Memory Efficient**: Uses generator-based processing to handle large PDFs
- ✅ **User Friendly**: Simple configuration and one-click execution
- ✅ **Bilingual**: Properly handles both Thai and English text
- ✅ **Well Structured**: Clean folder organization following best practices
- ✅ **Git Ready**: Proper `.gitignore` keeps output files out of version control
- ✅ **Reusable Skill**: Easy to deploy and integrate into other projects
- ✅ **AI Agent Ready**: Built-in support for Qwen CLI, Gemini CLI, and custom agents

**Considerations:**
- ⚠️ **Processing Speed**: OCR is CPU-intensive; large files take time
- ⚠️ **Python 32-bit Limitation**: Memory constraints may affect very large files
- ⚠️ **Tesseract Quality**: Thai OCR accuracy depends on document quality

**Recommendations for Improvement:**
1. Consider upgrading to Python 3.12+ for better performance
2. Add PDF text extraction before OCR (skip OCR for text-based PDFs)
3. Implement parallel processing for multi-core utilization
4. Add confidence scoring for OCR results

---

## 💬 Brief Opinion

**When to Use OCR Skill:**

✅ **Great for:**
- Thai and English document digitization
- Batch PDF processing with page separation
- AI agent workflows requiring document reading
- Quick deployment as reusable Python package
- Government/legal document processing (Thai language support)
- Printed documents with clear text

❌ **Not ideal for:**
- Handwritten text recognition (Tesseract limitation)
- Real-time OCR needs (processing takes time)
- Complex layout preservation (tables, forms may lose structure)
- Non-Latin/Non-Thai scripts without language packs

**💡 Pro Tip:** For complex layouts or handwriting, see [`ADVANCED_OCR.md`](ADVANCED_OCR.md) which covers:
- PaddleOCR integration (free, supports handwriting + layout) - **Optional add-on**
- Azure Form Recognizer (best for forms/tables)
- Google Cloud Vision (best for handwriting)
- Hybrid approach combining multiple engines

**🔧 Current Engine:** This project uses **Tesseract OCR** (not PaddleOCR by default). PaddleOCR support is available as an optional advanced feature.

**Bottom Line:** OCR Skill is a practical, well-engineered solution for Thai-English document processing using Tesseract OCR. It excels at batch operations and integrates smoothly with AI agent workflows. For best results, use with printed documents at 150+ DPI and consider AI post-processing for critical accuracy needs. For complex layouts or handwriting, add PaddleOCR (see ADVANCED_OCR.md).

---

## 📌 Important Notes

### About Tesseract OCR
This project uses **Tesseract OCR** via the `pytesseract` Python wrapper:
- Tesseract is an open-source OCR engine developed by Google
- Supports 100+ languages including Thai (`tha`) and English (`eng`)
- Language data files must be installed separately (`.traineddata` files)
- Accuracy depends on image quality, DPI settings, and language complexity

**Tesseract Installation Path (Windows):**
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Language Files Location:**
```
C:\Program Files\Tesseract-OCR\tessdata\tha.traineddata
C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata
```

### 💡 Post-OCR Accuracy Improvement with AI

**Observation:** After initial OCR processing with Tesseract, using an **online AI model** (such as ChatGPT, Claude, or Qwen) to review and adjust the OCR output can significantly improve accuracy, especially for:

1. **Thai Language Characters**: Thai script has complex vowels and tone marks that OCR may misrecognize
2. **Numbers and Dates**: Thai numerals vs. Arabic numerals confusion
3. **Special Characters**: Legal document symbols, bullet points, formatting
4. **Context Understanding**: AI can correct words based on document context

**Recommended Workflow:**
```
PDF → Tesseract OCR → Raw Text → AI Model Review → Corrected Text → Final Output
```

**Example AI Prompt for Correction:**
```
Please review and correct the following Thai OCR text. Fix any:
- Misrecognized Thai characters
- Incorrect numbers or dates
- Broken words or spacing issues
- Context-inappropriate words

Keep the original meaning and format intact.
```

**Why This Works:**
- Large Language Models (LLMs) have strong language understanding
- Can infer correct words from context
- Understands Thai grammar and common document patterns
- More accurate than OCR alone for ambiguous characters

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**In short:** You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review `ocr_progress.log` for processing details
3. Verify configuration in `config\config.ini`

---

**Last Updated:** March 31, 2026
**Version:** 1.0.0
