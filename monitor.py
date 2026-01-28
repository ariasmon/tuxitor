# monitor.py
import psutil

def bytes_to_gb(bytes_value):
    # Converts bytes to GB
    if bytes_value == 0:
        return 0.00
    gb_value = bytes_value / (1024 ** 3)
    return round(gb_value, 2)

def get_cpu():
    # CPU usage
    return psutil.cpu_percent(interval=None)

def get_network():
    # Returns tuple with sent_gb and recv_gb
    io = psutil.net_io_counters()
    return bytes_to_gb(io.bytes_sent), bytes_to_gb(io.bytes_recv)

def get_memory():
    # Tuple with RAM data
    mem = psutil.virtual_memory()
    return bytes_to_gb(mem.used), bytes_to_gb(mem.total), mem.percent

def get_disk():
    # Tuple with the state of the disc with ‘/’
    disk = psutil.disk_usage('/')
    return bytes_to_gb(disk.used), bytes_to_gb(disk.total), disk.percent


