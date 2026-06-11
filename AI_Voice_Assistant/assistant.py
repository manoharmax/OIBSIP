
import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import subprocess
import datetime
import psutil
import pyjokes
import socket
import threading
import platform

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = pyttsx3.init()

class VoiceAssistantPro:

    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("AI Voice Assistant Pro")
        self.app.geometry("1280x720")

        self.build_ui()
        self.update_dashboard()
        self.add_message("Assistant", "Welcome to AI Voice Assistant Pro")

    def add_message(self, sender, text):
        self.chat_box.insert("end", f"{sender}: {text}\n\n")
        self.chat_box.see("end")

    def speak(self, text):
        self.add_message("Assistant", text)
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    def process_command(self, command):
        cmd = command.lower().strip()

        if any(x in cmd for x in ["hello", "hi", "hey"]):
            return "Hello! How can I help you today?"

        if "how are you" in cmd:
            return "I am doing great and ready to assist you."

        if "who made you" in cmd:
            return "I was developed as an Oasis Infobyte internship project."

        if "what can you do" in cmd:
            return "I can search the web, open apps, provide system information and more."

        if "thank" in cmd:
            return "You are welcome."

        if "open google" in cmd:
            webbrowser.open("https://google.com")
            return "Opening Google"

        if "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"

        if "open github" in cmd:
            webbrowser.open("https://github.com")
            return "Opening GitHub"

        if "open gmail" in cmd:
            webbrowser.open("https://mail.google.com")
            return "Opening Gmail"

        if "open chatgpt" in cmd:
            webbrowser.open("https://chatgpt.com")
            return "Opening ChatGPT"

        if cmd.startswith("search "):
            q = cmd.replace("search ", "")
            webbrowser.open(f"https://www.google.com/search?q={q}")
            return f"Searching for {q}"

        if cmd.startswith("who is "):
            try:
                return wikipedia.summary(cmd.replace("who is ", ""), sentences=2)
            except:
                return "Wikipedia result not found."

        if "time" in cmd:
            return datetime.datetime.now().strftime("Current time is %I:%M %p")

        if "date" in cmd:
            return datetime.datetime.now().strftime("Today's date is %d %B %Y")

        if "day" in cmd:
            return datetime.datetime.now().strftime("Today is %A")

        if "battery" in cmd:
            b = psutil.sensors_battery()
            return f"Battery is {b.percent}%." if b else "Battery information unavailable."

        if "system" in cmd:
            return f"{platform.system()} {platform.release()}"

        if "username" in cmd:
            return f"Computer name is {socket.gethostname()}"

        if "joke" in cmd:
            return pyjokes.get_joke()

        if "open notepad" in cmd:
            subprocess.Popen("notepad.exe")
            return "Opening Notepad"

        if "open calculator" in cmd:
            subprocess.Popen("calc.exe")
            return "Opening Calculator"

        if "open command prompt" in cmd:
            subprocess.Popen("cmd.exe")
            return "Opening Command Prompt"

        if cmd in ["exit", "goodbye", "stop"]:
            self.app.destroy()
            return "Goodbye"

        return "Command not recognized. Try using the quick action buttons."

    def execute_command(self):
        cmd = self.command_entry.get().strip()
        if not cmd:
            return

        self.add_message("You", cmd)
        self.command_entry.delete(0, "end")

        response = self.process_command(cmd)
        self.speak(response)

    def listen(self):
        recognizer = sr.Recognizer()

        try:
            self.status_label.configure(text="🎤 Listening...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)

            text = recognizer.recognize_google(audio)

            self.command_entry.delete(0, "end")
            self.command_entry.insert(0, text)

            self.execute_command()

        except Exception:
            self.speak(
            "Microphone support is unavailable in this environment. Please use text commands."
        )

        self.status_label.configure(text="🟢 Ready")

    def start_listening(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def clear_chat(self):
        self.chat_box.delete("1.0", "end")

    def quick_action(self, command):
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, command)
        self.execute_command()

    def update_dashboard(self):
        battery = psutil.sensors_battery()
        battery_text = f"{battery.percent}%" if battery else "N/A"

        self.info_label.configure(
            text=(
                f"System: {platform.system()}\n"
                f"Battery: {battery_text}\n"
                f"Time: {datetime.datetime.now().strftime('%I:%M %p')}"
            )
        )

        self.app.after(30000, self.update_dashboard)

    def build_ui(self):

        sidebar = ctk.CTkFrame(self.app, width=260)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(
            sidebar,
            text="AI Assistant Pro",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.status_label = ctk.CTkLabel(sidebar, text="🟢 Ready")
        self.status_label.pack(pady=10)

        self.info_label = ctk.CTkLabel(sidebar, text="", justify="left")
        self.info_label.pack(pady=10)

        actions = [
            "Open Google",
            "Open YouTube",
            "Open GitHub",
            "Open Gmail",
            "Battery",
            "Time",
            "Tell me a joke"
        ]

        for action in actions:
            ctk.CTkButton(
                sidebar,
                text=action,
                command=lambda a=action: self.quick_action(a)
            ).pack(fill="x", padx=10, pady=5)

        main = ctk.CTkFrame(self.app)
        main.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.chat_box = ctk.CTkTextbox(main, font=("Consolas", 14))
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)

        bottom = ctk.CTkFrame(main)
        bottom.pack(fill="x", padx=10, pady=10)

        self.command_entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Enter command..."
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkButton(
            bottom,
            text="Execute",
            command=self.execute_command
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Listen",
            command=self.start_listening
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Clear Chat",
            command=self.clear_chat
        ).pack(side="left", padx=5)

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    VoiceAssistantPro().run()
