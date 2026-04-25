import random

responses = {
    "hi": "Hello! How can I assist you today?",
    "appointment": "You can book an appointment on the Patient Dashboard.",
    "doctor": "You can find doctor schedules on the Doctor Dashboard.",
    "bye": "Goodbye! Have a great day."
}

def get_chatbot_response(user_message):
    return responses.get(user_message.lower(), "I'm not sure how to respond to that.")
