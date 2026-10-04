# ExamPrep Vision AI 📸

**From Your Final Notes to Smart Revision**

ExamPrep Vision AI is an AI-powered visual revision assistant that helps students prepare for exams by turning their **final study notes** into faster and easier revision material.

## 🎯 Problem

Students often spend a lot of time preparing their final notes. After completing them, they may have very little time left for effective revision.

ExamPrep Vision AI helps students use those final notes more efficiently.

## 💡 Solution

The student uploads their own final study notes, and the AI helps them:

* Create quick visual revision material
* Identify repeated or unnecessary content
* Generate exam questions based on marks
* Ask questions about their study notes through the chat box

## ✨ Features

### 📸 Upload Final Study Notes

Upload an image of your final study notes.

### 🎯 Visual Revision

Convert the uploaded notes into a quick, easy-to-scan visual revision format.

### 📝 Smart Note Check

Identify repeated, unnecessary, overly detailed, or unclear points that could be shortened.

### 📚 Generate Exam Questions

Generate questions based on the required marks:

* **3 Marks** — Short-answer question
* **5 Marks** — Medium-answer question
* **10 Marks** — Detailed-answer question

### 💬 Study Chat

Ask questions or attach study-note images and get AI-powered help.

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API
* Google GenAI SDK
* GitHub
* Streamlit Community Cloud

## 🚀 How It Works

1. Enter your name and contact information.
2. Upload your final study notes.
3. Choose a revision feature.
4. Generate visual revision or check your notes.
5. Generate exam questions based on marks.
6. Use the chat box for study-related questions.

## 📁 Project Structure

```text
ExamPrep-Vision-AI/
├── .streamlit/
│   └── secrets.toml
├── examenv/
├── app.py
├── prompts.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔐 Security

The Gemini API key is stored using Streamlit secrets and is not included in the source code or GitHub repository.

## 🌱 Future Scope

Possible future improvements include:

* Support for multiple pages of notes
* Better visual diagrams
* More exam-question formats
* Subject-specific revision modes
* PDF note support
* Personalized revision suggestions

## 👩‍💻 Project

**ExamPrep Vision AI**
Built as an AI-powered exam preparation project using Python, Streamlit, and Google Gemini.
