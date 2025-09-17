# commands.py
import subprocess
import time
import os
import platform

# optional: pyautogui for typing (install in backend venv)
try:
    import pyautogui
except Exception:
    pyautogui = None

def _open_notepad_windows():
    try:
        subprocess.Popen(["notepad.exe"])
        return True, None
    except Exception as e:
        return False, str(e)

def _type_text(text, delay_after_open=1.2):
    if pyautogui is None:
        return False, "pyautogui not installed or unavailable."

    # try to open notepad if not already
    if platform.system() == "Windows":
        try:
            subprocess.Popen(["notepad.exe"])
        except Exception:
            pass

    time.sleep(delay_after_open)
    try:
        pyautogui.typewrite(text, interval=0.03)
        return True, None
    except Exception as e:
        return False, str(e)

def _open_browser(url="https://www.google.com"):
    try:
        # cross-platform opener
        if platform.system() == "Windows":
            os.startfile(url)
        else:
            subprocess.Popen(["xdg-open", url])
        return True, None
    except Exception as e:
        return False, str(e)

def _open_calculator():
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["calc.exe"])
        else:
            # best effort for linux/mac
            subprocess.Popen(["gnome-calculator"])
        return True, None
    except Exception as e:
        return False, str(e)

def handle_command(message: str):
    """
    Return dict {"executed": True, "response": "..."} if a local command was detected & executed.
    Otherwise return None.
    """

    if not message or not isinstance(message, str):
        return None

    msg = message.lower().strip()

    # OPEN NOTEPAD
    if "open notepad" in msg:
        ok, err = _open_notepad_windows()
        if ok:
            return {"executed": True, "response": "Opening Notepad..."}
        return {"executed": True, "response": f"Failed to open Notepad: {err}"}

    # TYPE <text>  -> exact phrase "type hello world"
    if msg.startswith("type "):
        text_to_type = message[len("type "):].strip()
        ok, err = _type_text(text_to_type)
        if ok:
            return {"executed": True, "response": f"Typed: {text_to_type}"}
        return {"executed": True, "response": f"Failed to type: {err}"}

    # OPEN BROWSER
    if "open browser" in msg or "open google" in msg:
        ok, err = _open_browser("https://www.google.com")
        if ok:
            return {"executed": True, "response": "Opening browser..."}
        return {"executed": True, "response": f"Failed to open browser: {err}"}

    # OPEN CALCULATOR
    if "open calculator" in msg or "open calc" in msg:
        ok, err = _open_calculator()
        if ok:
            return {"executed": True, "response": "Opening Calculator..."}
        return {"executed": True, "response": f"Failed to open Calculator: {err}"}

    # VOLUME (best-effort via pyautogui; may require additional keys)
    if "volume up" in msg:
        if pyautogui:
            try:
                pyautogui.press("volumeup")
                return {"executed": True, "response": "Volume increased."}
            except Exception as e:
                return {"executed": True, "response": f"Volume command failed: {e}"}
        return {"executed": True, "response": "pyautogui not available for volume control."}

    if "volume down" in msg:
        if pyautogui:
            try:
                pyautogui.press("volumedown")
                return {"executed": True, "response": "Volume decreased."}
            except Exception as e:
                return {"executed": True, "response": f"Volume command failed: {e}"}
        return {"executed": True, "response": "pyautogui not available for volume control."}

    if "mute" in msg:
        if pyautogui:
            try:
                pyautogui.press("volumemute")
                return {"executed": True, "response": "Muted."}
            except Exception as e:
                return {"executed": True, "response": f"Mute command failed: {e}"}
        return {"executed": True, "response": "pyautogui not available for mute control."}

    # LOCK PC
    if "lock pc" in msg or "lock workstation" in msg:
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return {"executed": True, "response": "Locking your PC..."}
            return {"executed": True, "response": "Lock command not supported on this platform."}
        except Exception as e:
            return {"executed": True, "response": f"Lock failed: {e}"}

    # SHUTDOWN (DESCTRUCTIVE) - DO NOT ENABLE UNLESS YOU KNOW RISKS
    if "shutdown pc" in msg or "turn off pc" in msg:
        return {"executed": True, "response": "Shutdown command is disabled for safety."}

    # No command matched
    return None
