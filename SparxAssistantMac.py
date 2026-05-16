import pyautogui
import json
import os
import time
from datetime import datetime, timezone, timedelta
from pynput import keyboard as kb

# ------------------- Setup -------------------
target_click = (1772, 60)
W_POINT_2 = (1297, 978)
res_file = "res_log.json"

# Check resolution
if pyautogui.size() != (1920, 1080):
    pyautogui.alert("hey, i dont recognise ur res, i just need u to help me with some things real quick")

    # try loading saved position
    if os.path.exists(res_file):
        with open(res_file, "r") as f:
            data = json.load(f)
            W_POINT_2 = tuple(data.get("W_POINT_2", W_POINT_2))
    else:
        # ask user to set position
        pyautogui.alert("press E where the answer button for Sparx is")
        def on_press_e(key):
            global W_POINT_2
            try:
                if key.char.lower() == "e":
                    W_POINT_2 = pyautogui.position()
                    return False
            except AttributeError:
                pass
        with kb.Listener(on_press=on_press_e) as listener:
            listener.join()

        with open(res_file, "w") as f:
            json.dump({"W_POINT_2": W_POINT_2}, f)
        pyautogui.alert("Got it! Thanks!")

# ------------------- License Key Check -------------------
PASTEBIN_RAW = "https://pastebin.com/raw/6gWa1iNB"
LOCAL_LOG = "used_keys.json"
if not os.path.exists(LOCAL_LOG):
    with open(LOCAL_LOG, "w") as f:
        json.dump({}, f)

import requests
def validate_key():
    user_key = pyautogui.prompt("Enter your license key:")
    if not user_key:
        exit()
    try:
        data = requests.get(PASTEBIN_RAW, timeout=5).json()
    except Exception as e:
        pyautogui.alert(f"Failed to fetch key list: {e}")
        exit()
    keys = data.get("keys", {})
    if user_key not in keys:
        pyautogui.alert("Invalid key.")
        exit()
    key_data = keys[user_key]
    now = datetime.now(timezone.utc)
    with open(LOCAL_LOG, "r") as f:
        try:
            state = json.load(f)
        except:
            state = {}
    if isinstance(state.get(user_key), int):
        state[user_key] = {"used": state[user_key], "first_used": None}
    entry = state.get(user_key, {"used": 0, "first_used": None})

    # Handle expiration & multi-use logic...
    # [Keep your logic here, same as original]

    state[user_key] = entry
    with open(LOCAL_LOG, "w") as f:
        json.dump(state, f, indent=2)
    return True

validate_key()

pyautogui.alert("hi :D")
pyautogui.alert("press E where the google lens button is")

# Target click position
def on_press_target(key):
    global target_click
    try:
        if key.char.lower() == "e":
            target_click = pyautogui.position()
            return False
    except AttributeError:
        pass

with kb.Listener(on_press=on_press_target) as listener:
    listener.join()

pyautogui.alert("okay got it")
pyautogui.alert("press F8 to pause/unpause, F3 to exit")

# ------------------- Main Loop -------------------
paused = False

pressed_keys = set()

def on_press_main(key):
    global pressed_keys
    pressed_keys.add(key)

def on_release_main(key):
    global pressed_keys
    pressed_keys.discard(key)
    # Exit
    try:
        if key == kb.Key.f3:
            pyautogui.alert("bye")
            exit()
        if key == kb.Key.f8:
            global paused
            paused = not paused
            pyautogui.alert("paused" if paused else "unpaused")
    except:
        pass

listener = kb.Listener(on_press=on_press_main, on_release=on_release_main)
listener.start()

while True:
    if not paused:
        orig_x, orig_y = pyautogui.position()
        if kb.Key.space in pressed_keys:
            pyautogui.moveTo(*target_click)
            time.sleep(0.2)
            pyautogui.click()
            pyautogui.moveTo(orig_x, orig_y)

        if getattr(kb.KeyCode.from_char('w'), 'char', None) in [k.char for k in pressed_keys if hasattr(k,'char')]:
            pyautogui.moveTo(*W_POINT_2)
            pyautogui.click()
            time.sleep(0.3)
            pyautogui.moveTo(*target_click)
            pyautogui.click()
            pyautogui.moveTo(orig_x, orig_y)
            pyautogui.press("enter")

        if getattr(kb.KeyCode.from_char('q'), 'char', None) in [k.char for k in pressed_keys if hasattr(k,'char')]:
            pyautogui.moveTo(*W_POINT_2)
            pyautogui.click()
            time.sleep(0.7)
            pyautogui.moveTo(*W_POINT_2)
            pyautogui.click()
            pyautogui.moveTo(1663, 799)

    time.sleep(0.05)  # small delay to reduce CPU