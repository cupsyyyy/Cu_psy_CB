# CUPSY_CB

**CUPSY_CB** is a **colorbot with triggerbot** that integrates with **OBS NDI** to perform real-time detection and automation.

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
git clone https://github.com/cupsyyyy/Cu_psy_CB.git
cd CUPSY_CB
```



## Usage

### Run via Windows batch script (`start.bat`):



This will automatically activate your virtual environment and start the CB!

---

## Project Structure

```
CUPSY_CB/
├─ src/
│  ├─ main.py
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
- OBS must be configured with the **NDI plugin** to work properly.  
- Always edit the configuration file before running the bot to be sure everything is setup.
- Some settings are only editable in the **config.py**, future changes are going to be made!
---

## License

MIT License

