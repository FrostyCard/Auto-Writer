import tkinter as tk
import threading
import time
try:
    import keyboard
except ImportError:
    import os
    os.system("pip install keyboard")
    import keyboard


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Writer")
        self.root.geometry("500x250") 
        
        self.phrase = ""
        self.index = 0
        self.is_running = False
        self.delay = 100 
        
        # Label de status
        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Campo para velocidade
        tk.Label(root, text="Speed (ms between characters):").pack()
        self.delay_entry = tk.Entry(root, width=10)
        self.delay_entry.insert(0, "100")
        self.delay_entry.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Start (F3)", command=self.start_macro)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop (F4)", command=self.stop_macro)
        self.stop_button.pack(pady=5)
        
        self.top_var = tk.BooleanVar(value=True)
        self.top_checkbox = tk.Checkbutton(root, text="Always on top", variable=self.top_var, command=self.toggle_topmost)
        self.top_checkbox.pack(pady=5)
        self.root.attributes("-topmost", True)
        
        self.shift_enter_var = tk.BooleanVar(value=False)
        self.shift_enter_checkbox = tk.Checkbutton(root, text="Use Shit+Enter instead of only enter", variable=self.shift_enter_var)
        self.shift_enter_checkbox.pack(pady=5)
        
        keyboard.add_hotkey("F3", self.start_macro)
        keyboard.add_hotkey("F4", self.stop_macro)
    
    def toggle_topmost(self):
        self.root.attributes("-topmost", self.top_var.get())
    
    def start_macro(self):
        if not self.is_running:
            self.phrase = self.root.clipboard_get()
            self.index = 0
            try:
                self.delay = int(self.delay_entry.get())
            except ValueError:
                self.delay = 100
            
            self.is_running = True
            self.status_label.config(text="Status: Working", fg="green")
            threading.Thread(target=self.send_chars).start()
    
    def stop_macro(self):
        self.is_running = False
        self.status_label.config(text="Status: Stopped", fg="red")
        self.index = 0
    
    def send_chars(self):
        while self.is_running and self.index < len(self.phrase):
            char = self.phrase[self.index]
            
            if char == "\n" and self.shift_enter_var.get():
                keyboard.press("shift")
                keyboard.press("enter")
                keyboard.release("enter")
                keyboard.release("shift")
            else:
                keyboard.write(char)
            
            self.index += 1
            time.sleep(self.delay / 1000.0)
        self.stop_macro()


if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
