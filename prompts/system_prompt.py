import json
import config
from models.schema import TriageResult

def build_system_prompt() -> str:
    schema_json = json.dumps(TriageResult.model_json_schema(), indent=2)
    
    return f"""You are an expert customer support triage AI. 
Analyze the customer message and extract the required information.

CATEGORIES ALLOWED:
{', '.join(config.CATEGORIES)}

PRIORITY DEFINITIONS:
- P0: {config.PRIORITIES['P0']}
- P1: {config.PRIORITIES['P1']}
- P2: {config.PRIORITIES['P2']}
- P3: {config.PRIORITIES['P3']}

ESCALATION RULES:
Set 'needs_human' to true and provide an 'escalation_reason' if the message contains:
{', '.join(config.ESCALATION_TRIGGERS)}

INSTRUCTIONS:
1. Output ONLY raw, valid JSON. Do not include markdown formatting like ```json.
2. Do not include any conversational text before or after the JSON.
3. Strictly adhere to this JSON schema:
{schema_json}
"""