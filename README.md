# 多语言内容助手 (Multilingual Assistant)

基于DeepSeek API的多语言内容助手，支持文本翻译、内容生成和多语言处理。

## 功能特点

- 💬 多语言文本翻译
- 📝 智能内容生成
- 🌐 支持多种语言
- 🚀 基于先进的DeepSeek API

## 安装方法

### 前置条件

- Python 3.8+
- pip

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/Oceanzen9/multilingual-assistant.git
cd multilingual-assistant
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建`.env`文件并添加以下内容：
```
DEEPSEEK_API_KEY=your_api_key_here
FLASK_DEBUG=true
SECRET_KEY=your_secret_key_here
```

## 使用方法

启动服务器：
```bash
python main.py
```

访问API：
- 本地访问：http://localhost:5000/api

## API文档

详细的API文档请参阅[docs/api.md](docs/api.md)。

## 开发指南

请参阅[docs/README.md](docs/README.md)获取开发指南。

## 许可证

本项目使用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！请先阅读贡献指南。

## 联系方式

作者：Haiyang Zeng
邮箱：oceanzen9@gmail.com