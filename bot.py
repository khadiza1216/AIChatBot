import tkinter as tk
from tkinter import scrolledtext
import threading
from groq import Groq

client = Groq(api_key="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")

COLORS = {
    "bg": "#1E82B0",
    "chat_bg": "#105980",
    "text": "#F0F2F5",
    "accent": "#0386F8",
    "user_msg": "#7C4DFF",
    "bot_msg": "#1E2329",
    "input_bg": "#424C5E",
    "border": "#2D4F7A"
}

def send_message():
    user_input = user_entry.get().strip()
    if not user_input:
        return

    if user_input.lower() in ["quit", "exit", "bye"]:
        window.quit()
        return

    chat_display.configure(state='normal')
    chat_display.insert(tk.END, "● YOU\n", "user_tag")
    chat_display.insert(tk.END, f"{user_input}\n\n", "text")
    chat_display.insert(tk.END, "● AI\n", "bot_tag")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)
    user_entry.delete(0, tk.END)

    threading.Thread(target=get_ai_response, args=(user_input,), daemon=True).start()

def get_ai_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                window.after(0, update_chat_display, content)
        
        window.after(0, update_chat_display, "\n\n")
    except Exception as e:
        window.after(0, update_chat_display, f"\nError: {str(e)}\n\n")

def update_chat_display(content):
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, content, "text")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)


window = tk.Tk()
window.title("My ChatBot")
window.geometry("1000x600")
window.configure(bg=COLORS["bg"])

chat_display = scrolledtext.ScrolledText(
    window, wrap=tk.WORD, state='disabled', 
    font=("Inter", 13), bg=COLORS["chat_bg"], 
    fg=COLORS["text"], insertbackground=COLORS["accent"],
    padx=20, pady=20, borderwidth=0, highlightthickness=1,
    highlightbackground=COLORS["border"]
)
chat_display.tag_configure("user_tag", foreground="#00D1FF", font=("Inter", 13, "bold"))
chat_display.tag_configure("bot_tag", foreground="#00D1FF", font=("Inter", 13, "bold"))
chat_display.tag_configure("text", foreground=COLORS["text"], spacing1=5)
chat_display.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)


input_frame = tk.Frame(window, bg=COLORS["bg"])
input_frame.pack(padx=20, pady=(0, 20), fill=tk.X)

user_entry = tk.Entry(
    input_frame, font=("Inter", 11), 
    bg=COLORS["input_bg"], fg=COLORS["text"], 
    insertbackground=COLORS["accent"], borderwidth=0, 
    highlightthickness=1, highlightbackground=COLORS["border"], 
    highlightcolor=COLORS["accent"]
)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12), ipady=10)
user_entry.bind("<Return>", lambda e: send_message())

send_button = tk.Button(
    input_frame, text="Send", command=send_message,
    bg=COLORS["accent"], fg="white", font=("Inter", 10, "bold"),
    activebackground="#6A3DE8", activeforeground="white",
    borderwidth=0, cursor="hand2", padx=25
)
send_button.pack(side=tk.RIGHT, ipady=7)

window.mainloop()
