# AI Grammar & Spell Checker (GrammarCraft)

[![Python 3.13](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![LanguageTool](https://img.shields.io/badge/NLP-LanguageTool-green.svg)](https://languagetool.org/)
[![Repository](https://img.shields.io/badge/GitHub-AI__grammar__checker-181717.svg?logo=github)](https://github.com/sumitchaudhari-rgb/AI_grammar_checker)

An intelligent, modern Natural Language Processing (NLP) web application that identifies grammatical flaws, catches spelling errors, and suggests accurate contextual corrections in real time.

🔗 **Repository Link**: [https://github.com/sumitchaudhari-rgb/AI_grammar_checker](https://github.com/sumitchaudhari-rgb/AI_grammar_checker)

---

## ✨ Key Features

- **🔴 Red-Line Error Underlining**: Mistaken or misspelled words in your input text are highlighted with a distinct red underline as soon as you analyze the text. Hovering shows the suggested correction.
- **🟢 Green-Line Correction Underlining**: Corrected replacement words in the **Smart Analysis** field are highlighted with a vibrant green underline. Hovering reveals the original word.
- **⚡ Snappy Asynchronous Engine**: Real-time checking via `/api/check` endpoint without page reloads or layout shift.
- **📊 Real-Time Metrics & Statistics**:
  - Live Word Count & Character Count
  - Estimated Reading Time
  - Accuracy Score (%) calculation
  - Breakdown of Spelling vs. Grammar & Style issues
- **🎨 Modern Glassmorphism UI**: High-contrast, clean dark theme with responsive typography, smooth glowing gradients, and native micro-animations.
- **🛠️ Productivity Utilities**:
  - **1-Click Sample Text**: Preloads test sentences with intentional errors for quick verification.
  - **Copy to Clipboard**: Quick copy of the clean, corrected text with animated toast feedback.
  - **Text-to-Speech (TTS)**: Built-in reader that speaks the corrected text aloud via the Web Speech API.
  - **"Use as Input"**: Feeds the corrected text back into the editor with one click.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13+, Flask
- **NLP Engine**: `language-tool-python` (powered by LanguageTool standalone server)
- **Runtime Requirement**: Java (OpenJDK 8+ or 17+) for LanguageTool
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism, CSS Custom Properties), JavaScript (Fetch API, Web Speech API)
- **Typography**: Google Fonts (*Plus Jakarta Sans* & *JetBrains Mono*)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.10+** (Python 3.13 recommended)
- **Java JRE / OpenJDK 8+** (Required by LanguageTool)
- **Git**

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sumitchaudhari-rgb/AI_grammar_checker.git
   cd AI_grammar_checker
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     py -3.13 -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in your browser**:
   Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📂 Project Structure

```text
AI_grammar_checker/
├── app.py                # Flask application routes, NLP logic, diff annotations & API
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignored files (venv, pycache, etc.)
├── templates/
│   └── index.html        # Modern glassmorphism web interface with real-time scripts
└── README.md             # Project documentation
```

---

## 📡 API Reference

### `POST /api/check`
Performs asynchronous grammar and spell analysis.

- **Request Body**:
  ```json
  {
    "text": "This are a bad speling mistake."
  }
  ```

- **Response Body**:
  ```json
  {
    "success": true,
    "text": "This are a bad speling mistake.",
    "corrected_text": "These are a bad spelling mistake.",
    "annotated_input_html": "<span class=\"red-line\" title=\"Suggested correction: These\">This</span> <span class=\"red-line\" title=\"Suggested correction: is\">are</span> a <span class=\"red-line\" title=\"Suggested correction: spelling\">speling</span> mistake.",
    "annotated_corrected_html": "<span class=\"green-line\" title=\"Corrected from: This\">These</span> <span class=\"green-line\" title=\"Corrected from: are\">is</span> a <span class=\"green-line\" title=\"Corrected from: speling\">spelling</span> mistake.",
    "matches": [ ... ],
    "stats": {
      "words": 6,
      "chars": 31,
      "sentences": 1,
      "reading_time_sec": 2,
      "issues_total": 2,
      "issues_spelling": 1,
      "issues_grammar": 1,
      "issues_style": 0,
      "accuracy_score": 67
    }
  }
  ```

---

## 📄 License & Attribution

This project is open source and available under the [MIT License](LICENSE).
Engine powered by [LanguageTool](https://languagetool.org/).
