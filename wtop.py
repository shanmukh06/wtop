import psutil
import cpuinfo
import wmi


def data_unit_converter(data) -> float:
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

      return (f'CPU Name: {cpu_info_dict["brand_raw"]}'
              f'\nLogical Processors: {psutil.cpu_count()}\nCores: {psutil.cpu_count(logical=False)}\n'
              f'Architecture: {cpu_info_dict["arch"]}\n'
              f'Base Clock: {cpu_info_dict["hz_advertised_friendly"]:.2f}')

def mem_info():
      mem = psutil.virtual_memory()
      swap_mem = psutil.swap_memory()
      total_swap = swap_mem.total
      used_swap = swap_mem.used
      free_swap = swap_mem.free
      avail_mem = mem.available
      total_mem = mem.total
      used_mem = mem.used
      return (f'Total RAM: {data_unit_converter(total_mem)}\nAvailable RAM: {data_unit_converter(avail_mem)}\n'
              f'Used RAM: {data_unit_converter(used_mem)}\n'
              f'Total Swap: {data_unit_converter(total_swap)}\nUsed Swap: {data_unit_converter(used_swap)}\n'
              f'Free Swap: {data_unit_converter(free_swap)}')

def disk_management():
    disk_info = psutil.disk_partitions()
    for disk in disk_info:
        global disk_data_info
        disk_data_info = psutil.disk_usage(disk.device)
    total_disk = disk_data_info.total
    used_disk = disk_data_info.used
    free_disk = disk_data_info.free
    return (f'Total Disk Space: {data_unit_converter(total_disk)}\nUsed Disk Space: {data_unit_converter(used_disk)}'
            f'\nFree Disk Space: {data_unit_converter(free_disk)}')
