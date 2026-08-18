# Hotkey Screenshot Automation

Python scripts for capturing screenshots with keyboard shortcuts and finding screen coordinates.

## Scripts

- `clipboard_capture.py`: Runs the screenshot hotkey tool.
  - Backtick key captures a screenshot
  - Backslash pauses/resumes the script
  - Esc stops the script

- `find_coordinates.py`: Helps find and adjust screen/window coordinates when using different screens or monitors.

## Requirements

These scripts require the Python packages listed in `requirements.txt`.

Tesseract is the OCR engine, and `pytesseract` lets Python talk to Tesseract.

## Python Libraries/Packages

- `keyboard`: listens for keyboard shortcuts/hotkeys like backtick, backslash, and Esc.
- `pyautogui`: takes screenshots and gets mouse coordinates.
- `pillow`: image-processing library used to handle and save screenshot images.
- `pytesseract`: Python wrapper that sends images to Tesseract OCR so text can be extracted from screenshots.
- `pywin32`: Windows-only package used to copy images to the Windows clipboard.

## Mac Setup

```bash
pip install -r requirements.txt
brew install tesseract
