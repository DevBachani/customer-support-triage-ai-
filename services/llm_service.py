import json
import re
import ollama
from pydantic import ValidationError
from models.schema import TriageResult
from prompts.system_prompt import build_system_prompt

def clean_json_response(raw_text: str) -> str:
    cleaned = re.sub(r"```json\s*", "", raw_text)
    cleaned = re.sub(r"```\s*", "", cleaned)
    return cleaned.strip()

def generate_fallback() -> TriageResult:
    return TriageResult(
        category="Other",
        priority="P0",
        summary="SYSTEM ERROR: LLM failed to extract valid JSON.",
        suggested_action="Review message manually.",
        confidence=0.0,
        needs_human=True,
        escalation_reason="Model output failed strict schema validation after retry."
    )

def analyze_message(message: str, max_retries: int = 1) -> TriageResult:
    system_prompt = build_system_prompt()
    
    for attempt in range(max_retries + 1):
        try:
            # 1. Turn stream=True
            response = ollama.chat(
                model='llama3.1',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': message}
                ],
                options={'temperature': 0.0},
                stream=True 
            )
            
            # 2. Print the chunks as they arrive
            print("\n[dim]Model is writing: [/dim]", end="", flush=True)
            raw_output = ""
            for chunk in response:
                text = chunk['message']['content']
                print(text, end="", flush=True)
                raw_output += text
            print("\n")
            
            json_string = clean_json_response(raw_output)
            
            parsed_data = json.loads(json_string)
            validated_result = TriageResult.model_validate(parsed_data)
            
            import config
            if validated_result.confidence < config.CONFIDENCE_THRESHOLD:
                validated_result.needs_human = True
                validated_result.escalation_reason = "Confidence below threshold"
                
            return validated_result
            
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"\nAttempt {attempt + 1} failed: {e}")
            if attempt == max_retries:
                return generate_fallback()