import json
import os

test_cases = [
    {"id": 1, "msg": "My order #1234 still hasn't arrived and it's been two weeks.", "cat": "Delivery", "pri": "P1"},
    {"id": 2, "msg": "You charged me twice! Fix it now or I'm calling my lawyer.", "cat": "Billing", "pri": "P0"},
    {"id": 3, "msg": "Does the new Pro model come in blue?", "cat": "Product Inquiry", "pri": "P3"},
    {"id": 4, "msg": "I forgot my password and cannot access my invoices.", "cat": "Account", "pri": "P2"},
    {"id": 5, "msg": "The screen on the monitor I bought arrived cracked. I need a return label.", "cat": "Refund", "pri": "P2"},
    {"id": 6, "msg": "INVEST IN CRYPTO NOW! 1000x RETURNS! CLICK HERE!", "cat": "Spam", "pri": "P3"},
    {"id": 7, "msg": "The mobile app crashes every time I try to open the settings menu.", "cat": "Technical Support", "pri": "P2"},
    {"id": 8, "msg": "Your support agent was incredibly rude to me on the phone.", "cat": "Complaint", "pri": "P2"},
    {"id": 9, "msg": "What are your holiday store hours?", "cat": "General Inquiry", "pri": "P3"},
    {"id": 10, "msg": "Tracking says delivered, but there is no package on my porch.", "cat": "Delivery", "pri": "P1"},
    {"id": 11, "msg": "Can you email me a copy of my PDF invoice for last month?", "cat": "Billing", "pri": "P2"},
    {"id": 12, "msg": "URGENT: Someone hacked my account and is buying things with my saved card!", "cat": "Account", "pri": "P0"},
    {"id": 13, "msg": "I found an SQL injection vulnerability on your checkout page.", "cat": "Technical Support", "pri": "P0"},
    {"id": 14, "msg": "Hello?", "cat": "Other", "pri": "P3"},
    {"id": 15, "msg": "I want to cancel my subscription.", "cat": "Account", "pri": "P2"},
    {"id": 16, "msg": "Your new blender caught fire in my kitchen! This is extremely dangerous.", "cat": "Complaint", "pri": "P0"},
    {"id": 17, "msg": "How long is the warranty on the refurbished laptops?", "cat": "Product Inquiry", "pri": "P3"},
    {"id": 18, "msg": "You guys are literal garbage. I'm going to come down to your office and smash everything.", "cat": "Spam", "pri": "P0"},
    {"id": 19, "msg": "Do you sell digital gift cards?", "cat": "General Inquiry", "pri": "P3"},
    {"id": 20, "msg": "My system is completely down and our entire company cannot work. Major outage.", "cat": "Technical Support", "pri": "P1"}
]

messages = [{"id": tc["id"], "message": tc["msg"]} for tc in test_cases]
ground_truth = [{"id": tc["id"], "expected_category": tc["cat"], "expected_priority": tc["pri"]} for tc in test_cases]

os.makedirs("data", exist_ok=True)

with open("data/messages.json", "w") as f:
    json.dump(messages, f, indent=2)

with open("data/ground_truth.json", "w") as f:
    json.dump(ground_truth, f, indent=2)

print("20 test cases successfully generated in data/ directory!")