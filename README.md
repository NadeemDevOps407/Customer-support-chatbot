# 🛍️ Customer Support Chatbot  

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python)  
![Flask](https://img.shields.io/badge/Made%20with-Flask-black?logo=flask)  
![OpenAI](https://img.shields.io/badge/Powered%20by-ChatGPT-green?logo=openai)  
![Speech](https://img.shields.io/badge/Supports-Voice%20%26%20Text-orange?logo=google-voice)  
![License](https://img.shields.io/badge/License-MIT-yellow.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  

An **AI-powered customer support chatbot** for shopping stores, designed to **talk with customers via text and voice**.  
It brings **human-like intelligence** to online shopping experiences using **ChatGPT** and **Flask**.  

---

## ✨ Features  

- 💬 **Text Chat** – Interactive and real-time conversations.  
- 🎙️ **Voice Support** – Speak with the bot and hear replies.  
- 🤖 **Powered by ChatGPT** – Intelligent, human-like support.  
- ⚡ **Flask Backend** – Lightweight and scalable backend.  
- 🎨 **Modern UI** – Smooth, user-friendly chat interface.  

---

## 🎥 Demo  

| Text Conversation | Voice Conversation |
|-------------------|---------------------|
| ![Demo Text Chat](screenshots/demo-text.gif) | ![Demo Voice Chat](screenshots/demo-voice.gif) |

---

## 🏗️ Project Architecture  
flowchart TD
    A[🎤 User Voice Input] --> B[🌐 Web Frontend]
    B --> C[🎯 Flask Backend\n/voice endpoint]
    C --> D[🔊 Whisper API\nSpeech to Text]
    D --> E[💬 GPT-4o-mini\nAI Response]
    E --> F[📢 TTS API\nText to Speech]
    F --> C
    C --> G[🔊 Audio Response]
    G --> B
    B --> H[🎧 Play Audio to User]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#ffebee
    style F fill:#e0f2f1
    style G fill:#fce4ec
    style H fill:#e8eaf6