import json
from rich.console import Console
from services.llm_service import analyze_message

console = Console()

def run_cli_test():
    with open("data/messages.json", "r") as f:
        messages = json.load(f)

    # If you only want to test the first 2 messages to save time, 
    # change the line below to: for msg in messages[:2]:
    for msg in messages:
        console.rule(f"[bold blue]Message ID: {msg['id']}")
        console.print(f"[italic]'{msg['message']}'[/italic]\n")
        
        # Displaying a clear spinner since CPU inference takes time
        with console.status("[bold cyan]Llama 3.1 is analyzing (this may take 30-60 seconds on CPU)...[/bold cyan]"):
            result = analyze_message(msg['message'])
        
        color = "green" if not result.needs_human else "red"
        console.print(result.model_dump_json(indent=2), style=color)
        console.print("\n")

if __name__ == "__main__":
    run_cli_test()