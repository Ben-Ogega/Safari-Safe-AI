# Safari-Safe-AI 🇰🇪 🚗
**Optimizing Vision Transformers (ViT) for Real-Time Pedestrian Safety on Edge Hardware.**

## 📌 Project Overview
Safari-Safe-AI is a research-driven project developed for the **November 2026 Engineering Conference**. The goal is to implement a high-accuracy, Transformer-based safety system that can detect and predict pedestrian movement at zebra crossings, specifically optimized for standard CPU environments and regional road infrastructure challenges (e.g., heavy rain, high-density pedestrian traffic).

### 🎯 Conference Goals
- **Real-Time Inference:** Achieve <100ms latency on standard CPU hardware using MobileViT.
- **Robustness:** Maintain high confidence scores during simulated environmental noise (light to heavy rain).
- **Edge Deployment:** Demonstrate a viable "Inference-at-the-Edge" pipeline for Kenyan automotive safety applications.

---

## 🛠️ Tech Stack & Architecture
- **Model:** `MobileViT` (Mobile-friendly Vision Transformer)
- **Framework:** `PyTorch` / `Hugging Face Transformers`
- **Optimization:** `Quantization` (INT8) via ONNX Runtime / OpenVINO
- **Environment:** VS Code, Jupyter, Git

### Why Transformers?
Unlike traditional CNNs, the **Self-Attention** mechanism in Safari-Safe-AI allows the model to understand the global context of a scene—relating the car's velocity vector directly to the pedestrian's distance from the zebra crossing markings.

---

## 📅 Development Roadmap (7-Month Milestone)
- [x] **Month 1:** Environment Setup & Repository Initialization (April 2026)
- [ ] **Month 2-3:** Synthetic Data Generation & Simulation (CARLA)
- [ ] **Month 4:** Cross-Attention Mechanism implementation
- [ ] **Month 5:** CPU Optimization & Model Quantization
- [ ] **Month 6:** Performance Benchmarking & Paper Drafting
- [ ] **Month 7:** Conference Presentation (November 2026)

---

## 🚀 Getting Started
1. Clone the repo:
   ```bash
   git clone [https://github.com/Ben-Ogega/Safari-Safe-AI.git](https://github.com/Ben-Ogega/Safari-Safe-AI.git)

2. Install dependencies:
  ```bash
    pip install -r requirements.txt
  ```  

🤝 Contribution & Contact
This project is part of a 7-month mastery journey into Transformer Architectures.
Developer: Ben Ogega

Location: Kisumu, Kenya