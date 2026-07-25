import json
import time
import sys
import os
import pandas as pd
from rich.console import Console

# Add root folder to python path to fix "ModuleNotFoundError: No module named 'services'"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.llm_service import analyze_message

console = Console()

def run_evaluation():
    with open("data/messages.json", "r") as f:
        all_messages = {msg['id']: msg['message'] for msg in json.load(f)}
    
    with open("data/ground_truth.json", "r") as f:
        ground_truth = {gt['id']: gt for gt in json.load(f)}

    results = []
    
    # Fast evaluation slice for CPU deadline constraint (first 5 messages)
    test_subset = list(all_messages.items())[:5]

    console.print(f"[bold yellow]Starting Evaluation Run ({len(test_subset)} messages)...[/bold yellow]\n")

    for msg_id, message_text in test_subset:
        expected = ground_truth.get(msg_id)
        if not expected: 
            continue

        console.print(f"Evaluating Message ID {msg_id} (processing via Llama 3.1)...")
        
        start_time = time.time()
        result = analyze_message(message_text)
        latency = time.time() - start_time

        category_match = result.category == expected['expected_category']
        priority_match = result.priority == expected['expected_priority']

        results.append({
            "ID": msg_id,
            "Cat Match": category_match,
            "Pri Match": priority_match,
            "Latency(s)": round(latency, 2),
            "Needs Human": result.needs_human
        })

    df = pd.DataFrame(results)
    cat_accuracy = (df["Cat Match"].sum() / len(df)) * 100
    pri_accuracy = (df["Pri Match"].sum() / len(df)) * 100
    avg_latency = df["Latency(s)"].mean()

    console.rule("[bold green]Final Evaluation Metrics")
    console.print(f"Category Accuracy: {cat_accuracy:.1f}%")
    console.print(f"Priority Accuracy: {pri_accuracy:.1f}%")
    console.print(f"Average Latency:   {avg_latency:.2f} seconds/message\n")
    
    console.print(df.to_string(index=False))

if __name__ == "__main__":
    run_evaluation()