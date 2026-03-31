@echo off
echo ============================================
echo AI OCR Processor - Thai and English
echo ============================================
echo.

cd /d %~dp0..

echo Starting OCR processing...
python src\ocr_processor.py

echo.
echo ============================================
echo Processing Complete!
echo ============================================
pause
