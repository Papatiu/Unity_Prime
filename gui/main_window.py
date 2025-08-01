# gui/main_window.py
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame
import sys
import threading
from core.logic.prompt_handler import process_and_execute_prompt

class PrimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unity AI PRIME v1.0")
        self.root.geometry("800x600")

        # Ana Frame
        main_frame = Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Log alanı (ScrolledText)
        self.log_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=25, state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Redirect stdout (print çıktılarını log alanına yönlendirme)
        sys.stdout = TextRedirector(self.log_area, "stdout")

        # Giriş alanı ve buton için alt Frame
        bottom_frame = Frame(main_frame)
        bottom_frame.pack(fill=tk.X)

        self.prompt_entry = Entry(bottom_frame, font=("Arial", 12))
        self.prompt_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, ipady=5, padx=(0, 10))
        # Enter tuşuna basıldığında da gönderme işlemi yapsın
        self.prompt_entry.bind("<Return>", self.send_prompt_thread)

        self.send_button = Button(bottom_frame, text="Gönder", command=self.send_prompt_thread, font=("Arial", 10, "bold"), padx=10)
        self.send_button.pack(side=tk.RIGHT)
        
        print("----------- AI Destekli Unity İstemcisi (PRIME) -----------")
        print("Komutunuzu girin ve 'Gönder' butonuna basın.")


    def send_prompt_thread(self, event=None):
        """ Butona basıldığında prompt'u ayrı bir thread'de işler, arayüzün donmasını engeller. """
        prompt = self.prompt_entry.get()
        if prompt:
            # İşlem sırasında butonu ve giriş alanını devre dışı bırak
            self.send_button.config(state='disabled')
            self.prompt_entry.config(state='disabled')

            # Prompt'u işlemesi için yeni bir thread başlat
            thread = threading.Thread(target=self.process_in_background, args=(prompt,))
            thread.start()
    
    def process_in_background(self, prompt):
        """ Arka planda çalışan asıl işlem fonksiyonu. """
        try:
            process_and_execute_prompt(prompt)
        finally:
            # İşlem bittiğinde, ana thread üzerinden GUI elemanlarını tekrar aktif et
            self.root.after(0, self.enable_ui)

    def enable_ui(self):
        """ GUI elemanlarını tekrar kullanılabilir hale getirir. """
        self.prompt_entry.delete(0, tk.END) # Giriş alanını temizle
        self.send_button.config(state='normal')
        self.prompt_entry.config(state='normal')
        self.prompt_entry.focus() # İmleci tekrar giriş alanına odakla


# Bu sınıf, print() fonksiyonundan gelen yazıların Tkinter Text widget'ına yazılmasını sağlar
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.config(state='normal')
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END) # Otomatik olarak en alta kaydır
        self.widget.config(state='disabled')
        
    def flush(self):
        pass