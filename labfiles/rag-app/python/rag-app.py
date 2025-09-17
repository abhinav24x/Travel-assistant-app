import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
from openai import AzureOpenAI

class TravelChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Luna Travel Assistant")
        self.root.geometry("750x550")
        self.root.configure(bg="#eaf2f8")

        # Load environment variables
        load_dotenv()
        self.open_ai_endpoint = os.getenv("OPENAI_ENDPOINT")
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        self.chat_model = os.getenv("CHAT_MODEL")
        self.embedding_model = os.getenv("EMBEDDING_MODEL")
        self.search_url = os.getenv("SEARCH_ENDPOINT")
        self.search_key = os.getenv("SEARCH_KEY")
        self.index_name = os.getenv("INDEX_NAME")

        if not self.open_ai_key or not self.open_ai_endpoint:
            messagebox.showerror("Configuration Error", "Missing API Key or Endpoint in .env file.")
            self.root.quit()

        # Initialize Azure OpenAI client
        try:
            self.chat_client = AzureOpenAI(
                api_version="2024-12-01-preview",
                azure_endpoint=self.open_ai_endpoint,
                api_key=self.open_ai_key
            )
        except Exception as ex:
            messagebox.showerror("Initialization Error", f"Failed to initialize AzureOpenAI: {ex}")
            self.root.quit()

        # Prompt history
        self.prompt = [
            {"role": "system", "content": "You are Luna, a friendly and knowledgeable travel assistant. "
            "Your job is to answer questions about countries, tourist attractions, hotels, food, culture, and travel tips. "
            "Use the information available in the search results (PDF data and index) as your main source. "
            "If you cannot find the answer, politely say that you don't have enough information."}
        ]

        # Title/Header
        header = tk.Label(
            self.root,
            text="Luna Travel Assistant",
            font=("Arial", 18, "bold"),
            bg="#000000",
            fg="Gold",
            pady=10
        )
        header.pack(fill=tk.X)

        # Chat Display Area
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state='disabled', 
            bg="white", fg="black", font=("Arial", 12),
            relief="flat", bd=0
        )
        self.chat_display.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        # Entry + Button Area
        self.entry_frame = tk.Frame(self.root, bg="#eaf2f8")
        self.entry_frame.pack(fill=tk.X, padx=15, pady=5)

        self.entry = tk.Entry(self.entry_frame, font=("Arial", 12), relief="solid", bd=1)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=5)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(
            self.entry_frame, text="Send", command=self.send_message,
            bg="#0078d7", fg="white", font=("Arial", 11, "bold"),
            relief="flat", padx=15, pady=5
        )
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg="#005a9e"))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg="#0078d7"))

        # Status Bar
        self.status_label = tk.Label(self.root, text="", font=("Arial", 9), bg="#eaf2f8", fg="gray")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        if user_input.lower() == "quit":
            self.root.quit()
            return

        self.display_message("You", user_input, "blue")
        self.entry.delete(0, tk.END)
        self.status_label.config(text="Thinking... ⏳")

        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()

    def process_message(self, user_input):
        try:
            self.prompt.append({"role": "user", "content": user_input})

            rag_params = {
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": self.search_url,
                            "index_name": self.index_name,
                            "authentication": {
                                "type": "api_key",
                                "key": self.search_key,
                            },
                            "query_type": "vector",
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": self.embedding_model,
                            },
                        }
                    }
                ],
            }

            response = self.chat_client.chat.completions.create(
                model=self.chat_model,
                messages=self.prompt,
                extra_body=rag_params
            )
            completion = response.choices[0].message.content
            self.display_message("Bot", completion, "green")
            self.prompt.append({"role": "assistant", "content": completion})
            self.status_label.config(text="")

        except Exception as ex:
            self.display_message("Error", f"Something went wrong: {ex}", "red")
            self.status_label.config(text="Error ❌")

    def display_message(self, sender, message, color):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: ", ("bold",))
        self.chat_display.insert(tk.END, f"{message}\n\n", (color,))
        self.chat_display.tag_configure("bold", font=("Arial", 12, "bold"))
        self.chat_display.tag_configure("blue", foreground="#0078d7")
        self.chat_display.tag_configure("green", foreground="#228B22")
        self.chat_display.tag_configure("red", foreground="red")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelChatApp(root)
    root.mainloop()
