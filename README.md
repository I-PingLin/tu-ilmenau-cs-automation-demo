# TU Ilmenau CS & Automation — Portfolio Demo

A self-contained Streamlit app showcasing modules aligned with TU Ilmenau's Computer Science and Automation programme:
- AI/ML: Iris classification (Logistic Regression / Random Forest)
- Computer Vision: Preprocessing and Canny edge detection
- Robotics: A* path planning in a grid world
- Cybersecurity: Password hashing (bcrypt), JWT, and symmetric encryption (Fernet)

## Quick start (Windows)
1. Open PowerShell in the project folder.
2. Run:
   
   ```powershell
   .\run_app.ps1
   ```

This will create a virtual environment, install dependencies, and launch the app in your browser.

## Structure
- `streamlit_app.py` — Unified UI
- `modules/ml.py` — ML model training + inference on Iris
- `modules/cv.py` — Image preprocessing and edge detection
- `modules/robotics.py` — Grid generation and A* path planning
- `modules/security.py` — Hashing, JWT, and Fernet crypto

## Notes
- No external services required.
- Packages are pinned for reproducibility.

---

## 日本語: 概要と使い方
TU Ilmenau の「Computer Science and Automation」に対応する統合デモです（Streamlit製）。以下のモジュールをまとめて体験できます。
- AI/ML（Iris分類）
- コンピュータビジョン（前処理・Cannyエッジ）
- ロボティクス（グリッド/A*経路計画）
- セキュリティ（bcrypt/JWT/Fernet）

### 実行方法（Windows）
PowerShell でプロジェクト直下を開き、次を実行してください。

```powershell
.\run_app.ps1
```

ブラウザでアプリが起動します。
