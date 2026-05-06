from rich.console import Console

from .events import Event
from moxchange.types import Kline

console = Console(highlight=False)


class CLI:
    """Command-line interface for Moxchange."""

    def print_banner(self, version: str, port: int) -> None:
        """Prints the Moxchange banner with version and connection info."""
        ascii_art = "                      __                        \n  __ _  ___ __ ______/ /  ___ ____  ___ ____    \n /  ' \\/ _ \\\\ \" / __/ _ \\/ _ `/ _ \\/ _ `/ -_)   \n/_/_/_/\\___/_\\_\\\\__/_//_/\\_,_/_//_/\\_, /\\__/    \n                                  /___/         \n"
        console.print(ascii_art, style="cyan")
        console.print(
            f"Version: [cyan]{version}[/cyan] | Created by [cyan]februu[/cyan]"
        )
        console.print("Repository: [cyan]https://github.com/februu/moxchange[/cyan]")
        console.print("Docs: [cyan]https://febru.dev/moxchange[/cyan]\n")
        console.print(
            f"⚡ Connect your client here: [green]127.0.0.1:{port}/ws[/green]\n"
        )

    def on_candle_event(self, event: Event) -> None:
        """Handles candle events."""

        candle: Kline = event.payload

        direction = "▲" if candle.is_bullish() else "▼"
        color = "green" if candle.is_bullish() else "red"
        change_pct = ((candle.close - candle.open) / candle.open) * 100

        console.print(
            f"[{color}]{direction}[/{color}]  "
            f"[dim]{candle.timestamp}[/dim]\t"
            f"[dim]O:[/dim][{color}]{candle.open:<10}[/{color}] \t"
            f"[dim]H:[/dim][{color}]{candle.high:<10}[/{color}] \t"
            f"[dim]L:[/dim][{color}]{candle.low:<10}[/{color}] \t"
            f"[dim]C:[/dim][{color}]{candle.close:<10}[/{color}]"
            f"[bold {color}]\t{change_pct:+.2f}%[/bold {color}]"
        )
