# 版本控制服务器

这是一个基于Flask的简单版本控制服务器，用于管理和追踪客户端版本信息，支持文件上传下载功能。

## 功能特点

- 版本管理：追踪和更新版本号
- 客户端管理：记录客户端访问信息和备注
- 文件管理：支持文件的上传和下载
- Web界面：提供简单的Web管理界面

## 安装说明

1. 确保已安装Python 3.x
2. 克隆项目到本地
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

服务器配置文件为 `server_config.json`，包含以下配置项：
- `upload_dir`: 文件上传目录
- `version`: 当前版本号
- `port`: 服务器端口号

## 运行服务器

### Windows
```bash
python server.py
```

### Linux/Mac
```bash
./run_server.sh
```

服务器默认运行在 `http://localhost:5000`

## API接口

### 版本管理
- GET `/version` - 获取当前版本
- GET `/update_version` - 更新版本号

### 客户端管理
- GET `/clients` - 获取所有客户端信息
- DELETE `/client/<client_ip>` - 删除指定客户端
- PUT `/client/<client_ip>/note` - 更新客户端备注

### 文件管理
- POST `/upload` - 上传文件
- GET `/file/<filename>` - 下载文件

## 目录结构

```
├── server.py          # 主服务器程序
├── requirements.txt   # Python依赖
├── server_config.json # 服务器配置
├── clients_data.json  # 客户端数据
├── run_server.sh      # 启动脚本
├── static/            # 静态文件目录
└── uploads/           # 上传文件目录
```

## 注意事项

- 首次运行时会自动创建必要的目录和配置文件
- 确保服务器有足够的存储空间用于文件上传
- 建议在生产环境中配置适当的安全措施

## 许可证

MIT License
