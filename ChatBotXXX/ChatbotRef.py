'''
_____________________________code for Gemini(just in case)_______________________________

'''
import json
import requests

def get_chat_history(file_name):
    try:
        with open(file_name, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File {file_name} not found. Please check the file path.")
        return {}

def generate_ai_reply(user_prompt):
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    API_KEY = 'API_KEY_HERE'  # Replace with your actual API key

    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}]
    }
    
    try:
        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", headers=headers, json=payload)
        response.raise_for_status()
        json_response = response.json()
        
        if 'candidates' in json_response and 'content' in json_response['candidates'][0]:
            return json_response['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Unexpected response structure from API."
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't generate a response."

def chat_session(user_id, chat_history):
    if user_id not in chat_history:
        print("No conversation history found for this user.")
        return
    
    history = chat_history[user_id]
    
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            print("Goodbye!")
            break
        
        history.append({"human": f"(user_id: {user_id}): {user_message}"})
        
        prompt_text = "\n".join([f"{msg.get('human', '')} {msg.get('ai', '')}" for msg in history])
        
        ai_reply = generate_ai_reply(prompt_text)
        
        history.append({"ai": ai_reply})
        
        print(f"AI: {ai_reply}")

if __name__ == "__main__":
    chat_history_data = get_chat_history('chat_history.json')
    user_id = "-4567175683"
    chat_session(user_id, chat_history_data)
