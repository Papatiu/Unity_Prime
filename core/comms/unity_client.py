# core/comms/unity_client.py
import socket
# Düzeltilmiş import satırı
from utils.config_manager import UNITY_SERVER_IP, UNITY_SERVER_PORT

def send_to_unity(command_json_str):
    try:
        # Düzeltilmiş değişken isimleri
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((UNITY_SERVER_IP, UNITY_SERVER_PORT))
        client_socket.sendall(command_json_str.encode('utf-8'))
        print(f"\n[İLETİLİYOR] -> Unity'ye: {command_json_str}")
        response = client_socket.recv(8192)
        print(f"[UNITY'DEN CEVAP] <- {response.decode('utf-8')}")
    except Exception as e:
        print(f"[HATA] Unity ile iletişim kurulamadı: {e}")
    finally:
        if 'client_socket' in locals() and client_socket.fileno() != -1:
            client_socket.close()