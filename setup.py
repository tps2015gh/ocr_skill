"""
Setup script for ai_ocr_gml_ocr package
Install with: pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [line.strip() for line in requirements_path.read_text().splitlines() if line.strip() and not line.startswith('#')]

setup(
    name='ai_ocr_gml_ocr',
    version='1.0.0',
    author='Qwen Code AI Assistant',
    description='OCR processor for Thai and English documents (PDF, JPG, PNG, BMP, TIFF)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ai_ocr_gml_ocr',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ai-ocr=src.ocr_processor:main',
        ],
    },
    keywords='ocr thai english pdf image tesseract document-processing',
)
