# utils.py
import json
import difflib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List

# Load local medical knowledge base
from medical_knowledge import MEDICAL_KNOWLEDGE

def get_condition_info(condition: str = "") -> Dict:
    if not condition:
        return MEDICAL_KNOWLEDGE
    condition = condition.lower()
    for cond_name, cond_data in MEDICAL_KNOWLEDGE.items():
        if condition in cond_name.lower():
            return cond_data
        for alt in cond_data.get("alternate_names", []):
            if condition in alt.lower():
                return cond_data
    matches = difflib.get_close_matches(condition.title(), MEDICAL_KNOWLEDGE.keys(), n=1, cutoff=0.3)
    return MEDICAL_KNOWLEDGE[matches[0]] if matches else {
        "name": condition.title(),
        "overview": "Condition information not available",
        "symptoms": [],
        "treatments": ["Consult a healthcare provider"],
        "lifestyle_changes": [],
        "alternate_names": []
    }

def suggest_conditions(symptoms: str) -> List[str]:
    words = set(symptoms.lower().split())
    matches = []
    for condition, data in MEDICAL_KNOWLEDGE.items():
        cond_symptoms = set(s.lower() for s in data.get("symptoms", []))
        score = len(words & cond_symptoms)
        if score >= 1:
            matches.append((condition, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in matches]

def generate_treatment_guidance(condition: str) -> str:
    info = get_condition_info(condition)
    treatments = info.get("treatments", [])
    lifestyle = info.get("lifestyle_changes", [])
    response = [f"## Treatment Options for {condition.title()}", "### Medications:"]
    response += [f"- {t}" for t in treatments]
    response += ["", "### Lifestyle Recommendations:"]
    response += [f"- {l}" for l in lifestyle]
    return "\n".join(response)

def assess_emergency(symptoms: str) -> Dict:
    emergencies = {
        "chest pain": "Possible heart attack.",
        "difficulty breathing": "Possible respiratory emergency.",
        "severe bleeding": "Uncontrolled bleeding.",
        "paralysis": "Possible stroke.",
        "suicidal": "Mental health emergency."
    }
    symptoms_lower = symptoms.lower()
    for key, msg in emergencies.items():
        if key in symptoms_lower:
            return {"emergency": True, "message": msg}
    return {"emergency": False, "message": ""}

def generate_ai_chat_response(query: str) -> str:
    emergency = assess_emergency(query)
    if emergency["emergency"]:
        return f"🚨 **EMERGENCY**: {emergency['message']}\nPlease seek immediate medical attention."
    matches = suggest_conditions(query)
    if matches:
        result = ["Possible conditions:"]
        for cond in matches[:3]:
            info = get_condition_info(cond)
            result.append(f"- **{cond.title()}**: {info['overview']}")
        return "\n".join(result) + "\nThis is not a diagnosis."
    return "Please describe your symptoms in more detail."

def get_sample_patient_data(days=30):
    dates = pd.date_range(end=datetime.today(), periods=days)
    return pd.DataFrame({
        "Date": dates,
        "Heart Rate": np.random.normal(72, 5, days).astype(int),
        "Systolic BP": np.random.normal(120, 10, days).astype(int),
        "Diastolic BP": np.random.normal(80, 6, days).astype(int),
        "Blood Glucose": np.random.normal(95, 10, days).astype(int)
    })
