from rich.columns import Columns
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.progress_bar import ProgressBar
from datetime import datetime
import time
import psutil
import cpuinfo
import json
import GPUtil
import keyboard  # Used for non-blocking key detection

# 1. DATA GATHERING FUNCTIONS
def data_unit_converter(data: float) -> str:
    if (data / (1024 ** 3)) >= 1000:
        return f'{data / (1024 ** 4):.2f} TB'
    elif (data / (1024 ** 2)) >= 1000:
        return f'{data / (1024 ** 3):.2f} GB'
    elif (data / (1024 ** 1)) >= 1000:
        return f'{data / (1024 ** 2):.2f} MB'
    else:
        return f'{data / 1024:.2f} KB'

def cpu_static_info():
    info = cpuinfo.get_cpu_info()
    return {
        'Name': info.get("brand_raw", "Unknown CPU"),
        'L_Proc': psutil.cpu_count(),
        'Cores': psutil.cpu_count(logical=False),
        'Arch': info.get("arch", "Unknown")
    }

try:
    import pyamdgpuinfo
except ImportError:
    pyamdgpuinfo = None

def get_gpu_info():
    gpu_text = []
    # NVIDIA Check
    try:
        for gpu in GPUtil.getGPUs():
            gpu_text.append(f"NV {gpu.name}: {gpu.load*100:.1f}% | {gpu.temperature}C")
    except: pass
    # AMD Check
    if pyamdgpuinfo:
        try:
            for i in range(pyamdgpuinfo.get_gpu_count()):
                gpu = pyamdgpuinfo.get_gpu(i)
                gpu_text.append(f"AMD {gpu.name}: {gpu.query_load()}%")
        except: pass
    return gpu_text if gpu_text else ["No Dedicated GPU"]

# 2. LOGGING FUNCTION
def save_log(cpu, mem, disk, gpu):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_data = {
        "timestamp": timestamp,
        "cpu_usage": cpu,
        "memory": mem,
        "disks": disk,
        "gpu": gpu
    }
    filename = f"wtop_log_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(log_data, f, indent=4)
    return filename

# 3. UI LAYOUT & MAIN LOOP
def ui_layout():
    header = Layout(name="header")
    header.split_column(
        Layout(name="top_row", size=10),
        Layout(name="bottom_row", ratio=1)
    )
    header["top_row"].split_row(Layout(name="upper"), Layout(name="Middle"))
    header["bottom_row"].split_row(Layout(name="disk_box", ratio=2), Layout(name="gpu_box", ratio=1))

    static_cpu = cpu_static_info()
    last_log_msg = ""

    with Live(header, refresh_per_second=4, screen=True) as live:
        while True:
            # --- CPU ---
            cpu_usage = psutil.cpu_percent()
            cpu_content = f"L. Proc: {static_cpu['L_Proc']}\nCores: {static_cpu['Cores']}\nArch: {static_cpu['Arch']}\nUsage: [bold cyan]{cpu_usage}%[/bold cyan]"
            header["upper"].update(Panel(cpu_content, title=static_cpu['Name'], expand=True))

            # --- Memory ---
            m = psutil.virtual_memory()
            mem_content = Group(f"Total: {data_unit_converter(m.total)}", f"Used:  {data_unit_converter(m.used)}", ProgressBar(total=100, completed=m.percent))
            header["Middle"].update(Panel(mem_content, title="Memory", expand=True))

            # --- Disks ---
            drive_panels = []
            disk_stats = {}
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    if usage.total == 0: continue
                    d_content = Group(f"Drive: {part.mountpoint}", f"Used: {data_unit_converter(usage.used)}", ProgressBar(total=100, completed=usage.percent))
                    drive_panels.append(Panel(d_content, expand=True))
                    disk_stats[part.mountpoint] = usage.percent
                except: continue
            header["disk_box"].update(Panel(Columns(drive_panels, equal=True, expand=True), title="Storage"))

            # --- GPU & Logging ---
            gpu_list = get_gpu_info()
            if keyboard.is_pressed('s'):
                fname = save_log(cpu_usage, m.percent, disk_stats, gpu_list)
                last_log_msg = f"[bold green]Saved: {fname}[/bold green]"

            gpu_content = "\n".join(gpu_list) + f"\n\n{last_log_msg}\n[dim]Press 'S' to Log[/dim]"
            header["gpu_box"].update(Panel(gpu_content, title="GPU & Status", expand=True))

            time.sleep(0.4)

if __name__ == '__main__':
    ui_layout()