"""
Example 4: AI Agent Integration

This example shows how to integrate OCR as a tool in an AI agent.
"""

from ocr_skill.skill import OCRSkill

class MyAIAgent:
    """Example AI agent with OCR capability"""
    
    def __init__(self):
        # Initialize OCR skill
        self.ocr = OCRSkill(languages='tha+eng')
    
    def read_document(self, file_path):
        """Agent tool: Read a document using OCR"""
        print(f"📖 Reading document: {file_path}")
        text = self.ocr.extract_text(file_path)
        print(f"✓ Extracted {len(text)} characters")
        return text
    
    def analyze_document(self, file_path):
        """Agent tool: Analyze a document"""
        result = self.ocr.scan(file_path)
        
        analysis = {
            'file': result.file_path,
            'type': result.file_type,
            'pages': result.total_pages,
            'total_chars': len(result.get_all_text()),
            'output_files': {
                'txt': result.txt_output,
                'md': result.md_output
            }
        }
        
        return analysis


# Usage example
if __name__ == "__main__":
    agent = MyAIAgent()
    
    # Read a document
    text = agent.read_document("input_pdf/document.pdf")
    
    # Analyze a document
    info = agent.analyze_document("input_pdf/document.pdf")
    print(f"\nDocument Analysis:")
    for key, value in info.items():
        print(f"  {key}: {value}")
