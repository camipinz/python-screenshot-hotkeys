from io import BytesIO
from pathlib import Path
import os
import platform
import subprocess
import sys
import time

import keyboard
import pyautogui
import pytesseract
from PIL import Image


SCREENSHOT_FOLDER_NAME = "event_screenshots"

# Optional: set this environment variable if Tesseract is not found automatically.
# Windows example:
#   set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
# macOS example:
#   export TESSERACT_CMD=/opt/homebrew/bin/tesseract
TESSERACT_CMD = os.environ.get("TESSERACT_CMD")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


paused = False
running = True


def copy_image_to_clipboard(image):
    """Copy a screenshot to the clipboard when the current platform supports it."""
    system = platform.system()

    if system == "Windows":
        try:
            import win32clipboard
        except ImportError:
            print("Clipboard copy skipped: install pywin32 on Windows to enable it.", flush=True)
            return

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            print("Image copied to clipboard.", flush=True)
        except Exception as error:
            print(f"Error copying to clipboard: {error}", flush=True)
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass
        return

    if system == "Darwin":
        try:
            png_data = BytesIO()
            image.save(png_data, "PNG")
            subprocess.run(
                ["osascript", "-e", "set the clipboard to (read (POSIX file \"/dev/stdin\") as PNG picture)"],
                input=png_data.getvalue(),
                check=True,
            )
            print("Image copied to clipboard.", flush=True)
        except Exception:
            print("Clipboard copy skipped on macOS. Screenshot was still saved.", flush=True)
        return

    print("Clipboard copy skipped: this platform is not supported.", flush=True)


def toggle_pause():
    """Pause or resume screenshot capture."""
    global paused
    paused = not paused
    if paused:
        print("\n--- Script paused. Press '\\' to resume. ---", flush=True)
    else:
        print("\n--- Script resumed. Capture is enabled. ---", flush=True)


def quit_script():
    """Stop the script."""
    global running
    print("\nEsc pressed. Shutting down the script...", flush=True)
    running = False


def get_coordinates_from_user():
    """Ask for the four coordinates for the capture region."""
    print("--- Please Enter Capture Region Coordinates ---")
    print("Use find_coordinates.py to find the correct values.")

    try:
        left_x = int(input("Enter the Top-Left X coordinate: "))
        top_y = int(input("Enter the Top-Left Y coordinate: "))
        right_x = int(input("Enter the Bottom-Right X coordinate: "))
        bottom_y = int(input("Enter the Bottom-Right Y coordinate: "))

        if left_x >= right_x or top_y >= bottom_y:
            print("\nError: left must be less than right, and top must be less than bottom.")
            sys.exit(1)

        return left_x, top_y, right_x, bottom_y

    except ValueError:
        print("\nError: invalid input. Please enter numbers only.")
        sys.exit(1)


def take_screenshots():
    """Set up hotkeys, then wait for user input."""
    left_x, top_y, right_x, bottom_y = get_coordinates_from_user()

    script_directory = Path(__file__).resolve().parent
    screenshot_folder_path = script_directory / SCREENSHOT_FOLDER_NAME
    screenshot_folder_path.mkdir(exist_ok=True)

    capture_width = right_x - left_x
    capture_height = bottom_y - top_y
    region_to_capture = (left_x, top_y, capture_width, capture_height)

    def capture_now():
        """Take one screenshot, save it, copy it to the clipboard, and run OCR."""
        if paused:
            print("\nCannot capture. Script is paused.", flush=True)
            return

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        save_path = screenshot_folder_path / filename

        try:
            screenshot = pyautogui.screenshot(region=region_to_capture)
            screenshot.save(save_path)
            print(f"\nCaptured screenshot: {filename}", flush=True)

            copy_image_to_clipboard(screenshot)

            print("--- OCR Result ---")
            extracted_text = pytesseract.image_to_string(Image.open(save_path))
            print(extracted_text)
            print("------------------")

        except pytesseract.TesseractNotFoundError:
            print("\n--- TESSERACT ERROR ---")
            print("Tesseract is not installed or was not found.")
            print("Install Tesseract, then set the TESSERACT_CMD environment variable if needed.")
            print("-----------------------")
        except Exception as error:
            print(f"\nAn error occurred during capture or OCR: {error}")

    keyboard.add_hotkey("`", capture_now)
    keyboard.add_hotkey("\\", toggle_pause)
    keyboard.add_hotkey("esc", quit_script)

    print("\n--- Capture Region Set ---")
    print(f"Top-Left: (X={left_x}, Y={top_y}), Bottom-Right: (X={right_x}, Y={bottom_y})")
    print("--------------------------")
    print("\n--- SCRIPT IS LIVE ---")
    print("Press '`' to capture and OCR, '\\' to pause/resume, and Esc to quit.")

    while running:
        time.sleep(0.1)

    print("\nScript has finished running.")


if __name__ == "__main__":
    take_screenshots()
