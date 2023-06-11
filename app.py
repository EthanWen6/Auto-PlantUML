from flask import Flask, request, jsonify, send_file,render_template
import plantuml
import openai

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

    # 保存图片到服务器的临时目录中
    image_path = 'static/diagram.png'
    with open(image_path, 'wb') as image_file:
        image_file.write(image_bytes)

    return send_file(image_path, mimetype='image/png')

openai.api_key = "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"

@app.route('/process-user-input', methods=['POST'])
def process_user_input():
    user_content = request.json['content']

    # 构造对话历史，替换示例助手的部分
    messages = [
        {"role": "system", "content": "你是一个公司的产品经理"},
        {"role": "system", "name": "example_user", "content": "你需要了解PlantUML这种语言，这是用来绘制UML图型的语言"},
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

    print(code_block)
    return jsonify({'reply': code_block})


if __name__ == '__main__':
    app.run()
