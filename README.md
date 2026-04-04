# 大模型API检测系统

## 项目背景

作为一名拥有十年投资经验、最近投身AI创业的从业者，我在开发AI产品过程中发现了一个关键问题：通过API使用的token成为了重要的生产消耗。更令人担忧的是，我注意到同一模型在不同时候会表现出截然不同的能力。当我与模型对话时，模型直接报出自己是Sonnet模型，而非我调用的Opus模型，这证实了我的怀疑。

受此启发，我通过"vibe coding"开发了这个项目，以解决模型降级问题。该系统确保用户获得他们付费购买的确切模型，防止出现售卖高级模型API但输出低级模型、或通过coding plan的形式大幅增加低级模型输出比例的情况。

对于vibe coding乃至全领域的AI应用而言，模型能力是一个与输出效果挂钩的核心指标。本项目旨在消除任何形式的模型降级，确保AI API使用的透明度和可靠性。

我们面向中国用户的API平台为api.spiritgpu.com，有需要的用户可以关注我们。对于有使用需求的境外用户，我们也将在产品稳定运行后推出境外版本。

## 项目概述

本项目旨在构建一个对多个AI供应商模型API接口具备检测能力的系统，能够准确识别接入生文模型的供应商与模型型号。支持OpenAI、Google、Anthropic、MiniMax、DeepSeek、Step、智谱、月之暗面、通义千问、小米等多家主流供应商的模型。

## 核心功能

- **单次模型测试**：快速测试单个模型的真实性和Token使用情况
- **批量模型测试**：支持API聚合站，自动获取可用模型并进行批量检测
- **智能模型匹配**：识别模型核心名称，对高度相似的模型名进行智能匹配
- **生图/生视频模型过滤**：自动过滤非生文模型，避免误测试
- **Token使用统计**：记录并展示Token使用情况，方便用户自行与平台账单核对
- **实时进度展示**：批量测试时显示进度条和进度日志
- **美观简洁的UI**：清爽的界面设计，专业易用

## 技术栈

- 后端：Python 3.10+
- Web框架：Flask
- 数据存储：SQLite
- 前端：原生JavaScript + CSS
- 部署：Docker（可选）

## 项目结构

```
├── app/
│   ├── api/            # API路由
│   ├── core/           # 核心检测逻辑
│   ├── models/         # 数据模型和数据库
│   └── utils/          # 工具函数
├── static/             # 静态资源
│   ├── css/            # 样式文件
│   └── js/             # JavaScript文件
├── templates/          # HTML模板
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
cd <project-directory>/llm-api-detector
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:8080` 上运行。

## 使用说明

### 单次模型测试

1. 在"单次测试"面板输入API URL和API Key
2. 点击"获取可用模型"按钮自动拉取该端点的可用模型
3. 从下拉列表中选择要测试的模型
4. 点击"开始测试"
5. 查看测试结果和Token使用情况

### 批量模型测试

1. 在"批量测试"面板输入API URL和API Key
2. 点击"第一步：获取可用模型"按钮
3. 从获取到的模型列表中勾选要测试的模型
4. 点击"第二步：开始检测"
5. 观看进度条实时更新
6. 查看完整的检测报告

## 支持的模型

系统支持多家主流供应商的模型，包括但不限于：

- **OpenAI**: GPT-4o, GPT-5系列
- **Anthropic**: Claude Opus/Sonnet/Haiku系列
- **Google**: Gemini 2.5/3.1系列
- **DeepSeek**: DeepSeek V3.2系列
- **智谱**: GLM-5系列
- **月之暗面**: Kimi K2.5系列
- **通义千问**: Qwen 3/3.5系列
- **小米**: MiMo V2 Pro
- **阶跃星辰**: Step 3.5系列
- **MiniMax**: M2.5/M2.7系列
- 以及更多...

## 检测原理

### 1. 模型名称检测
- 通过API响应中的`model`字段获取实际调用的模型名
- 与请求的模型名进行匹配
- 支持核心名称匹配（如`gpt-4o`和`gpt-4o-2024-11-20`）

### 2. 供应商识别
- 基于模型命名模式识别供应商
- 支持17+主流供应商的识别

### 3. 响应时间分析
- 记录API响应时间
- 与正常响应时间范围进行对比

### 4. Token使用统计
- 记录Prompt Token、Completion Token和Total Token
- 突出展示，方便用户自行与平台账单核对

## 注意事项

- 本系统基于API接口的特征进行识别，对于经过代理或修改的API可能识别不准确
- 随着各供应商API的更新，识别规则可能需要定期维护
- Token一致性检测已移除，改为由用户自行核对
- 生图/生视频模型会被自动过滤，仅测试生文模型

## 更新日志

### 2026-04-04
- **修复**: 修改聚合站检测超时时间为15秒，超过15秒无响应视为不通
- **优化**: 单次测试结果中添加醒目的"模型返回内容"板块
- **更新**: 单次模型测试默认提示词改为更直接的身份质询
- **修复**: 确保输入框支持文本选择和键盘快捷键（Ctrl+A等）

## 许可证

MIT License

---

# Large Language Model API Detection System

## Project Background

As an investor with ten years of experience who has recently ventured into AI entrepreneurship, I discovered a critical issue while developing our AI products: the token consumption through API usage became a significant production cost. More alarmingly, I noticed that the same model would exhibit drastically different capabilities at different times. This suspicion was confirmed when a model I was conversing with directly revealed it was a Sonnet model, despite me explicitly calling the Opus model.

Driven by this discovery, I developed this project through "vibe coding" to address the problem of model downgrading. This system ensures that users receive the exact model they pay for, preventing scenarios where premium model APIs are sold but deliver lower-tier models, or where coding plans are used to significantly increase the proportion of lower-tier model outputs.

For vibe coding and the entire AI application domain, model capability is a core indicator directly linked to output quality. This project aims to eliminate any form of model downgrading, ensuring transparency and reliability in AI API usage.

Our API platform for Chinese users is api.spiritgpu.com, and we plan to launch an international version once the product stabilizes.

## Project Overview

This project aims to build a system capable of detecting API interfaces from multiple AI suppliers, accurately identifying the supplier and model type of the accessed language model. It supports models from OpenAI, Google, Anthropic, MiniMax, DeepSeek, Step, Zhipu, Moonshot, Qwen, Xiaomi, and other popular providers.

## Core Features

- **Single Model Test**: Quickly test the authenticity and token usage of individual models
- **Batch Model Test**: Support API aggregators, automatically fetch available models and perform batch detection
- **Smart Model Matching**: Identify model core names and intelligently match highly similar model names
- **Image/Video Model Filtering**: Automatically filter non-text models to avoid accidental testing
- **Token Usage Statistics**: Record and display token usage for users to verify with platform billing
- **Real-time Progress Display**: Show progress bar and logs during batch testing
- **Clean and Elegant UI**: Professional, easy-to-use interface design

## Technology Stack

- Backend: Python 3.10+
- Web Framework: Flask
- Data Storage: SQLite
- Frontend: Vanilla JavaScript + CSS
- Deployment: Docker (optional)

## Project Structure

```
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core detection logic
│   ├── models/         # Data models and database
│   └── utils/          # Utility functions
├── static/             # Static resources
│   ├── css/            # Style files
│   └── js/             # JavaScript files
├── templates/          # HTML templates
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
cd <project-directory>/llm-api-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Service

```bash
python app.py
```

The service will run at `http://localhost:8080`.

## Usage Guide

### Single Model Test

1. Enter API URL and API Key in the "Single Test" panel
2. Click "Get Available Models" to automatically fetch models from the endpoint
3. Select the model to test from the dropdown
4. Click "Start Test"
5. View test results and token usage

### Batch Model Test

1. Enter API URL and API Key in the "Batch Test" panel
2. Click "Step 1: Get Available Models"
3. Select models to test from the fetched list
4. Click "Step 2: Start Detection"
5. Watch the progress bar update in real-time
6. View the complete detection report

## Supported Models

The system supports models from many major providers, including but not limited to:

- **OpenAI**: GPT-4o, GPT-5 series
- **Anthropic**: Claude Opus/Sonnet/Haiku series
- **Google**: Gemini 2.5/3.1 series
- **DeepSeek**: DeepSeek V3.2 series
- **Zhipu**: GLM-5 series
- **Moonshot**: Kimi K2.5 series
- **Qwen**: Qwen 3/3.5 series
- **Xiaomi**: MiMo V2 Pro
- **Step**: Step 3.5 series
- **MiniMax**: M2.5/M2.7 series
- And many more...

## Detection Principles

### 1. Model Name Detection
- Get the actual model name from the `model` field in API responses
- Compare with the requested model name
- Support core name matching (e.g., `gpt-4o` and `gpt-4o-2024-11-20`)

### 2. Supplier Identification
- Identify suppliers based on model naming patterns
- Support identification of 17+ major suppliers

### 3. Response Time Analysis
- Record API response time
- Compare with normal response time ranges

### 4. Token Usage Statistics
- Record Prompt Token, Completion Token, and Total Token
- Highlight display for users to verify with platform billing

## Notes

- This system identifies based on API interface features, and may not be accurate for proxied or modified APIs
- As suppliers update their APIs, identification rules may need regular maintenance
- Token consistency checking has been removed, replaced by user self-verification
- Image/video models are automatically filtered, only text models are tested

## Changelog

### 2026-04-04 (Beijing Time)
- **Fix**: Changed aggregator detection timeout to 15 seconds, no response after 15 seconds considered as unavailable
- **Improvement**: Added prominent "Model Response Content" section in single test results
- **Update**: Changed default prompt for single model test to more direct identity inquiry
- **Fix**: Ensure input fields support text selection and keyboard shortcuts (Ctrl+A, etc.)

## License

MIT License
