#!/usr/bin/env python3
# main.py

import sys
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

import dashboard
import logger

console = Console()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_menu():
    clear_screen()
    
    menu_text = """
[bold cyan]1.[/bold cyan] 🖥️  Live Dashboard
[bold cyan]2.[/bold cyan] 📜 Simple Logger
[bold cyan]3.[/bold cyan] 🚪 Exit
    """
    
    rprint(Panel(menu_text, title="[bold green]🐧 TUXITOR MENU[/bold green]", subtitle="Select an option"))

def main():
    while True:
        show_menu()
        
        # Ask user for an input
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], default="1")
        
        try:
            if choice == "1":
                console.print("[green]Launching Dashboard...[/green]")
                time.sleep(0.5)
                dashboard.main()
                                
            elif choice == "2":
                console.print("[yellow]Starting Logger...[/yellow]")
                time.sleep(0.5)
                logger.main()
                
            elif choice == "3":
                console.print("[bold]See you later.[/bold]")
                sys.exit(0)
                
        except KeyboardInterrupt:
            # If CTRL+C inside a tool this return to the main menu.
            console.print("\n\n[bold yellow]Returning to Main Menu...[/bold yellow]")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
