#------------------------------------------#
# CrossB Made by Miska Juro Studios (2025) #
#------------------------------------------#

import tkinter as tk
import ctypes
import os
import threading
import keyboard
import sys

# Gets releative path
if getattr(sys, 'frozen', False): # It's diffrent from .py and .exe
    rel_path = os.path.dirname(sys.executable)
else:
    rel_path = os.path.dirname(__file__)

settings_opened_once = False # I had to add this function, because if it wasn't there it's going to open the settings in loop

def LoadSettings():
    global CrossType, CrossKey, SettingsKey, ExitKey, OffsetX, OffsetY
    new = False
    directory = fr"{rel_path}\Settings" # Defines directory

    # (further in code) if not found, this will be left as a default
    CrossType = "White Crosshair" 
    CrossKey = "Shift+F8"
    SettingsKey = "Control+Shift+F8"
    ExitKey = "Escape+F8"
    OffsetX = 0
    OffsetY = 0

    # Path to saved files (from Settings/...)
    paths = {
        "CrossType": "CrossType.set",
        "CrossKey": "CrossKey.set",
        "SettingsKey": "SettingsKey.set",
        "ExitKey": "ExitKey.set",
        "OffsetX": "OffsetX.set",
        "OffsetY": "OffsetY.set"
    }

    for key, filename in paths.items(): # some kind of magic
        filepath = fr"{directory}\{filename}"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                value = f.read().strip()
                if key in ["OffsetX", "OffsetY"]:
                    try:
                        globals()[key] = int(value)
                    except ValueError:
                        globals()[key] = 0
                else:
                    globals()[key] = value
        else:
            new = True

    if new and not settings_opened_once:
        os.startfile(os.path.join(rel_path, "settings.exe"))
        globals()["settings_opened_once"] = True

LoadSettings()

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)


# gets the center of screen
size = 31
x = (screen_width - size) // 2 + OffsetX
y = (screen_height - size) // 2 + OffsetY

# initiliazises tkitner window
root = tk.Tk() 
root.overrideredirect(True)
root.attributes("-topmost", True)
bg_color = "#ffffff"
root.configure(bg=bg_color)
root.wm_attributes("-transparentcolor", bg_color)
root.geometry(f"{size}x{size}+{x}+{y}")

# this makes it, when for and example during and gameplay the mouse won't show after hovering this window
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080

current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
new_style = current_style | WS_EX_NOACTIVATE | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)

# Canvas for crosshair
canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0, bg=bg_color)
canvas.pack()

def draw_crosshair(cross_type): # This draws the crosshair (and settings)
    canvas.delete("all")
    center = size // 2
    color = "#f9f9f9"
    width = 1

    if "Red" in cross_type: # colors
        color = "red"
    elif "Blue" in cross_type:
        color = "#39a7f1"

    if "Thicker" in cross_type: # .. thicc?
        width = 3

    if "Dot" in cross_type: # types
        canvas.create_oval(center - 2, center - 2, center + 2, center + 2, fill=color, outline=color)
    if "Crosshair" in cross_type:
        canvas.create_line(center - 10, center, center + 10, center, fill=color, width=width)
        canvas.create_line(center, center - 10, center, center + 10, fill=color, width=width)

draw_crosshair(CrossType)

visible = True
def toggle_visibility(): # this toggles the visibility
    global visible
    if visible:
        root.withdraw()
    else:
        root.deiconify()
    visible = not visible

def listen_hotkeys(): # listening to key shortcuts
    keyboard.add_hotkey(CrossKey, toggle_visibility)
    keyboard.add_hotkey(SettingsKey, lambda: os.startfile(os.path.join(rel_path, "settings.exe")))
    keyboard.add_hotkey(ExitKey, lambda: os._exit(0))
    keyboard.wait()

threading.Thread(target=listen_hotkeys, daemon=True).start()

# Automatic recover settings
last_settings = {"CrossType": CrossType, "OffsetX": OffsetX, "OffsetY": OffsetY}

def periodic_refresh(): # this is propably really unoptimzed, but checks every 1000ms the settings (and changes them)
    global last_settings
    LoadSettings()

    if (CrossType != last_settings["CrossType"] or
        OffsetX != last_settings["OffsetX"] or
        OffsetY != last_settings["OffsetY"]):

        draw_crosshair(CrossType)
        new_x = (screen_width - size) // 2 + OffsetX
        new_y = (screen_height - size) // 2 + OffsetY
        root.geometry(f"{size}x{size}+{new_x}+{new_y}")

        last_settings = {
            "CrossType": CrossType,
            "OffsetX": OffsetX,
            "OffsetY": OffsetY
        }

    root.after(1000, periodic_refresh)

periodic_refresh()
root.mainloop()
