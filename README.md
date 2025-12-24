# wtop

**wtop** is a lightweight, high-performance terminal dashboard built in Python for real-time system monitoring. It features a compact, side-by-side UI layout designed to provide a comprehensive view of hardware health with minimal screen real estate.

## 🚀 Features
* **Real-time Dashboard:** Uses `rich.live` for smooth, multi-panel terminal rendering.
* **Optimized Performance:** Fetches static hardware data (CPU name, architecture) once at startup to reduce I/O overhead and CPU footprint.
* **Side-by-Side Layout:** A custom nested grid structure that maximizes horizontal space for CPU, Memory, and Storage metrics.
* **Cross-Vendor GPU Support:** Integrated monitoring for both **NVIDIA** (via `GPUtil`) and **AMD** (via `pyamdgpuinfo`) hardware.
* **Research Logging:** Press `S` to export a time-stamped system snapshot to a `.json` file for data analysis and experiment tracking.

## 💻 Platforms
* **Windows:** Fully optimized (Tested on Microsoft Surface Laptop).
* **Linux:** Core metrics supported; advanced GPU/Layout features in progress.

## 🛠️ Modules Used
* **[rich](https://github.com/Textualize/rich):** TUI layout, progress bars, and live rendering.
* **[psutil](https://github.com/giampaolo/psutil):** Core system metrics (CPU, RAM, Disk).
* **[py-cpuinfo](https://github.com/workhorse/py-cpuinfo):** Detailed hardware specifications.
* **[GPUtil](https://github.com/anderskm/gputil):** NVIDIA GPU monitoring.
* **[pyamdgpuinfo](https://github.com/Svechnikov/pyamdgpuinfo):** AMD GPU monitoring.
* **[keyboard](https://github.com/boppreh/keyboard):** Non-blocking hotkey detection for logging.

## 📥 Installation & Usage
1. **Install dependencies:**
   Ensure you have a `requirements.txt` file in your directory, then run:
   ```bash
   pip install -r requirements.txt
   ```
2. **Clone the repository and install dependencies:**
   ```bash
   pip install rich psutil py-cpuinfo gputil pyamdgpuinfo keyboard
    ```
3. **Run the Application**
    ```bash
   python wtop.py
   ```
4. Hotkeys:

* `S`: Export current system stats to a JSON log.
* `Ctrl+C`: Exit the application.