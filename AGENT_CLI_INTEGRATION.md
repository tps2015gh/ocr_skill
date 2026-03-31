# AI Agent CLI Integration Guide

This guide shows how to use OCR Skill from AI agent command-line interfaces like **Gemini CLI** and **Qwen CLI**.

---

## 📋 Prerequisites

Before using OCR Skill with AI agent CLIs, ensure:

1. **OCR Skill is installed:**
   ```bash
   cd D:\dev\ai_ocr_GML_OCR
   pip install -e .
   ```

2. **Tesseract OCR is installed:**
   ```bash
   # Windows
   choco install tesseract --add-package-parameters "/Langs=tha,eng"
   
   # Verify installation
   tesseract --version
   ```

3. **AI Agent CLI is installed:**
   ```bash
   # For Qwen CLI
   npm install -g @qwen-code/qwen-code
   
   # For Gemini CLI (Google Cloud)
   # Follow: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text
   ```

---

## 🤖 Qwen CLI Integration

### Method 1: Direct Python Import

Use OCR Skill directly in your Python code that's called by Qwen CLI:

```python
# ocr_tool.py
from ocr_skill import process_file
from ocr_skill.skill import OCRSkill

def read_document(file_path: str) -> str:
    """
    Read a document using OCR and return the text.
    This function can be called by Qwen CLI agents.
    """
    ocr = OCRSkill(languages='tha+eng')
    text = ocr.extract_text(file_path)
    return text

def analyze_document(file_path: str) -> dict:
    """
    Analyze a document and return metadata.
    """
    ocr = OCRSkill()
    result = ocr.scan(file_path)
    
    return {
        'file': result.file_path,
        'pages': result.total_pages,
        'type': result.file_type,
        'text_preview': result.get_all_text()[:500]
    }

# Example usage
if __name__ == "__main__":
    text = read_document("input_pdf/document.pdf")
    print(f"Extracted {len(text)} characters")
```

**Call from Qwen CLI:**
```bash
qwen "Read this PDF and summarize it" --file input_pdf/document.pdf
```

### Method 2: Create Qwen CLI Tool

Create a tool that Qwen CLI can invoke:

```python
# qwen_ocr_tool.py
import sys
import json
from ocr_skill.skill import OCRSkill

def ocr_extract(file_path, output_format='text'):
    """
    OCR extraction tool for Qwen CLI.
    
    Usage:
        python qwen_ocr_tool.py extract <file_path> [--format text|json|md]
    """
    ocr = OCRSkill(languages='tha+eng')
    result = ocr.scan(file_path)
    
    if output_format == 'json':
        output = result.to_dict()
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif output_format == 'md':
        print(f"# OCR Result: {result.file_path}\n")
        print(f"**Pages:** {result.total_pages}\n")
        print("---\n")
        print(result.get_all_text())
    else:  # text
        print(result.get_all_text())

def main():
    if len(sys.argv) < 3:
        print("Usage: python qwen_ocr_tool.py extract <file> [--format text|json|md]")
        sys.exit(1)
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    
    # Parse optional format argument
    output_format = 'text'
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]
    
    if command == 'extract':
        ocr_extract(file_path, output_format)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
# Extract as text
python qwen_ocr_tool.py extract document.pdf

# Extract as JSON (structured data)
python qwen_ocr_tool.py extract document.pdf --format json

# Extract as Markdown
python qwen_ocr_tool.py extract document.pdf --format md

# Pipe to Qwen CLI for analysis
python qwen_ocr_tool.py extract document.pdf | qwen "Summarize this text"
```

### Method 3: Qwen Agent with OCR Tool

Create a custom Qwen agent with OCR capability:

```python
# qwen_agent_with_ocr.py
from qwen_agent.agents import Assistant
from ocr_skill.skill import OCRSkill

# Initialize OCR skill
ocr_skill = OCRSkill(languages='tha+eng')

# Define OCR tool
def ocr_read(file_path: str) -> str:
    """Read document text using OCR"""
    return ocr_skill.extract_text(file_path)

def ocr_analyze(file_path: str) -> dict:
    """Analyze document structure"""
    result = ocr_skill.scan(file_path)
    return {
        'pages': result.total_pages,
        'type': result.file_type,
        'text': result.get_all_text()
    }

# Create agent with OCR tools
agent = Assistant(
    name='OCR Assistant',
    description='AI assistant with OCR capabilities for Thai and English documents',
    tools=[ocr_read, ocr_analyze],
    instruction='''You are an assistant that can read documents using OCR.
When user asks to read a PDF or image, use the ocr_read tool to extract text.
When user asks about document structure, use ocr_analyze tool.
Support both Thai and English languages.'''
)

# Run agent
messages = []
while True:
    query = input("User: ")
    if query.lower() in ['quit', 'exit']:
        break
    
    messages.append({'role': 'user', 'content': query})
    response = agent.run(messages)
    print(f"Assistant: {response}")
    messages.append({'role': 'assistant', 'content': response})
```

**Run the agent:**
```bash
python qwen_agent_with_ocr.py
```

---

## 🌟 Gemini CLI Integration

### Method 1: Vertex AI with OCR

```python
# gemini_ocr_integration.py
from ocr_skill import process_file
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key='YOUR_GEMINI_API_KEY')
model = genai.GenerativeModel('gemini-pro')

def process_with_gemini(file_path: str, prompt: str = None):
    """
    Process document with OCR and analyze with Gemini.
    
    Args:
        file_path: Path to PDF or image
        prompt: Question or instruction for Gemini
    
    Returns:
        Gemini's analysis of the document
    """
    # Step 1: Extract text with OCR
    print("Extracting text with OCR...")
    ocr_result = process_file(file_path)
    text = ocr_result.get_all_text()
    
    # Step 2: Analyze with Gemini
    if not prompt:
        prompt = "Summarize this document:"
    
    full_prompt = f"{prompt}\n\nDocument text:\n{text}"
    
    print("Analyzing with Gemini...")
    response = model.generate_content(full_prompt)
    
    return {
        'ocr_text': text,
        'gemini_response': response.text,
        'pages': ocr_result.total_pages
    }

# Usage
if __name__ == "__main__":
    result = process_with_gemini(
        "input_pdf/document.pdf",
        "Extract key points and action items from this document"
    )
    
    print(f"\nPages: {result['pages']}")
    print(f"\nGemini Analysis:\n{result['gemini_response']}")
```

### Method 2: Gemini CLI Tool

Create a command-line tool for Gemini:

```python
# gemini_ocr_cli.py
import argparse
import sys
from ocr_skill.skill import OCRSkill
import google.generativeai as genai

def setup_argparse():
    parser = argparse.ArgumentParser(description='OCR + Gemini CLI Tool')
    parser.add_argument('file', help='PDF or image file to process')
    parser.add_argument('--prompt', '-p', default='Summarize this document',
                       help='Prompt for Gemini')
    parser.add_argument('--api-key', '-k', help='Gemini API key')
    parser.add_argument('--ocr-only', action='store_true',
                       help='Only run OCR, skip Gemini analysis')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'md'],
                       default='text', help='Output format')
    return parser.parse_args()

def main():
    args = setup_argparse()
    
    # Run OCR
    ocr = OCRSkill(languages='tha+eng')
    print(f"Processing {args.file}...", file=sys.stderr)
    
    result = ocr.scan(args.file)
    text = result.get_all_text()
    
    if args.ocr_only:
        if args.output == 'json':
            import json
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        elif args.output == 'md':
            print(f"# OCR Result\n\n{result.get_all_text()}")
        else:
            print(text)
        return
    
    # Run Gemini analysis
    if args.api_key:
        genai.configure(api_key=args.api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        print("Analyzing with Gemini...", file=sys.stderr)
        response = model.generate_content(f"{args.prompt}\n\n{text}")
        
        if args.output == 'json':
            import json
            print(json.dumps({
                'ocr_text': text,
                'gemini_response': response.text,
                'pages': result.total_pages
            }, indent=2, ensure_ascii=False))
        else:
            print(f"\n{response.text}")
    else:
        print("\nWarning: No API key provided. Showing OCR text only.", file=sys.stderr)
        print(text)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
# OCR only
python gemini_ocr_cli.py document.pdf --ocr-only

# OCR + Gemini analysis
python gemini_ocr_cli.py document.pdf \
  --prompt "Extract all dates and deadlines" \
  --api-key YOUR_API_KEY

# Output as JSON
python gemini_ocr_cli.py document.pdf --output json --api-key YOUR_API_KEY
```

### Method 3: Gemini Function Calling

Use Gemini's function calling with OCR:

```python
# gemini_function_calling_ocr.py
import google.generativeai as genai
from ocr_skill.skill import OCRSkill
import json

# Initialize
genai.configure(api_key='YOUR_API_KEY')
ocr = OCRSkill()

# Define OCR functions for Gemini
def read_document(file_path: str) -> str:
    """Extract text from a PDF or image file using OCR.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text content
    """
    result = ocr.scan(file_path)
    return result.get_all_text()

def get_document_info(file_path: str) -> dict:
    """Get metadata about a document.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Document metadata (pages, type, etc.)
    """
    result = ocr.scan(file_path)
    return {
        'pages': result.total_pages,
        'type': result.file_type,
        'processed_at': result.processed_at
    }

# Configure Gemini with functions
tools = [read_document, get_document_info]

model = genai.GenerativeModel(
    'gemini-pro',
    tools=tools
)

# Chat with document
def chat_with_document():
    print("Gemini OCR Assistant - Type 'quit' to exit")
    print("You can ask about PDF files in input_pdf/ folder\n")
    
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        # Add file path context
        if 'input_pdf/' in user_input or '.pdf' in user_input:
            response = chat.send_message(user_input)
        else:
            response = chat.send_message(user_input)
        
        print(f"Gemini: {response.text}\n")

if __name__ == "__main__":
    chat_with_document()
```

---

## 🔧 Custom Agent Integration Template

Create a reusable agent template:

```python
# agent_template.py
"""
Template for creating AI agents with OCR capabilities.
Works with Qwen, Gemini, or other LLM frameworks.
"""

from ocr_skill.skill import OCRSkill
from typing import Optional

class OCRAgent:
    """Base agent class with OCR capabilities"""
    
    def __init__(self, languages: str = 'tha+eng'):
        self.ocr = OCRSkill(languages=languages)
        self.documents = {}  # Cache processed documents
    
    def read(self, file_path: str, cache: bool = True) -> str:
        """Read document with OCR"""
        if cache and file_path in self.documents:
            return self.documents[file_path]
        
        text = self.ocr.extract_text(file_path)
        
        if cache:
            self.documents[file_path] = text
        
        return text
    
    def analyze(self, file_path: str) -> dict:
        """Analyze document structure"""
        result = self.ocr.scan(file_path)
        return result.to_dict()
    
    def search(self, file_path: str, query: str) -> list:
        """Search for text in document"""
        text = self.read(file_path)
        lines = text.split('\n')
        
        results = []
        for i, line in enumerate(lines, 1):
            if query.lower() in line.lower():
                results.append({
                    'line': i,
                    'text': line.strip()
                })
        
        return results
    
    def compare(self, file1: str, file2: str) -> dict:
        """Compare two documents"""
        text1 = self.read(file1)
        text2 = self.read(file2)
        
        return {
            'file1_chars': len(text1),
            'file2_chars': len(text2),
            'difference': abs(len(text1) - len(text2)),
            'similar': text1 == text2
        }

# Usage example
if __name__ == "__main__":
    agent = OCRAgent()
    
    # Read document
    text = agent.read("input_pdf/document.pdf")
    print(f"Extracted {len(text)} characters")
    
    # Search in document
    results = agent.search("input_pdf/document.pdf", "สัญญา")
    for r in results[:5]:
        print(f"Line {r['line']}: {r['text']}")
    
    # Analyze document
    info = agent.analyze("input_pdf/document.pdf")
    print(f"\nDocument Info: {info}")
```

---

## 📊 Comparison Table

| Method | Best For | Complexity |
|--------|----------|------------|
| **Direct Import** | Simple scripts | ⭐ Easy |
| **CLI Tool** | Command-line workflows | ⭐⭐ Medium |
| **Agent with Tools** | Interactive assistants | ⭐⭐⭐ Advanced |
| **Function Calling** | Automated workflows | ⭐⭐⭐ Advanced |

---

## 🎯 Quick Start Examples

### Qwen CLI - Quick Summary
```bash
# One-liner to summarize PDF
python -c "from ocr_skill import process_file; print(process_file('doc.pdf').get_all_text())" | qwen "Summarize this"
```

### Gemini CLI - Extract Information
```bash
# Extract specific information
python gemini_ocr_cli.py contract.pdf \
  --prompt "Extract: 1) Contract date, 2) Parties involved, 3) Key terms" \
  --api-key YOUR_KEY
```

### Custom Agent - Search Document
```python
from agent_template import OCRAgent

agent = OCRAgent()
results = agent.search("document.pdf", "deadline")

print("Mentions of 'deadline':")
for r in results:
    print(f"  Page {r['line']}: {r['text']}")
```

---

## 🐛 Troubleshooting

### "Module not found: ocr_skill"
```bash
# Install the package
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:/path/to/ocr_skill"
```

### "Tesseract not found"
```bash
# Install Tesseract
choco install tesseract  # Windows
brew install tesseract   # macOS
sudo apt install tesseract-ocr  # Linux

# Install Thai language pack
sudo apt install tesseract-ocr-tha
```

### "API key not valid" (Gemini)
```bash
# Get API key from: https://makersuite.google.com/app/apikey
# Set as environment variable
export GEMINI_API_KEY="your-api-key"
```

---

## 📚 Additional Resources

- **OCR Skill Documentation:** See `DEPLOYMENT.md`
- **Examples:** Check `examples/` folder
- **Tesseract Docs:** https://tesseract-ocr.github.io/
- **Qwen CLI:** https://github.com/qwen-code/qwen-code
- **Gemini API:** https://ai.google.dev/

---

**Version:** 1.0.0  
**Last Updated:** March 31, 2026
