from django.shortcuts import render
from django.http import JsonResponse
import requests
import markdown
import json
from django.conf import settings

API_URL = "https://router.huggingface.co/v1/chat/completions"
API_KEY = settings.API_KEY
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct:novita"

DEFAULT_GREETING = {
    "role": "assistant", 
    "content": "<strong>Bot:</strong> Hi! How can I assist you today? 😊"
}

def query_huggingface(messages):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"model": MODEL_NAME, "messages": messages}
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "⚠️ Sorry, I couldn’t get a proper response from the model."


def chat_view(request):
    # Initialize with greeting if chat empty
    if "chat_history" not in request.session or not request.session["chat_history"]:
        request.session["chat_history"] = [DEFAULT_GREETING]

    chat_history = request.session["chat_history"]

    # AJAX Request (No Page Reload)
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        data = json.loads(request.body)
        user_input = data.get("message", "").strip()

        if user_input:
            # Add user message
            chat_history.append({"role": "user", "content": user_input})

            # Query AI Model
            reply = query_huggingface(chat_history)

            # Convert markdown to HTML
            formatted_reply = markdown.markdown(
                reply,
                extensions=["fenced_code", "tables", "nl2br"]
            )

            # Add bot reply
            chat_history.append({"role": "assistant", "content": formatted_reply})
            request.session["chat_history"] = chat_history

            return JsonResponse({"reply": formatted_reply})

        return JsonResponse({"reply": "❗ Please type something..."})

    # First page load → UI only
    return render(request, "chat/chat.html")


def clear_chat(request):
    request.session["chat_history"] = [DEFAULT_GREETING]
    return JsonResponse({"status": "cleared", "greeting": DEFAULT_GREETING["content"]})
