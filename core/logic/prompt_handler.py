# core/logic/prompt_handler.py
import json
from core.comms.llm_manager import get_llama_response
from core.comms.unity_client import send_to_unity

# Bu, yapay zekamızı eğiteceğimiz "Anayasa Promptu"
SYSTEM_INSTRUCTION = """
You are an expert AI that converts user prompts into a sequence of JSON-RPC commands for the Unity Engine.

RULES:
1. Your response MUST be ONLY a valid JSON object or a JSON array of objects. Do not include any extra text.
2. Each JSON object MUST use `{"jsonrpc": "2.0", "type": "...", "params": {...}}`. Use the 'type' keyword, not 'method'.
3. For multi-step commands, you MUST return a JSON array: `[ { ... }, { ... } ]`.
4. Use `\n` for newlines in C# code within the 'content' field.

AVAILABLE COMMANDS:
- "type": "manage_gameobject"
  - "params":
    - "action": "create"
    - "primitiveType": "Cube", "Sphere", "Capsule", "Cylinder", "Plane", "Quad".
    - "name": (string) The name of the new object.
    - "position": (list of 3 floats) [x, y, z].
    - "scale": (list of 3 floats) [x, y, z].
    - "color": (object) {"r":0.0-1.0, "g":0.0-1.0, "b":0.0-1.0, "a":1.0}.
"""

def process_and_execute_prompt(user_prompt):
    """
    Ana işlem fonksiyonu: prompt'u alır, LLM'e gönderir ve sonucu Unity'ye iletir.
    """
    print(f"\n[İŞLENİYOR] Kullanıcı prompt'u: '{user_prompt}'")
    print("[İSTEK] Llama modelinden cevap bekleniyor...")
    
    json_text = get_llama_response(user_prompt, SYSTEM_INSTRUCTION)
    
    if not json_text:
        print("[HATA] LLM'den bir cevap alınamadı. İşlem durduruldu.")
        return

    print(f"[LLAMA'DAN YANIT]\n{json_text}")

    try:
        parsed_json = json.loads(json_text)
        if isinstance(parsed_json, list):
            print(f"\n[BİLGİ] {len(parsed_json)} adımlı bir komut dizisi algılandı...")
            for i, command in enumerate(parsed_json, 1):
                print(f"--- Adım {i} gönderiliyor... ---")
                command_str = json.dumps(command)
                send_to_unity(command_str)
        else:
            send_to_unity(json_text)
            
    except json.JSONDecodeError:
        print("[HATA] Llama'dan gelen yanıt geçerli bir JSON değil.")