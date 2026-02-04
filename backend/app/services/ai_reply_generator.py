from groq import Groq
from app.config import settings

def generate_reply(subject: str, description: str, category: str):
    """
    Generates a support reply using Groq.
    """
    if not settings.GROQ_API_KEY or "your_groq_api_key" in settings.GROQ_API_KEY:
        return "Thank you for reaching out. We will get back to you shortly."

    client = Groq(api_key=settings.GROQ_API_KEY)
    
    prompt = f"""
    You are a helpful support agent. Write a polite and professional reply to the following ticket.
    
    Category: {category}
    Subject: {subject}
    Description: {description}
    
    Keep the reply concise (under 3 or 4 sentences) and reassuring.
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
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Reply Generation Error: {e}")
        return "Thank you for reaching out. We are reviewing your request."
