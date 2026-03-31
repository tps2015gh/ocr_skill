# AI OCR GML OCR Project

A powerful PDF OCR (Optical Character Recognition) processor supporting **Thai and English** languages. This project processes PDF files and converts them to text and markdown formats with page-by-page separation.

---

## 📋 Features

- **Multi-language Support**: Thai (tha) + English (eng) OCR
- **Batch Processing**: Process multiple PDF files automatically
- **Progress Tracking**: Real-time progress display during processing
- **Dual Output**: Generate both TXT and MD (Markdown) formats
- **Page Separation**: Each page is clearly separated in output files
- **Memory Efficient**: Optimized for processing large PDF files
- **Configurable**: Easy-to-edit configuration file

---

## 🏗️ Project Structure

```
ai_ocr_GML_OCR/
├── config/                 # Configuration files
│   └── config.ini         # OCR settings
├── input_pdf/             # Input PDF files (gitignored)
├── output_txt/            # TXT output files (gitignored)
├── output_md/             # MD output files (gitignored)
├── scripts/               # Utility scripts
│   └── run_ocr.bat        # Windows batch script to run OCR
├── src/                   # Source code
│   ├── __init__.py
│   └── ocr_processor.py   # Main OCR processing script
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── requirements.txt       # Python dependencies
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
- Place PDF files in `input_pdf/` folder
- The processor automatically finds all `.pdf` files
- Processes the 3 largest files by default (configurable)

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

This project is provided as-is for educational and practical use.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review `ocr_progress.log` for processing details
3. Verify configuration in `config\config.ini`

---

**Last Updated:** March 31, 2026
**Version:** 1.0.0
