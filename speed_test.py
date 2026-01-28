#!/usr/bin/env python3
# speed_test.py

import os
import sys
import speedtest
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    clear_screen()

    # 1. ANIMATION
    with console.status("[bold green]Testing network speed (fetching servers)...[/bold green]", spinner="dots"):
        try:
            # 2. GET DATA
            st = speedtest.Speedtest()
            
            st.get_best_server()
            
            # Bps -> Mbps
            download_speed = st.download() / 1024 / 1024
            upload_speed = st.upload() / 1024 / 1024
            ping = st.results.ping
            
            results = {
                "download": round(download_speed, 2),
                "upload": round(upload_speed, 2),
                "ping": round(ping, 2)
            }
            
        except Exception as e:
            console.print(f"\n[bold red]❌ Connection Error:[/bold red] {str(e)}")
            Prompt.ask("\n[dim]Press Enter to return...[/dim]")
            return

    # 3. SHOW RESULTS
    res_text = f"""
        [bold green]⬇️  Download:[/bold green]  {results['download']} Mbps
        [bold blue]⬆️  Upload:[/bold blue]    {results['upload']} Mbps
        [bold yellow]📶  Ping:[/bold yellow]      {results['ping']} ms
        """
    
    console.print(Panel(res_text, title="[bold cyan]Speed Results[/bold cyan]", border_style="cyan"))
    
    # 4. PAUSE
    Prompt.ask("\n[dim]Press Enter to return menu...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
