# servers/tcp_server.py
import socket
import threading

HOST_IP = "127.0.0.1"
HOST_PORT = 8080
UNITY_IP = "127.0.0.1"
UNITY_PORT = 6400

def handle_client(client_socket):
    print(f"[TCP Sunucu] Yeni istemci bağlandı: {client_socket.getpeername()}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as unity_socket:
            unity_socket.connect((UNITY_IP, UNITY_PORT))
            print(f"[TCP Sunucu] Unity Editor'a başarıyla bağlanıldı.")
            
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                print(f"[TCP Sunucu] {len(data)} byte veri alındı, Unity'ye yönlendiriliyor...")
                unity_socket.sendall(data)
                
                response_from_unity = unity_socket.recv(8192)
                if response_from_unity:
                    print(f"[TCP Sunucu] {len(response_from_unity)} byte cevap alındı, istemciye geri gönderiliyor...")
                    client_socket.sendall(response_from_unity)

    except Exception as e:
        print(f"[HATA] TCP sunucusunda bir hata oluştu: {e}")
    finally:
        print(f"[TCP Sunucu] Bağlantı kapatılıyor.")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_IP, HOST_PORT))
    server.listen(5)
    print(f"[*] Postacı sunucu dinlemede: {HOST_IP}:{HOST_PORT}")
    while True:
        client_sock, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()