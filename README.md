# ✨ Minimalist-Content-Creator

## ⚡ Overview

**Minimalist-Content-Creator** is a technical showcase demonstrating how to achieve **precise stylistic control** over Large Language Models (LLMs) using **System Instructions** within the **Gemini API**.

This tool enforces a strict narrative persona — such as a *1950s pulp sci-fi narrator* — and transforms any user input into that selected tone. The goal: prove that LLMs can operate as **directive content engines**, not just conversational agents.

---

## ✨ Key Features

- **Persona-Locked Output**  
  System Instruction ensures the LLM always speaks in the defined style.

- **Predictable Generation**  
  Content is produced consistently, without drift from the persona rules.

- **Stylised Content Creation**  
  Converts ordinary user text into themed narrative styles (retro sci-fi, noir, historical, etc.).

- **Lightweight UI**  
  Minimal interface using **Gradio or Streamlit** for fast testing and demos.

- **True Gemini System-Instruction Integration**  
  Proper `generateContent` payload structure highlighting System Instruction priority.

---

## 🧠 Architecture & Flow

1. User enters text
2. Project prepends a multi-line persona and behaviour rule set as **System Instruction**
3. Sends request to **gemini-2.5-flash-preview-09-2025**
4. Response is always persona-consistent

This ensures the persona remains locked and output stays aligned with the desired voice.

---

## 🚀 Installation & Setup

### ✅ Prerequisites

- Python **3.8+**
- **Gemini API Key** (Google AI Studio)

---

### 📦 Clone Repository

```bash
git clone https://github.com/your-username/minimalist-content-creator.git
cd minimalist-content-creator
```

---

### 🧩 Install Dependencies

```bash
pip install google-genai gradio
```

> *(Use Streamlit instead if desired)*

---

### 🔑 Add API Key

Create `.env`:

```bash
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

(or export via environment variable)

---

## ▶️ Run the App

```bash
python orchestrator_app.py
```

Then visit the local app URL (e.g. `http://127.0.0.1:7860`).

---

## 🎭 Example Test Prompt

> Explain what a toaster does.

Example output tone you might expect:

> *In the gleaming kitchens of tomorrow-yesterday, brave coils of fire singe humble bread into golden sustenance for star-faring dreamers…*

---

## 📂 Purpose

This project serves as a **reference implementation** of:

- system-anchored LLM behaviour control  
- persona-based content pipelines  
- deterministic, stylised generation workflows  

---

## 📜 License

MIT License — build, tweak, and explore freely 🤝
