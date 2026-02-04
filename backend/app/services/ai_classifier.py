from groq import Groq
import json
from app.config import settings

def classify_ticket(subject: str, description: str):
    """
    Classifies a ticket using Groq (Llama3-8b-8192 or similar).
    Returns a dict with 'priority' and 'category'.
    """
    if not settings.GROQ_API_KEY or "your_groq_api_key" in settings.GROQ_API_KEY:
         # Fallback mock if key is not set
        return {"priority": "Medium", "category": "General"}

    client = Groq(api_key=settings.GROQ_API_KEY)
    
    prompt = f"""
    You are a support ticket classifier.
    Analyze the following ticket and return a JSON object with 'priority' (High, Medium, Low) and 'category' (Bug, Feature, Billing, General).
    
    Ticket Subject: {subject}
    Ticket Description: {description}
    
    Output JSON only:
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            response_format={"type": "json_object"},
        )
        
        result_content = chat_completion.choices[0].message.content
        return json.loads(result_content)
    except Exception as e:
        print(f"Groq Classification Error: {e}")
        return {"priority": "Medium", "category": "General"}
