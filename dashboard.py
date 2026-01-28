#!/usr/bin/env python3
# dashboard.py

import time
import monitor
import process_manager

from rich.console import JustifyMethod
from rich.console import Console 
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich import box

# CONFIG
REFRESH_RATE = 1
console = Console()

def generate_sensor_table():
    # Creates the Upper Panel (CPU, RAM, Disk, Network)
    # Invisible table for layout
    table = Table(box=box.ROUNDED, expand=True, show_header=True)

    # Define columns
    table.add_column("CPU", justify='center', style='cyan')
    table.add_column("RAM", justify='center', style='magenta')
    table.add_column("DISK", justify='center', style="yellow")
    table.add_column("NET (Up/Down)", justify='center', style='green')

    # 1. GET DATA
    cpu = monitor.get_cpu()
    ram_used, ram_total, ram_pct = monitor.get_memory()
    disk_used, disk_total, disk_pct = monitor.get_disk()
    net_sent, net_recv = monitor.get_network()

    # 2. CONDITIONAL COLORS
    # Red and bold if CPU > 50%
    cpu_style = '[red bold]' if cpu > 50 else '[white]'
    
    # 3. ADD ROW
    table.add_row(
        f'{cpu_style}{cpu}%',
        f'{ram_pct}% ({ram_used}/{ram_total} GB)',
        f'{disk_pct}% ({disk_used}/{disk_total} GB)',
        f'{net_sent} ↓{net_recv} GB'
    )

    return Panel(table, title="[b]System Sensors[/b]", border_style='blue')

def generate_process_table():
    # Lower panel
    table = Table(box=box.SIMPLE, expand=True)
    
    table.add_column("PID", style='dim')
    table.add_column("Name", style='bold white')
    table.add_column("User", style='cyan')
    table.add_column("CORE %", style='purple')
    table.add_column("CPU %", justify='right', style='green')
    table.add_column("MEM %", justify='right', style='magenta')
    table.add_column("STRESS", justify='right', style='bold yellow')

    # 1. GET DATA
    procs = process_manager.get_top_processes(limit=25)

    for p in procs:
        user = p['username'] if p['username'] else "System"
        
        core_val = p['cpu_core'] or 0.0
        cpu_val = p['cpu_percent'] or 0.0
        mem_val = p['memory_percent'] or 0.0
        stress_val = p['stress']

        stress_style = '[red bold]' if stress_val > 50 else "[yellow bold]"

        table.add_row(
            str(p['pid']),
            p['name'],
            user,
            f'{core_val:.2f}%',
            f'{cpu_val:.2f}%',
            f'{mem_val:.2f}%',
            f'{stress_style}{stress_val:.2f}'
        )
    
    return Panel(table, title="[b]Most demanding processes[/b]", border_style='red')

def kill_mode_logic(layout):
    console.clear()
    
    # Static layout
    layout['upper'].update(generate_sensor_table())
    layout['lower'].update(generate_process_table())
    console.print(layout)

    console.print("\n[bold yellow]⏸️ PAUSED[/] - Enter PID to kill: ", end="")
    
    try:
        target = input()
        
        # RESUME
        if target.lower() in ['q', 'exit']:
            return True
        
        if not target:
            return True

        pid_int = int(target)
        
        # STOP
        with console.status(f"[red]Killing process {pid_int}...[/]"):
            success, message = process_manager.kill_process(pid_int)
            time.sleep(0.8)
        
        if success:
            console.print(f"✅ [bold green]SUCCESS:[/] {message}")
        else:
            console.print(f"❌ [bold red]ERROR:[/] {message}")
            
        console.input("[dim]Press Enter to resume live view...[/]")
        return True

    except ValueError:
        console.print("[red]Invalid PID. Must be a number.[/]")
        time.sleep(1)
        return True
    
    except KeyboardInterrupt:
        # Another CTRL+C to exit
        console.print()
        return False

def main():
    layout = Layout()

    # Split screen
    layout.split_column(
        Layout(name='upper', size=8),
        Layout(name='lower', size=20)
    )

    print("Starting dashboard...")

    running = True
    while running:
        try:
            with Live(layout, refresh_per_second=1, screen=True) as live:
                while True:
                    layout['upper'].update(generate_sensor_table())
                    layout['lower'].update(generate_process_table())
                    
                    live.update(layout)
                    time.sleep(REFRESH_RATE)
        
        except KeyboardInterrupt:
            # CTRL+C to enter the kill mode
            should_continue = kill_mode_logic(layout)
            if not should_continue:
                running = False
if __name__ == "__main__":
    try:
        monitor.get_cpu()
        main()
    except KeyboardInterrupt:
        pass
