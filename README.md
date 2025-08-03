# NEXA-Next-Gen-AI-Experience-Assistant
NEXA – A real-time voice-enabled AI assistant that uses speech recognition, NLP, a trained TensorFlow model, and a series of intelligent command handlers to manage tasks such as opening apps, browsing the web, solving math problems, and more, all through natural speech.

### Features:
- Voice-controlled interface via Google Speech Recognition
- Custom-trained neural network (intent classification with NLP)
- Real-time app control: Calculator, Notepad, VSCode, Zoom, etc.
- Social media access: Facebook, WhatsApp, LinkedIn, etc.
- System monitoring: CPU usage, battery condition
- Personalized scheduling (day-wise timetable)
- Math solver: Interprets and calculates spoken math expressions
- Dynamic small talk & Q/A responses using trained intents

### Tech Stack:
| Area                 | Tool/Library                    |
| -------------------- | ------------------------------- |
| Programming Language | Python                          |
| NLP & ML Framework   | TensorFlow, Keras, Scikit-learn |
| Speech Recognition   | `speech_recognition`, `pyttsx3` |
| GUI Automation       | `pyautogui`                     |
| System Info & Tasks  | `psutil`, `os`, `webbrowser`    |
| Persistence          | `pickle`, JSON                  |

### Sample Voice Commands:
- “Open calculator”
- “What’s the schedule for Friday?”
- “Search ChatGPT on Google”
- “Multiply 25 by 4”
- “Check the system condition”
- “Open LinkedIn”
- “Close Zoom”

### How It Works:
1. Speech Input → Captured using Google Speech Recognition via speech_recognition.
2. Text Preprocessing → Tokenized, padded using the saved tokenizer.
3. Model Prediction → A trained Keras NLP model classifies the intent.
4. Response Generator:
   - Executes system commands or opens URLs.
   - Responds from intents.json for predefined interactions.
5. Voice Output → Responds with natural speech using pyttsx3.
