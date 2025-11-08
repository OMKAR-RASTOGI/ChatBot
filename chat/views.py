
from django.shortcuts import render, redirect
import requests
import markdown  
import os
from django.conf import settings

API_URL = "https://router.huggingface.co/v1/chat/completions"
API_KEY = settings.API_KEY
print("sndfvk:::",API_KEY)
MODEL_NAME = "moonshotai/Kimi-K2-Thinking:novita"

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
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    chat_history = request.session["chat_history"]

    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()
        if user_input:
            chat_history.append({"role": "user", "content": user_input})
            reply = query_huggingface(chat_history)

            # ✅ Convert markdown (AI response) to HTML for display
            formatted_reply = markdown.markdown(
                reply,
                extensions=["fenced_code", "tables", "nl2br"]
            )

            chat_history.append({"role": "assistant", "content": formatted_reply})
            request.session["chat_history"] = chat_history
        return redirect("chat")

    return render(request, "chat/chat.html", {"chat_history": chat_history})

def clear_chat(request):
    request.session["chat_history"] = []
    return redirect("chat")
