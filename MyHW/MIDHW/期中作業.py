from PyQt5 import QtWidgets
import sys
import threading
import requests
import pyttsx3
import openai
import speech_recognition as sr
from flask import Flask, request, jsonify
from flask_cors import CORS

# =Flask 初始化=
app = Flask(__name__)
CORS(app)

# =openai API 金鑰=
openai.api_key = 'API KEY'

# =Flask API 路由=
@app.route('/magic_mirror', methods=['POST'])
def magic_mirror():
    try:
        data = request.get_json()
        user_input = data.get('question')
        if not user_input:
            return jsonify({'error': '未提供問題'}), 400

        # OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150
        )
        answer = response['choices'][0]['message']['content'].strip()
        threading.Thread(target=speak_text, args=(answer,), daemon=True).start()
        return jsonify({'answer': answer})

    except Exception as e:
        print(f"Flask 錯誤: {e}")
        return jsonify({'error': str(e)}), 500

# =語音=
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"語音合成錯誤: {e}")

# =前端呼叫 Flask API=
def chat_with_api(question):
    try:
        res = requests.post("http://127.0.0.1:5000/magic_mirror", json={"question": question})
        return res.json().get('answer', 'API 錯誤，請檢查伺服器')
    except Exception as e:
        return f"請求失敗: {e}"

# =PyQt5 GUI=
class MagicMirrorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("羅伯特")
        self.resize(800, 400)

        self.label = QtWidgets.QLabel("歡迎使用 金門大學資工系 聊天機器人", self)
        self.label.setGeometry(70, 20, 700, 50)
        self.label.setStyleSheet('font-size: 30px; font-family: "微軟正黑體";')

        self.chat_display = QtWidgets.QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setGeometry(50, 80, 700, 180)

        self.user_input = QtWidgets.QLineEdit(self)
        self.user_input.setPlaceholderText("請輸入您的問題...")
        self.user_input.setGeometry(50, 280, 500, 40)

        self.send_button = QtWidgets.QPushButton("送出", self)
        self.send_button.setGeometry(570, 280, 80, 40)
        self.send_button.clicked.connect(self.handle_user_input)

        self.voice_button = QtWidgets.QPushButton("語音輸入", self)
        self.voice_button.setGeometry(670, 280, 80, 40)
        self.voice_button.clicked.connect(self.handle_voice_input)

    def handle_user_input(self):
        question = self.user_input.text().strip()
        if question:
            self.chat_display.append(f"<b>您:</b> {question}")
            self.user_input.clear()
            answer = chat_with_api(question)
            self.chat_display.append(f"<b>機器人:</b> {answer}")

    def handle_voice_input(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.chat_display.append("<b>系統:</b> 請說話...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            question = recognizer.recognize_google(audio, language="zh-TW")
            self.chat_display.append(f"<b>您:</b> {question}")
            answer = chat_with_api(question)
            self.chat_display.append(f"<b>機器人:</b> {answer}")
        except Exception as e:
            self.chat_display.append(f"<b>錯誤:</b> {e}")

# =Flask + GUI=
def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

def start_gui():
    qt_app = QtWidgets.QApplication(sys.argv)
    form = MagicMirrorApp()
    form.show()
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    # Flask Server
    threading.Thread(target=run_flask, daemon=True).start()

    # GUI
    start_gui()
