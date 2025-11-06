# ✨ Minimalist-Content-Creator

## ⚡ Overview
**Minimalist-Content-Creator** is a technical showcase demonstrating precise stylistic control over Large Language Models (LLMs) using **System Instructions** in the Gemini API. It converts any input into a fixed persona — e.g., a 1950s pulp sci‑fi narrator — proving LLMs can be deterministic content engines, not only chats.

---

## ✨ Key Features
- Persona‑Locked Output  
- Predictable controlled generation  
- Retro / Noir / Historical persona modes  
- Minimal UI (Gradio/Streamlit)  
- Direct Gemini payload control  

---

## 🧠 Architecture & Flow
1. User input  
2. System Instruction applied  
3. Request to `gemini-2.5-flash-preview-09-2025`  
4. Persona‑consistent output  

---

## 🚀 Setup
```bash
git clone https://github.com/your-username/minimalist-content-creator.git
cd minimalist-content-creator
pip install google-genai gradio
```

`.env`:
```bash
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Run:
```bash
python orchestrator_app.py
```

---

## 🎭 Demo Prompt
**Input:** Explain a toaster.  
**Output:**  
*In the chromium‑gleam kitchens of tomorrow‑yesteryear, crackling coils forge bread into rocket‑fuel for cosmic dreamers…*

---

## 🛠️ Technical Deep Dive: `Minimalist-Content-Creator.py`

### Architectural Overview
| Component | Purpose | Concept |
|---|---|---|
| `main()` | CLI + input loop | Interface |
| `os.getenv()` | Load credentials | Security |
| `generate_content()` | Build request + call API | Wrapper |
| Retry loop | Auto retry | Exponential Backoff |

---

### Key Configuration
| Constant | Value | Purpose |
|---|---|---|
| `MODEL_NAME` | `gemini-2.5-flash-preview-09-2025` | Fast persona LLM |
| `SYSTEM_PROMPT` | Persona rules | Enforce style |

---

### Authentication
```python
api_key = os.getenv("GEMINI_API_KEY")
```
✔ avoids leaking secrets

---

### Payload
```python
payload = {
    "contents": [{"parts": [{"text": user_query}]}],
    "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
    "tools": [{"google_search": {} }],
}
```

- `systemInstruction` = persona lock  
- `google_search` = real info grounding  

---

### Exponential Backoff
```python
MAX_RETRIES = 5
delay = BASE_DELAY * (2 ** attempt)
```

✔ avoids overloading API  
✔ handles 429/500/503  

---

### Response Parsing
```python
text = data.get("candidates",[{}])[0]\
       .get("content",{}).get("parts",[{}])[0]\
       .get("text")
```

Extracts useful output only.

---

### CLI Flow
- prints persona info  
- loops for user prompts  
- `Ctrl+C` exits safely  

---

## 📜 License
MIT License
