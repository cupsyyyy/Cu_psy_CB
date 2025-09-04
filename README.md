# Eventuri-AI

**Eventuri-AI** is a **colorbot with triggerbot** that integrates with **OBS NDI** to perform real-time detection and automation.

---

## Features

- **Colorbot**: detects specific colors on your screen and performs automatic actions.  
- **Triggerbot**: reacts instantly when a defined event occurs.  
- **OBS NDI Integration**: captures video feed directly from OBS using NDI.  
- **Easy Configuration**: customize bot behavior using JSON configuration files.  
- **Graphical Interface**: built with CustomTkinter for fast and intuitive control.

---

## Requirements

- **Python 3.12.0 or higher**  
- OBS Studio with the **NDI plugin** installed

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/Eventuri-AI.git
cd Eventuri-AI
```

2. **Start the run.bat**



## Configuration

1. Open `configs/BEST_CONFIG.json`.  
2. Set your preferred **colors**, **triggers**, and **behavior options**.  
3. Save the file.

---

## Usage

### Run via Python:

```bash
python src/Eventuri-AI.py
```

### Run via Windows batch script (`start.bat`):

```bat
@echo off
cd /d "%~dp0src"
call venv\Scripts\activate
python Eventuri-AI.py
pause
```

This will automatically activate your virtual environment and start the bot.

---

## Project Structure

```
Eventuri-AI/
├─ src/
│  ├─ Eventuri-AI.py
│  ├─ config.py
│  ├─ mouse.py
│  ├─ detection.py
│  └─ ...
├─ configs/
│  └─ BEST_CONFIG.json
├─ requirements.txt
└─ README.md
```

---

## Notes

- Make sure **Python 3.12.0+** is installed.  
- The virtual environment (`venv`) is recommended to avoid dependency conflicts.  
- OBS must be configured with the **NDI plugin** to work properly.  
- Always edit the configuration file before running the bot for proper behavior.

---

## License

MIT License

