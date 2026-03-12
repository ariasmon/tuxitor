# monitor.py
import psutil
import time

# Store the last network counters and time to calculate speed
last_net_io = psutil.net_io_counters()
last_time = time.time()

def bytes_to_gb(bytes_value):
    # Converts bytes to GB
    if bytes_value == 0:
        return 0.00
    gb_value = bytes_value / (1024 ** 3)
    return round(gb_value, 2)

def bytes_to_mb(bytes_value):
    # Converts bytes to MB
    if bytes_value == 0:
        return 0.00
    mb_value = bytes_value / (1024 ** 2)
    return round(mb_value, 2)

def get_cpu():
    # CPU usage
    # Setting interval to 0.1 allows psutil to measure the delta correctly
    return psutil.cpu_percent(interval=0.1)

def get_network():
    # Returns tuple with sent_mb/s and recv_mb/s
    global last_net_io, last_time
    
    # Get current counters and time
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    
    # Calculate the time difference
    elapsed_time = current_time - last_time
    if elapsed_time <= 0:
        elapsed_time = 1
    
    # Calculate speed: (current_bytes - last_bytes) / elapsed_time
    sent_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / elapsed_time
    recv_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / elapsed_time
    
    # Update global variables for the next call
    last_net_io = current_net_io
    last_time = current_time
    
    # Return formatted speeds in MB/s
    return bytes_to_mb(sent_speed), bytes_to_mb(recv_speed)

def get_memory():
    # Tuple with RAM data
    mem = psutil.virtual_memory()
    return bytes_to_gb(mem.used), bytes_to_gb(mem.total), mem.percent

def get_disk():
    # Tuple with the state of the disc with ‘/’
    disk = psutil.disk_usage('/')
    return bytes_to_gb(disk.used), bytes_to_gb(disk.total), disk.percent
