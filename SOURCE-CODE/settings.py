#------------------------------------------#
# CrossB Made by Miska Juro Studios (2025) #
#------------------------------------------#

import customtkinter as CTk
import sys
import os

# Gets releative path
if getattr(sys, 'frozen', False): # It's diffrent from .py and .exe
    rel_path = os.path.dirname(sys.executable)
else:
    rel_path = os.path.dirname(__file__)

rel_path_inner = os.path.dirname(__file__)

# initiliazises tkitner window
root = CTk.CTk()
root.geometry("350x430")
root.title("CrossB - Control Panel")
root._set_appearance_mode("dark")
root.iconbitmap(fr"{rel_path_inner}\Assets\CrossB.ico")


# This function stops users from typing into ComboBoxes (used in "eCrossType")
def block_typing(event):
    return "break" 

#----------------------#
#          UI          #
#----------------------#

# the Repeating elements are these-
#
#     etElement = ...
#     eElement = ...
#
# Basicly et- is a title (eg.: "Crosshair Type")
# and e- is the actuall element where you choose an option (eg.: "ComboBox")

eTitle = CTk.CTkLabel(master=root, text='CrossB Settings', font=('Constantia', 30))
eTitle.pack(anchor='s', pady=10)

etCrossType = CTk.CTkLabel(master=root, width=250, text='Crosshair Type')
etCrossType.pack(anchor='s')
eCrossType = CTk.CTkComboBox(master=root, width=250,
                             values=["White Dot", "Blue Dot", "Red Dot", "White Crosshair", "Blue Crosshair", "Red Crosshair", "White Crosshair Thicker", "Blue Crosshair Thicker", "Red Crosshair Thicker"])
eCrossType.pack(anchor='s')
eCrossType._entry.bind("<Key>", block_typing)

etBindKey = CTk.CTkLabel(master=root, width=250, text='Key to toggle Crosshair')
etBindKey.pack(anchor='s')
eBindKey = CTk.CTkEntry(master=root, width=250, placeholder_text="eg.: Shift+F8")
eBindKey.pack(anchor='s')

etBindKeySettings = CTk.CTkLabel(master=root, width=250, text='Key to open CrossB Settings')
etBindKeySettings.pack(anchor='s')
eBindKeySettings = CTk.CTkEntry(master=root, width=250, placeholder_text="eg.: Control+Shift+F8")
eBindKeySettings.pack(anchor='s')

etExitKey = CTk.CTkLabel(master=root, width=250, text='Key to quit CrossB')
etExitKey.pack(anchor='s')
eExitKey = CTk.CTkEntry(master=root, width=250, placeholder_text="eg.: Escape+F8")
eExitKey.pack(anchor='s')

etOffset = CTk.CTkLabel(master=root, width=250, text='Crosshair Offset Y and X')
etOffset.pack(anchor='s')
ecOffset = CTk.CTkFrame(master=root, fg_color="transparent")
ecOffset.pack(pady=5)

eOffsetY = CTk.CTkEntry(master=ecOffset, width=125, placeholder_text="(Y) eg.: 50")
eOffsetY.pack(side="left", padx=5)
eOffsetX = CTk.CTkEntry(master=ecOffset, width=125, placeholder_text="(X) eg.: -5")
eOffsetX.pack(side="left", padx=5)

# Save button, Calls function SaveSettings() - further in this program

eSaveSettings = CTk.CTkButton(master=root, width=250, text='Save', fg_color="#33a31a", hover_color="#2a8716", cursor="hand2",
                              command=lambda: SaveSettings(eCrossType.get(), eBindKey.get(), eBindKeySettings.get(), eExitKey.get(), eOffsetX.get(), eOffsetY.get()))
eSaveSettings.pack(anchor='s', pady=20)

# (↓↓↓ These two functions [LoadSettings and SaveSettings] are not really made efficent, I know that I cloud make ut just better... Yea I'm just lazy :D)

### LOAD FUNCTION ###
def LoadSettings():
    global CrossType, CrossKey, SettingsKey, ExitKey, OffsetX, OffsetY

    directory = fr"{rel_path}\Settings"

    # These are the default values, if there aren't found any saved ones.
    CrossType = "White crosshair"
    CrossKey = "Shift+F8"
    SettingsKey = "Control+Shift+F8"
    ExitKey = "Escape+F8"

    OffsetX = "0"
    OffsetY = "0"

    if os.path.exists(fr"{directory}\CrossType.set"): # this (and others) loads a file...
        with open(fr"{directory}\CrossType.set", "r") as f:
            CrossType = f.read()
    else:
        print("File 'CrossType.set' not found!")

    if os.path.exists(fr"{directory}\CrossKey.set"):
        with open(fr"{directory}\CrossKey.set", "r") as f:
            CrossKey = f.read()
    else:
        print("File 'CrossKey.set' not found!")
    
    if os.path.exists(fr"{directory}\SettingsKey.set"):
        with open(fr"{directory}\SettingsKey.set", "r") as f:
            SettingsKey = f.read()
    else:
        print("File 'SettingsKey.set' not found!")

    if os.path.exists(fr"{directory}\ExitKey.set"):
        with open(fr"{directory}\ExitKey.set", "r") as f:
            ExitKey = f.read()
    else:
        print("File 'ExitKey.set' not found!")
    


    if os.path.exists(fr"{directory}\OffsetX.set"):
        with open(fr"{directory}\OffsetX.set", "r") as f:
            OffsetX = f.read()
    else:
        print("File 'OffsetX.set' not found!")

    if os.path.exists(fr"{directory}\OffsetY.set"):
        with open(fr"{directory}\OffsetY.set", "r") as f:
            OffsetY = f.read()
    else:
        print("File 'OffsetY.set' not found!")


    eBindKey.insert(0, CrossKey)
    eBindKeySettings.insert(0, SettingsKey)
    eExitKey.insert(0, ExitKey)
    eCrossType.set(CrossType)

    eOffsetX.insert(0, OffsetX)
    eOffsetY.insert(0, OffsetY)

LoadSettings()

### SAVE FUNCTION ###
def SaveSettings(CrossType, BindKey, BindKeySettings, ExitKey, OffsetX, OffsetY):

    os.makedirs(fr"{rel_path}\Settings", exist_ok=True)

    with open(fr"{rel_path}\Settings\CrossType.set", "w") as f: # this (and others) writes the files
        f.write(CrossType)

    with open(fr"{rel_path}\Settings\CrossKey.set", "w") as f:
        f.write(BindKey)
    
    with open(fr"{rel_path}\Settings\SettingsKey.set", "w") as f:
        f.write(BindKeySettings)

    with open(fr"{rel_path}\Settings\ExitKey.set", "w") as f:
        f.write(ExitKey)

    with open(fr"{rel_path}\Settings\OffsetX.set", "w") as f:
        f.write(OffsetX)

    with open(fr"{rel_path}\Settings\OffsetY.set", "w") as f:
        f.write(OffsetY)

root.mainloop()
