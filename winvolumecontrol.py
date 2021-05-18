import winhotkeys
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

CHANGE_AMOUNT = .02
IGNORE_PROCESSES = ["discord.exe"]

def change_app_volume(amount):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if not session.Process or session.Process.name().lower() not in IGNORE_PROCESSES:
            current_volume = volume.GetMasterVolume()
            new_volume = max(0, min(1, current_volume + amount))
            volume.SetMasterVolume(new_volume, None)

def handle_win_f3():
    print("Volume down")
    change_app_volume(-CHANGE_AMOUNT)

def handle_win_f4():
    print("Volume up")
    change_app_volume(CHANGE_AMOUNT)

HOTKEYS = {
    (winhotkeys.VK_F3, winhotkeys.MOD_WIN): handle_win_f3,
    (winhotkeys.VK_F4, winhotkeys.MOD_WIN): handle_win_f4
}

def main():
    winhotkeys.handle_hotkeys(HOTKEYS)

if __name__ == "__main__":
    main()
