import tkinter as tk
from datetime import datetime, timedelta
from chatbot_core import find_best_match  # Connect backend

class AILegalAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Legal Assistant")
        self.root.geometry("500x600")
        self.root.configure(bg="#f5f7fa")

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        top_bar = tk.Frame(self.root, bg="#1f2937", height=60)
        top_bar.pack(fill=tk.X)

        avatar = tk.Label(top_bar, text="🧑‍⚖️", bg="#1f2937", font=("Arial", 18))
        avatar.pack(side=tk.LEFT, padx=10)

        title = tk.Label(top_bar, text="AI Lawyer", fg="white", bg="#1f2937", font=("Arial", 14, "bold"))
        title.pack(side=tk.LEFT)

        self.clock_label = tk.Label(top_bar, fg="white", bg="#1f2937", font=("Arial", 12))
        self.clock_label.pack(side=tk.RIGHT, padx=10)

        self.chat_frame = tk.Text(self.root, wrap=tk.WORD, bg="#f9fbfc", fg="#000", font=("Arial", 12), state=tk.DISABLED)
        self.chat_frame.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

        self.chat_frame.config(state=tk.NORMAL)
        self.chat_frame.tag_configure("center", justify='center')
        self.chat_frame.tag_configure("welcome", font=("Arial", 16, "bold"))
        self.chat_frame.tag_configure("time", font=("Arial", 10), foreground="#888")
        self.chat_frame.insert(tk.END, "\n\nHow can I assist you today?\n\n", ("center", "welcome"))
        self.chat_frame.config(state=tk.DISABLED)

        input_frame = tk.Frame(self.root, bg="white")
        input_frame.pack(pady=10)

        center_inner_frame = tk.Frame(input_frame, bg="white")
        center_inner_frame.pack()

        self.input_entry = tk.Entry(center_inner_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE, width=32)
        self.input_entry.grid(row=0, column=0, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(center_inner_frame, text="Send", font=("Arial", 12), bg="#0a84ff", fg="white", command=self.send_message)
        send_button.grid(row=0, column=1)

    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime('%I:%M %p')
        self.clock_label.config(text=time_str)
        self.root.after(1000, self.update_clock)

    def send_message(self, event=None):
        message = self.input_entry.get().strip()
        if message == "":
            return

        timestamp = (datetime.now() + timedelta(minutes=2)).strftime('%I:%M %p')

        response = find_best_match(message)  # ✅ Fetch backend response

        self.chat_frame.config(state=tk.NORMAL)
        self.chat_frame.insert(tk.END, f"You: {message}\n", "user")
        self.chat_frame.insert(tk.END, f"{timestamp}\n", "time")
        self.chat_frame.insert(tk.END, f"Bot: {response}\n\n", "bot")
        self.chat_frame.config(state=tk.DISABLED)
        self.chat_frame.see(tk.END)

        self.input_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AILegalAssistantApp(root)
    root.mainloop()
