from rich.columns import Columns
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.progress_bar import ProgressBar
import time
import psutil
import cpuinfo
import wmi

def data_unit_converter(data: float) -> str:
    if (data/(1024**3)) >= 1000:
        return f'{data/(1024**4):.2f} TB'
    elif (data/(1024**2)) >= 1000:
        return f'{data/(1024**3):.2f} GB'
    elif (data/(1024**1)) >= 1000:
        return f'{data/(1024**2):.2f} MB'
    else:
        return f'{data/1024:.2f} KB'

def cpu_info():
      cpu_info_dict = cpuinfo.get_cpu_info()

      return {'CPU_Name' : cpu_info_dict["brand_raw"],
              'Logical Processors': psutil.cpu_count(), 'Cores': psutil.cpu_count(logical=False),
              'Architecture': cpu_info_dict["arch"], 'Base Clock': cpu_info_dict["hz_advertised_friendly"]}

def mem_info():
      mem = psutil.virtual_memory()
      swap_mem = psutil.swap_memory()
      return {'total_swap': swap_mem.total, 'used_swap': swap_mem.used,
             'free_swap': swap_mem.free, 'avail_mem': mem.available,
             'total_mem': mem.total, 'used_mem': mem.used, 'mem_percent':mem.percent}

def disk_management():
    disk_info = psutil.disk_partitions()
    disk_data = {}
    for disk in disk_info:
        global disk_data_info
        disk_data_info = psutil.disk_usage(disk.mountpoint)
        disk_data[disk.device] = {
            'mount_point' : disk.mountpoint,
            'total_disk' : disk_data_info.total,
            'used_disk' : disk_data_info.used,
            'free_disk' : disk_data_info.free,
            }
    return disk_data

def ui_layout():
    header = Layout(name="header")
    header.split_column(
        Layout(name="upper"),
        Layout(name="Middle"),
        Layout(name="Lower")
    )

    def memory():
        data = cpu_info()
        header["upper"].size = 6
        header["upper"].update(Panel(
            (f"Logical Processors: {data.get('Logical Processors')}\nCores:{data.get('Cores')}"
             f"\nArchitecture: {data.get('Architecture')}\nBase Clock: {data.get('Base Clock')}"),
            title=data.get('CPU_Name'),
            title_align="left"
        )
        )

        mem_data = mem_info()
        header["Middle"].size = 7
        total = mem_data.get('total_mem')
        used = mem_data.get('used_mem')
        avail = mem_data.get('avail_mem')

        memory_panel_content = Group(
            f"Total Memory: {data_unit_converter(total)}",
            f"Available Memory: {data_unit_converter(avail)}",
            f"Used Memory: {data_unit_converter(used)}",
            ProgressBar(total=100, completed=(used / total) * 100)
        )

        header['Middle'].update(
            Panel(memory_panel_content, title="Memory", title_align="left")
        )
        return header

    def disk_ui():
        disk_info = disk_management()
        all_panels = []
        for drive, info in disk_info.items():
            used_percent = (info['used_disk']/info['total_disk'])*100
            disk_panel_content = Group(
                f"Drive: {info['mount_point']}",
                f"Total: {data_unit_converter(info['total_disk'])}",
                f"Used: {data_unit_converter(info['used_disk'])}",
                f"Free: {data_unit_converter(info['free_disk'])}",
                ProgressBar(total=100, completed=used_percent)
            )
            all_panels.append(Panel(disk_panel_content, width=30, padding=(0,1)))
        disk_panel = Panel(
            Columns(all_panels, expand=True, equal=False),
            title='Disk Info',
            title_align='left'
        )
        header['Lower'].update(disk_panel)


    with Live(header, refresh_per_second=4) as live:
        while True:
            memory()
            disk_ui()
            time.sleep(0.4)


if __name__ == '__main__':
    ui_layout()