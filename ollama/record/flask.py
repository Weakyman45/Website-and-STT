import os
import queue
import vosk
import sys
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 设置 Vosk 模型路径
MODEL_PATH = "model"

# 加载 Vosk 模型
if not os.path.exists(MODEL_PATH):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    sys.exit()

model = vosk.Model(MODEL_PATH)

# 设置音频流参数
samplerate = 16000  # 固定采样率，因为我们会处理上传的音频文件

# Flask API 路由
@app.route('/recognize', methods=['POST'])
def recognize():
    audio_data = request.files['audio'].read()

    # 创建识别器
    rec = vosk.KaldiRecognizer(model, samplerate)

    # 处理音频数据
    rec.AcceptWaveform(audio_data)
    result = rec.Result()
    text = json.loads(result)["text"]

    return jsonify({
        "recognized_text": text
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)