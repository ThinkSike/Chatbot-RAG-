import json
import requests

def load_conversation_history(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Could not find file: {file_path}")
        return {}

def get_huggingface_response(query_text):
    # Hugging Face model API for the BlenderBot
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    API_KEY = 'YOUR_HUGGINGFACE_API_KEY'  # Replace with your Hugging Face API key

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {"inputs": query_text}
    
    try:
        result = requests.post(API_URL, headers=headers, json=payload)
        result.raise_for_status()
        response_json = result.json()
        
        # Extracting generated response from the API response
        if response_json and 'generated_text' in response_json[0]:
            return response_json[0]['generated_text']
        else:
            return "Error: Unexpected response structure."
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
        return "Error: Unable to generate response."
    except Exception as error:
        print(f"An error occurred: {error}")
        return "Error: Unable to generate response."

def start_conversation(user_id, conversation_log):
    if user_id not in conversation_log:
        print("No conversation history found for this user.")
        return

    dialogue_history = conversation_log[user_id]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Session ended.")
            break

        dialogue_history.append({"user": f"({user_id}): {user_input}"})

        # Constructing the prompt with conversation history
        prompt_combined = "\n".join([f"{entry.get('user', '')} {entry.get('assistant', '')}" for entry in dialogue_history])
        
        # Generating response from Hugging Face model
        assistant_response = get_huggingface_response(prompt_combined)
        
        dialogue_history.append({"assistant": assistant_response})

        print(f"AI: {assistant_response}")

if __name__ == "__main__":
    conversation_log = load_conversation_history('chat_history.json')
    user_id = "-4567175683"
    start_conversation(user_id, conversation_log)
