from rich.console import Console

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
