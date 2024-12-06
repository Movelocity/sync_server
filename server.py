from flask import Flask, request, jsonify, send_from_directory, abort, redirect
import json
import os
import datetime
import logging
import pytz
from dataclasses import dataclass, asdict
from typing import Dict, Optional

@dataclass
class Client:
    last_seen: str
    note: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'Client':
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads'
CONFIG_FILE = 'server_config.json'
CLIENTS_FILE = 'clients_data.json'

# 配置日志级别
app.config['LOG_LEVEL'] = logging.WARNING
app.logger.setLevel(app.config['LOG_LEVEL'])  # 应用配置到日志器

config = {}
clients: Dict[str, Client] = {}
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=2)

def save_clients():
    with open(CLIENTS_FILE, 'w') as file:
        json.dump({ip: client.to_dict() for ip, client in clients.items()}, file, indent=2)

def load_clients():
    global clients
    try:
        with open(CLIENTS_FILE, 'r') as file:
            data = json.load(file)
            clients = {ip: Client.from_dict(client_data) for ip, client_data in data.items()}
    except FileNotFoundError:
        clients = {}
        save_clients()

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

load_clients()

@app.route('/')
def html_page():
    return redirect('/static/index.html')

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

@app.route('/version', methods=['GET'])
def get_version():
    tz = pytz.timezone('Asia/Shanghai')
    client_ip = request.remote_addr
    current_time = str(datetime.datetime.now(tz))
    
    if client_ip not in clients:
        clients[client_ip] = Client(last_seen=current_time)
    else:
        clients[client_ip].last_seen = current_time
    save_clients()
    return jsonify({
        "version": config['version']
    })

@app.route('/clients', methods=['GET'])
def get_clients():
    return jsonify({ip: client.to_dict() for ip, client in clients.items()})

@app.route('/client/<client_ip>', methods=['DELETE'])
def delete_client(client_ip):
    if client_ip in clients:
        del clients[client_ip]
        save_clients()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Client not found"}), 404

@app.route('/client/<client_ip>/note', methods=['PUT'])
def update_client_note(client_ip):
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    if 'note' not in data:
        return jsonify({"status": "error", "message": "Missing note field"}), 400
    
    if client_ip not in clients:
        return jsonify({"status": "error", "message": "Client not found"}), 404
    
    clients[client_ip].note = data['note']
    save_clients()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config['port'], debug=True)