import psutil
import cpuinfo
import wmi

def cpu_info():
      cpu_info_dict = cpuinfo.get_cpu_info()

      return (f'CPU Name: {cpu_info_dict["brand_raw"]}'
              f'\nLogical Processors: {psutil.cpu_count()}\nCores: {psutil.cpu_count(logical=False)}\n'
              f'Architecture: {cpu_info_dict["arch"]}\n'
              f'Base Clock: {cpu_info_dict["hz_advertised_friendly"]:.2f}')

def mem_info():
      mem = psutil.virtual_memory()
      avail_mem = mem.available
      total_mem = mem.total
      used_mem = mem.used
      return (f'Total RAM: {total_mem/(1024**3):.2f} GB\nAvailable RAM: {avail_mem/(1024**3):.2f} GB\n'
              f'Used RAM: {used_mem/(1024**3):.2f} GB')

def disk_management():
    pass
