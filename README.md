# Large Language Model API Detection System

## Project Background

As an investor with ten years of experience who has recently ventured into AI entrepreneurship, I discovered a critical issue while developing our AI products: the token consumption through API usage became a significant production cost. More alarmingly, I noticed that the same model would exhibit drastically different capabilities at different times. This suspicion was confirmed when a model I was conversing with directly revealed it was a Sonnet model, despite me explicitly calling the Opus model.

Driven by this discovery, I developed this project through "vibe coding" to address the problem of model downgrading. This system ensures that users receive the exact model they pay for, preventing scenarios where premium model APIs are sold but deliver lower-tier models, or where coding plans are used to significantly increase the proportion of lower-tier model outputs.

For vibe coding and the entire AI application domain, model capability is a core indicator directly linked to output quality. This project aims to eliminate any form of model downgrading, ensuring transparency and reliability in AI API usage.

Our API platform for Chinese users is api.spiritgpu.com, and we plan to launch an international version once the product stabilizes.

## Project Overview

This project aims to build a system capable of detecting API interfaces from multiple AI suppliers, accurately identifying the supplier and model type of the accessed language model. It supports models from OpenAI, Google, Anthropic, Meta, Mistral, Minimax, DeepSeek, Step, Xiaomi, and other popular providers.

## Core Features

- **Multi-Supplier Identification**: Accurately identify suppliers including OpenAI, Google, Anthropic, Meta, Mistral, Minimax, DeepSeek, Step, Xiaomi, and more
- **Model Type Identification**: Identify specific model types such as gpt-4o, gemini-1.5-pro, claude-3-opus, llama-3-70b, mistral-large, etc.
- **Confidence Calculation**: Provide confidence scores for identification results, sorted by reliability
- **Detailed Analysis**: Return detailed feature analysis reports for each detection
- **API Interface**: Provide RESTful API interface, supporting batch detection and real-time testing
- **OpenRouter Support**: Compatible with models from OpenRouter, including top 100 most used language models

## Technology Stack

- Backend: Python 3.10+
- Web Framework: Flask
- Data Processing: JSON
- Deployment: Docker (optional)

## Project Structure

```
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core detection logic
│   ├── models/         # Data models
│   └── utils/          # Utility functions
├── tests/              # Test cases
├── config.py           # Configuration file
├── requirements.txt    # Dependencies
├── app.py              # Application entry
└── README.md           # Project documentation
```

## Installation Instructions

### 1. Clone the Project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Service

```bash
python app.py
```

The service will run at `http://localhost:5000`.

## API Interfaces

### Detection Interface

**URL**: `/api/detect`
**Method**: `POST`
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "request": {
    "endpoint": "/v1/chat/completions",
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.7
  },
  "response": {
    "choices": [{
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      }
    }]
  }
}
```

**Response**:
```json
{
  "supplier": "openai",
  "model": "gpt-4o",
  "confidence": 0.7777777777777778,
  "analysis": {
    "endpoint": "/v1/chat/completions",
    "model_name": "gpt-4o",
    "request_features": ["endpoint", "model", "messages", "messages[0]", "messages[0].role", "messages[0].content", "temperature"],
    "response_features": ["choices", "choices[0]", "choices[0].message", "choices[0].message.role", "choices[0].message.content"]
  }
}
```

### Health Check Interface

**URL**: `/api/health`
**Method**: `GET`

**Response**:
```json
{
  "status": "healthy"
}
```

### Actual API Test Detection Interface

**URL**: `/api/detect/test`
**Method**: `POST`
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "api_url": "https://api.example.com/v1/chat/completions",
  "api_key": "your-api-key",
  "test_models": ["gpt-4o", "gemini-1.5-pro", "claude-3-opus-20240229"]
}
```

**Response**:
```json
{
  "best_match": {
    "supplier": "openai",
    "model": "gpt-4o",
    "confidence": 0.7777777777777778,
    "model_tested": "gpt-4o",
    "response_status": 200,
    "analysis": {
      "endpoint": "https://api.example.com/v1/chat/completions",
      "model_name": "gpt-4o",
      "request_features": [...],
      "response_features": [...]
    }
  },
  "all_results": [
    {
      "supplier": "openai",
      "model": "gpt-4o",
      "confidence": 0.7777777777777778,
      "model_tested": "gpt-4o",
      "response_status": 200,
      "analysis": {...}
    },
    {
      "model_tested": "gemini-1.5-pro",
      "error": "Model not found"
    },
    {
      "model_tested": "claude-3-opus-20240229",
      "error": "Model not found"
    }
  ]
}
```

## Identification Strategy

### OpenAI Identification Features
- Endpoint: `/v1/chat/completions`
- Request Parameters: `model`, `messages`, `temperature`, etc.
- Response Structure: `choices[].message`
- Model Naming: `gpt-3.5-turbo`, `gpt-4o`, `gpt-5`, etc.

### Google Gemini Identification Features
- Endpoint: `/generateContent` or `/v1/models/gemini-*-generateContent`
- Request Parameters: `contents`, `generationConfig`, etc.
- Response Structure: `candidates[].content`
- Model Naming: `gemini-1.5-pro`, `gemini-3.1-pro`, etc.

### Anthropic Claude Identification Features
- Endpoint: `/v1/messages`
- Request Parameters: `model`, `messages`, `max_tokens`, etc.
- Response Structure: `content[].text`
- Model Naming: `claude-3-opus-20240229`, `claude-5-sonnet`, etc.

## Testing

Run test scripts to verify system functionality:

```bash
python test_core.py
```

Or run comprehensive tests:

```bash
python tests/test_comprehensive.py
```

## Deployment

### Docker Deployment

1. Create Dockerfile:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. Build the image:

```bash
docker build -t model-detector .
```

3. Run the container:

```bash
docker run -p 5000:5000 model-detector
```

## Extension and Maintenance

### Adding New Model Support

1. Update the `model_patterns` dictionary in `app/core/detector.py`
2. Update corresponding endpoint and feature patterns

### Improving Identification Accuracy

- Add more feature extraction rules
- Optimize confidence calculation algorithm
- Increase training data

## Notes

- This system identifies based on API interface features, and may not be accurate for proxied or modified APIs
- As suppliers update their APIs, identification rules may need regular maintenance
- For mixed feature cases, the system will return results with lower confidence

## License

MIT License

---

# 大模型API检测系统

## 项目背景

作为一名拥有十年投资经验、最近投身AI创业的从业者，我在开发AI产品过程中发现了一个关键问题：通过API使用的token成为了重要的生产消耗。更令人担忧的是，我注意到同一模型在不同时候会表现出截然不同的能力。当我与模型对话时，模型直接报出自己是Sonnet模型，而非我调用的Opus模型，这证实了我的怀疑。

受此启发，我通过"vibe coding"开发了这个项目，以解决模型降级问题。该系统确保用户获得他们付费购买的确切模型，防止出现售卖高级模型API但输出低级模型、或通过coding plan的形式大幅增加低级模型输出比例的情况。

对于vibe coding乃至全领域的AI应用而言，模型能力是一个与输出效果挂钩的核心指标。本项目旨在消除任何形式的模型降级，确保AI API使用的透明度和可靠性。

我们面向中国用户的API平台为api.spiritgpu.com，有需要的用户可以关注我们。对于有使用需求的境外用户，我们也将在产品稳定运行后推出境外版本。

## 项目概述

本项目旨在构建一个对多个AI供应商模型API接口具备检测能力的系统，能够准确识别接入生文模型的供应商与模型型号。支持OpenAI、Google、Anthropic、Meta、Mistral、Minimax、DeepSeek、Step、Xiaomi等多家供应商的模型。

## 核心功能

- **多供应商识别**：准确识别OpenAI、Google、Anthropic、Meta、Mistral、Minimax、DeepSeek、Step、Xiaomi等多家供应商
- **模型型号识别**：识别具体的模型型号，如gpt-4o、gemini-1.5-pro、claude-3-opus、llama-3-70b、mistral-large等
- **置信度计算**：提供识别结果的置信度评分，按可靠性排序
- **详细分析**：返回详细的特征分析报告
- **API接口**：提供RESTful API接口，支持批量检测和实时测试
- **OpenRouter支持**：兼容OpenRouter上的模型，包括使用量排名前100的语言模型

## 技术栈

- 后端：Python 3.10+
- Web框架：Flask
- 数据处理：JSON
- 部署：Docker（可选）

## 项目结构

```
├── app/
│   ├── api/            # API路由
│   ├── core/           # 核心检测逻辑
│   ├── models/         # 数据模型
│   └── utils/          # 工具函数
├── tests/              # 测试用例
├── config.py           # 配置文件
├── requirements.txt    # 依赖项
├── app.py              # 应用入口
└── README.md           # 项目文档
```

## 安装说明

### 1. 克隆项目

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 上运行。

## API接口

### 检测接口

**URL**: `/api/detect`
**方法**: `POST`
**Content-Type**: `application/json`

**请求体**:
```json
{
  "request": {
    "endpoint": "/v1/chat/completions",
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.7
  },
  "response": {
    "choices": [{
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      }
    }]
  }
}
```

**响应**:
```json
{
  "supplier": "openai",
  "model": "gpt-4o",
  "confidence": 0.7777777777777778,
  "analysis": {
    "endpoint": "/v1/chat/completions",
    "model_name": "gpt-4o",
    "request_features": ["endpoint", "model", "messages", "messages[0]", "messages[0].role", "messages[0].content", "temperature"],
    "response_features": ["choices", "choices[0]", "choices[0].message", "choices[0].message.role", "choices[0].message.content"]
  }
}
```

### 健康检查接口

**URL**: `/api/health`
**方法**: `GET`

**响应**:
```json
{
  "status": "healthy"
}
```

### 实际API测试检测接口

**URL**: `/api/detect/test`
**方法**: `POST`
**Content-Type**: `application/json`

**请求体**:
```json
{
  "api_url": "https://api.example.com/v1/chat/completions",
  "api_key": "your-api-key",
  "test_models": ["gpt-4o", "gemini-1.5-pro", "claude-3-opus-20240229"]
}
```

**响应**:
```json
{
  "best_match": {
    "supplier": "openai",
    "model": "gpt-4o",
    "confidence": 0.7777777777777778,
    "model_tested": "gpt-4o",
    "response_status": 200,
    "analysis": {
      "endpoint": "https://api.example.com/v1/chat/completions",
      "model_name": "gpt-4o",
      "request_features": [...],
      "response_features": [...]
    }
  },
  "all_results": [
    {
      "supplier": "openai",
      "model": "gpt-4o",
      "confidence": 0.7777777777777778,
      "model_tested": "gpt-4o",
      "response_status": 200,
      "analysis": {...}
    },
    {
      "model_tested": "gemini-1.5-pro",
      "error": "Model not found"
    },
    {
      "model_tested": "claude-3-opus-20240229",
      "error": "Model not found"
    }
  ]
}
```

## 识别策略

### OpenAI识别特征
- 端点：`/v1/chat/completions`
- 请求参数：`model`, `messages`, `temperature`等
- 响应结构：`choices[].message`
- 模型命名：`gpt-3.5-turbo`, `gpt-4o`, `gpt-5`等

### Google Gemini识别特征
- 端点：`/generateContent`或`/v1/models/gemini-*-generateContent`
- 请求参数：`contents`, `generationConfig`等
- 响应结构：`candidates[].content`
- 模型命名：`gemini-1.5-pro`, `gemini-3.1-pro`等

### Anthropic Claude识别特征
- 端点：`/v1/messages`
- 请求参数：`model`, `messages`, `max_tokens`等
- 响应结构：`content[].text`
- 模型命名：`claude-3-opus-20240229`, `claude-5-sonnet`等

## 测试

运行测试脚本验证系统功能：

```bash
python test_core.py
```

或运行全面测试：

```bash
python tests/test_comprehensive.py
```

## 部署

### Docker部署

1. 创建Dockerfile：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. 构建镜像：

```bash
docker build -t model-detector .
```

3. 运行容器：

```bash
docker run -p 5000:5000 model-detector
```

## 扩展与维护

### 添加新模型支持

1. 在 `app/core/detector.py` 中更新 `model_patterns` 字典
2. 更新相应的端点和特征模式

### 提高识别准确率

- 添加更多特征提取规则
- 优化置信度计算算法
- 增加训练数据

## 注意事项

- 本系统基于API接口的特征进行识别，对于经过代理或修改的API可能识别不准确
- 随着各供应商API的更新，识别规则可能需要定期维护
- 对于混合特征的情况，系统会返回置信度较低的结果

## 许可证

MIT License