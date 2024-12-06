from flask import Flask, request, jsonify, send_from_directory, abort
import json
import os
import datetime
import logging
import pytz

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
CONFIG_FILE = 'server_config.json'

# 配置日志级别
app.config['LOG_LEVEL'] = logging.WARNING
app.logger.setLevel(app.config['LOG_LEVEL'])  # 应用配置到日志器

config = {}
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=2)

try:
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    print("未找到配置文件，已创建默认配置文件。")
    config = {
        'upload_dir': 'uploads',
        'version': None,
        'port': 5000
    }
    save_config(config)

os.makedirs(config['upload_dir'], exist_ok=True)

@app.route('/')
def html_page():
    return send_from_directory('.', 'dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "No files part", 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        # 获取文件的路径，例如：folder1/folder2/filename.txt
        file_path = file.filename
        # 创建多级目录
        directory = os.path.join(app.config['UPLOAD_FOLDER'], os.path.dirname(file_path))
        os.makedirs(directory, exist_ok=True)  # 创建目录（如果不存在）

        # 保存文件
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_path)
        file.save(filepath)
        return 'success'
    except Exception as e:
        return 'failed: '+ str(e)

@app.route('/file/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # 检查文件是否存在
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)  # 如果文件不存在，返回404错误

@app.route('/update_version', methods=['GET'])
def update_version_api():
    tz = pytz.timezone('Asia/Shanghai') 
    config['version'] = datetime.datetime.now(tz).strftime("%Y%m%d%H%M%S")
    save_config(config)
    return jsonify({
        "version": config['version']
    })

clients = {}

@app.route('/version', methods=['GET'])
def get_version():
    tz = pytz.timezone('Asia/Shanghai') 
    clients[request.remote_addr] = str(datetime.datetime.now(tz))
    return jsonify({
        "version": config['version']
    })

@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config['port'], debug=False)