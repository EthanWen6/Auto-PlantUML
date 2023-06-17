# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_file,render_template
import plantuml
import openai
import base64

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-diagram', methods=['POST'])
def generate_diagram():
    plantuml_code = request.json['code']

    # 将 PlantUML 代码转换为图片
    puml = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
    image_bytes = puml.processes(plantuml_code)

    # 将图片字节流转换为Base64编码字符串
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    return jsonify({'image_base64': image_base64})

openai.api_key = "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"

@app.route('/process-user-input', methods=['POST'])
def process_user_input():
    user_content = request.json['content']

    # 构造对话历史，替换示例助手的部分
    messages = [
        {"role": "system", "content": "你是一个PlantUML输出工具，需要根据用户描述的场景输出PlantUML代码"},
        {"role": "system", "content": "你的输出必须且只能包含代码块，不需要额外的描述"},
        {"role": "system", "name":"example_user", "content": user_content}
    ]

    # 调用OpenAI的ChatGPT模型生成回复
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    reply_content = response["choices"][0]["message"]["content"]

    start_delimiter = '@startuml'
    end_delimiter = '@enduml'

    start_index = reply_content.index(start_delimiter)
    end_index = reply_content.index(end_delimiter) + len(end_delimiter)

    code_block = reply_content[start_index:end_index]
    code_block = "!theme minty\n" + code_block

    print(code_block)
    return jsonify({'reply': code_block})


if __name__ == '__main__':
    app.run()
