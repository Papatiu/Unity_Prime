# core/comms/llm_manager.py
import requests
import json
from utils.config_manager import GITHUB_TOKEN  # Ayarları merkezi yerden alıyoruz

# Şimdilik sadece GitHub Llama modelini tanımlıyoruz
API_URL = "https://models.github.ai/inference/chat/completions"
MODEL_NAME = "meta/Meta-Llama-3.1-405B-Instruct"

def get_llama_response(prompt, system_instruction):
    """GitHub Llama modelinden bir cevap alır."""
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 4096,
        "top_p": 0.1
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            # Gelen yanıttan ```json ... ``` gibi işaretleri temizleyerek saf metni döndür
            content = response_json['choices'][0]['message']['content']
            return content.strip().replace("```json", "").replace("```", "").strip()
        else:
            error_text = response.text
            print(f"\n[HATA] GitHub API'den hata kodu {response.status_code} alındı: {error_text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n[HATA] LLM sunucusuna bağlanırken bir ağ hatası oluştu: {e}")
        return None