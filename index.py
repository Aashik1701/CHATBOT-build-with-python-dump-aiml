import tkinter as tk
from tkinter import scrolledtext
import aiml
import nltk
from nltk.corpus import wordnet
import os
import re
import cv2
from PIL import Image, ImageTk

nltk.download('wordnet')

LIGHT_BG = 'white'
LIGHT_TEXT = 'black'
DARK_BG = 'black'
DARK_TEXT = 'white'

current_mode = 'light'

BRAIN_FILE = "new_brain.dump"

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

def get_bot_response(user_input):
    global current_mode
    if user_input.lower() == "change to dark mode":
        current_mode = 'dark'
        return "Switching to Dark Mode..."
    elif user_input.lower() == "change to light mode":
        current_mode = 'light'
        return "Switching to Light Mode..."
    else:
        pattern = r"(?: what is the meaning of)\s(.+)"
        match = re.match(pattern, user_input.lower())
        if match:
            word_to_define = match.group(1)
            meaning = get_word_meaning(word_to_define)
            return meaning if meaning else "Sorry, I couldn't find the meaning of that word."
        else:
            return k.respond(user_input)

def get_word_meaning(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    else:
        return None


def display_user_message(message):
    chat_history.insert(tk.END, f"You: {message}\n\n")
    chat_history.see(tk.END)

def display_bot_message(message):
    chat_history.insert(tk.END, f"Chatbot: {message}\n\n")
    chat_history.see(tk.END)

def apply_theme(theme_mode):
    global LIGHT_BG, LIGHT_TEXT, DARK_BG, DARK_TEXT
    if theme_mode == 'light':
        # Apply light mode colors
        window.config(bg=LIGHT_BG)
        chat_history.config(bg=LIGHT_BG, fg=LIGHT_TEXT)
        input_entry.config(bg=LIGHT_BG, fg=LIGHT_TEXT)
        send_button.config(bg="lightblue", fg="white")
    elif theme_mode == 'dark':
        # Apply dark mode colors
        window.config(bg=DARK_BG)
        chat_history.config(bg=DARK_BG, fg=DARK_TEXT)
        input_entry.config(bg=DARK_BG, fg=DARK_TEXT)
        send_button.config(bg="darkblue", fg="white")

def send_message(event=None):
    user_input = input_entry.get()
    if user_input.strip() != "":
        display_user_message(user_input)
        bot_response = get_bot_response(user_input)
        display_bot_message(bot_response)
        # Check if user wants to change theme mode
        if current_mode in ['light', 'dark']:
            apply_theme(current_mode)
    input_entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("Chatbot")
window.config(bg=LIGHT_BG)

label= tk.Label(window,text="Welcome to ChatBot™  ☻",font=("Ravie",34))
label.pack(pady=10)

# Create a scrolled text widget for chat history
chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
chat_history.pack(expand=True, fill='both', padx=10, pady=10)

# Create an entry field for user input
input_entry = tk.Entry(window, font=("Arial", 12))
input_entry.pack(fill=tk.BOTH, padx=10, pady=10)
input_entry.bind("<Return>", send_message)

# Create a send button
send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 12), bg="lightblue", fg="white")
send_button.pack(pady=10)

# Start the main event loop
window.mainloop()
