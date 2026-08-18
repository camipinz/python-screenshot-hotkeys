import time

import pyautogui


def main():
    print("Coordinate Finder Tool")
    print("----------------------")
    print("Move your mouse cursor to the position you want to find.")
    print("The X and Y coordinates will be displayed below.")
    print("Press Ctrl+C in this terminal to quit the script when you're done.")

    try:
        while True:
            x, y = pyautogui.position()
            position_string = f"X: {str(x).rjust(4)}  Y: {str(y).rjust(4)}"

            print(position_string, end="")
            print("\b" * len(position_string), end="", flush=True)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nDone. You can now use the coordinates you noted.")


if __name__ == "__main__":
    main()
