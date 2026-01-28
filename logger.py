#!/usr/bin/env python3
# logger.py

import time
import sys
import os
from collections import deque
import monitor

REFRESH_RATE = 1
MAX_ROWS = 20

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Last 20 registers
    log_history = deque(maxlen=MAX_ROWS)
    
    try:
        while True:
            cpu = monitor.get_cpu()
            ram_used, ram_total, ram_pct = monitor.get_memory()
            disk_used, disk_total, disk_pct = monitor.get_disk()
            net_sent, net_recv = monitor.get_network()

            line = (
                f"{cpu:<10} | "
                f"{ram_pct}% ({ram_used}/{ram_total})".ljust(18) + " | "
                f"{disk_pct}% ({disk_used}/{disk_total})".ljust(18) + " | "
                f"↑{net_sent} ↓{net_recv}"
            )
            
            log_history.append(line)
            
            # RENDER
            clear_screen()
            print("--- TUXITOR ROLLING LOG (LAST 20) ---")
            print("-" * 75)
            print(f"{'CPU (%)':<10} | {'RAM (GB)':<18} | {'DISK (GB)':<18} | {'NET (GB)':<15}")
            print("-" * 75)
            
            print("\n".join(log_history), flush=True)
            
            time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    monitor.get_cpu()
    main()
