import tkinter as tk
from tkinter import scrolledtext

def on_agree():
    # Function for handling agreement to consent
    print("Consent given. Starting experiment...")

def on_disagree(root):
    # Function for handling disagreement to consent
    root.destroy()

def on_scroll(event, txt_consent, btn_agree):
    # Function to handle the scroll event
    if txt_consent.yview()[1] == 1.0:
        btn_agree.pack(side=tk.LEFT, padx=20)

def setup_consent_screen(root):
    # Function to set up the informed consent screen
    consent_text = """Your consent text here"""

    txt_consent = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
    txt_consent.insert(tk.INSERT, consent_text)
    txt_consent.config(state=tk.DISABLED)  # Makes the text read-only
    txt_consent.pack(pady=10)
    txt_consent.bind("<MouseWheel>", lambda event: on_scroll(event, txt_consent, btn_agree))

    # Creating the Agree and Disagree buttons
    btn_agree = tk.Button(root, text="I Agree", command=on_agree)
    btn_disagree = tk.Button(root, text="I Disagree", command=lambda: on_disagree(root), bg='red', fg='white')
    btn_disagree.pack(side=tk.RIGHT, padx=20)

# This part ensures that the code below doesn't run when this file is imported
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fitts' Law Experiment: INFORMED CONSENT")
    root.geometry("700x400")  # width x height

    setup_consent_screen(root)
    root.mainloop()
