# main.py
import tkinter as tk
from gui.main_window import PrimeApp
from servers.tcp_server import start_server # Postacı sunucumuzu import ediyoruz
import threading

def run_tcp_server():
    """ Postacı TCP sunucusunu ayrı bir thread'de başlatır. """
    print("[BİLGİ] Postacı TCP sunucusu başlatılıyor...")
    start_server()

if __name__ == "__main__":
    # Önce postacı sunucumuzu arka planda başlatalım
    # 'daemon=True' sayesinde ana program (arayüz) kapanınca bu thread de otomatik kapanır
    server_thread = threading.Thread(target=run_tcp_server)
    server_thread.daemon = True
    server_thread.start()

    # Şimdi Tkinter arayüzünü başlatalım
    # Bu, ana thread'de çalışacak ve programın açık kalmasını sağlayacak
    root = tk.Tk()
    app = PrimeApp(root)
    root.mainloop()