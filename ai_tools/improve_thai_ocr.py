"""
Improve OCR for Complex Thai - Automated PDCA Cycle
====================================================

This script runs the full PDCA improvement cycle for complex Thai OCR.

Usage:
    python ai_tools/improve_thai_ocr.py
"""

import sys
import time
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_tools import PDCATools
from skill import process_file


def improve_thai_ocr(input_file: str, target_quality: float = 0.90):
    """
    Run full PDCA cycle to improve Thai OCR quality.
    
    Args:
        input_file: Path to Thai PDF/image file
        target_quality: Target quality score (0.0-1.0)
    """
    print("\n" + "="*70)
    print("🚀 IMPROVE OCR FOR COMPLEX THAI")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Target Quality: {target_quality:.0%}")
    print("="*70 + "\n")
    
    tools = PDCATools()
    
    # ========== PHASE 1: PLAN ==========
    print("📋 PHASE 1: PLAN (Tech Lead)")
    print("-"*70)
    
    tools.plan_week(
        focus="Complex Thai OCR improvement",
        tasks=[
            "Run initial OCR",
            "Apply Thai text fixes",
            "Test quality"
        ],
        goals=[
            f"Achieve {target_quality:.0%} quality",
            "Fix Thai vowels and tone marks",
            "Convert Thai numerals"
        ]
    )
    
    print("✓ Planning complete\n")
    time.sleep(1)
    
    # ========== PHASE 2: DO ==========
    print("🔧 PHASE 2: DO (Developer)")
    print("-"*70)
    
    # Run initial OCR
    print("Running OCR...")
    result = process_file(input_file, show_progress=False)
    ocr_text = result.get_all_text()
    print(f"✓ OCR complete: {len(ocr_text)} characters")
    print(f"✓ Pages: {result.total_pages}")
    
    # Save initial OCR
    output_file = Path("output_txt") / f"{Path(input_file).stem}_ocr.txt"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ocr_text)
    print(f"✓ Saved: {output_file}")
    
    # Apply Thai fixes
    print("\nApplying Thai text fixes...")
    fixed_text = tools.apply_all_fixes(ocr_text, show_progress=True)
    
    # Save fixed text
    fixed_file = Path("output_txt") / f"{Path(input_file).stem}_fixed.txt"
    with open(fixed_file, 'w', encoding='utf-8') as f:
        f.write(fixed_text)
    print(f"✓ Saved: {fixed_file}")
    
    print("✓ Development complete\n")
    time.sleep(1)
    
    # ========== PHASE 3: CHECK ==========
    print("🧪 PHASE 3: CHECK (QA)")
    print("-"*70)
    
    # Calculate quality before fixes
    quality_before = tools.calculate_quality(ocr_text, log=False)
    print(f"Quality BEFORE fixes: {quality_before:.0%}")
    
    # Calculate quality after fixes
    quality_after = tools.calculate_quality(fixed_text, log=True)
    print(f"Quality AFTER fixes:  {quality_after:.0%}")
    
    improvement = quality_after - quality_before
    print(f"Improvement: {improvement:+.0%}")
    
    # Show comparison
    print("\nComparison:")
    print(f"  Before: {len(ocr_text)} chars")
    print(f"  After:  {len(fixed_text)} chars")
    print(f"  Difference: {len(ocr_text) - len(fixed_text):+d} chars")
    
    print("✓ Testing complete\n")
    time.sleep(1)
    
    # ========== PHASE 4: ACT ==========
    print("📊 PHASE 4: ACT (Tech Lead)")
    print("-"*70)
    
    if quality_after >= target_quality:
        print(f"✓ Target quality reached! ({quality_after:.0%} >= {target_quality:.0%})")
        tools.review_week(
            quality_before=f"{quality_before:.0%}",
            quality_after=f"{quality_after:.0%}",
            improvement=f"+{improvement:.0%}",
            notes="Complex Thai OCR improved successfully"
        )
    else:
        print(f"⚠ Target not reached ({quality_after:.0%} < {target_quality:.0%})")
        print("  More iterations needed")
        tools.review_week(
            quality_before=f"{quality_before:.0%}",
            quality_after=f"{quality_after:.0%}",
            improvement=f"+{improvement:.0%}",
            notes="Need more improvement iterations"
        )
    
    print("✓ Review complete\n")
    
    # ========== SUMMARY ==========
    print("="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Pages: {result.total_pages}")
    print(f"Quality: {quality_before:.0%} → {quality_after:.0%} ({improvement:+.0%})")
    print(f"Target: {target_quality:.0%}")
    print(f"Status: {'✓ PASSED' if quality_after >= target_quality else '⚠ NEEDS WORK'}")
    print(f"\nOutput files:")
    print(f"  OCR: {output_file}")
    print(f"  Fixed: {fixed_file}")
    print("="*70 + "\n")
    
    return {
        'input': input_file,
        'pages': result.total_pages,
        'quality_before': quality_before,
        'quality_after': quality_after,
        'improvement': improvement,
        'target_met': quality_after >= target_quality,
        'output_files': {
            'ocr': str(output_file),
            'fixed': str(fixed_file)
        }
    }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Improve Thai OCR with PDCA cycle')
    parser.add_argument('input_file', nargs='?', default='input_pdf/02-ขอบเขตของงานฯ.pdf',
                       help='Input PDF/image file')
    parser.add_argument('--quality', type=float, default=0.90,
                       help='Target quality (0.0-1.0)')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not Path(args.input_file).exists():
        print(f"❌ File not found: {args.input_file}")
        print("\nAvailable files:")
        input_dir = Path('input_pdf')
        if input_dir.exists():
            for f in input_dir.glob('*.pdf')[:5]:
                print(f"  - {f}")
        return
    
    # Run improvement
    result = improve_thai_ocr(args.input_file, args.quality)
    
    # Open dashboard to see results
    print("\n📊 Opening dashboard to view agent activities...")
    print("   (Dashboard should show Tech Lead, Developer, QA at work)")
    print("   Visit: http://localhost:8000\n")


if __name__ == "__main__":
    main()
