# 📚 SayTheWord

**SayTheWord** is an educational web app designed to help young learners improve their reading and pronunciation skills. It uses text-to-speech (TTS) technology to pronounce words or sentences aloud when clicked—whether they are typed text or part of an image (like a textbook photo).

---

## 🚀 Features

### ✅ Version 1 (V1):
- Upload or type any sentence.
- Click on any word to hear it pronounced using browser-based text-to-speech.
- Ideal for kids learning to read and pronounce English words correctly.

### 🖼️ Version 2 (V2 - Current):
- Upload a picture from local storage (e.g., a page of a book).
- The app uses OCR (Optical Character Recognition) to detect words directly **on the image**.
- Users can click **on the image itself** to hear the spoken word at the clicked location.

---

## 🛠️ Tech Stack

- Python
- Flask (backend)
- HTML, CSS, JavaScript (frontend)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via `pytesseract`
- Pillow (image processing)
- Web Speech API (for browser TTS)

---

## 📂 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/saytheword.git
cd saytheword
