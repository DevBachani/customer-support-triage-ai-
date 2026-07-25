CATEGORIES = [
    "Billing", "Delivery", "Technical Support", "Account", 
    "Refund", "Complaint", "Product Inquiry", "General Inquiry", 
    "Spam", "Other"
]

PRIORITIES = {
    "P0": "Critical (security, fraud, legal threats, safety issues)",
    "P1": "Urgent customer-impacting issues (missing order, duplicate charge, major outage)",
    "P2": "Normal support requests (bugs, complaints, returns, damaged items)",
    "P3": "Low priority (general questions, feedback, product information)"
}

ESCALATION_TRIGGERS = [
    "Confidence below threshold",
    "Legal issues",
    "Threats",
    "Abuse",
    "Multiple conflicting issues",
    "Ambiguous messages",
    "Model unable to classify confidently"
]

CONFIDENCE_THRESHOLD = 0.85