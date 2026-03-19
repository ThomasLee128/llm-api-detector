# 大模型API检测系统架构设计

## 系统概述

本系统旨在检测和识别OpenAI、Google和Anthropic三家企业的模型API接口，能够准确识别接入生文模型的供应商与模型型号。

## 核心架构

### 1. 输入处理模块
- 接收API请求/响应样本
- 解析JSON格式数据
- 标准化输入格式

### 2. 特征提取模块
- 提取端点路径特征
- 提取请求参数特征
- 提取响应结构特征
- 提取模型命名特征

### 3. 识别模块
- 供应商识别（OpenAI/Google/Anthropic）
- 模型型号识别
- 置信度计算

### 4. 结果输出模块
- 返回识别结果
- 提供详细分析报告
- 支持批量检测

### 5. 测试验证模块
- 验证识别准确性
- 收集和更新特征库

## 技术栈

- 后端：Python 3.10+
- Web框架：Flask
- 数据处理：Pandas, JSON
- 部署：Docker

## API接口设计

### 检测接口
```
POST /api/detect
Content-Type: application/json

{
  "request": {...},  // API请求数据
  "response": {...}  // API响应数据
}
```

### 响应格式
```json
{
  "supplier": "openai",  // openai, google, anthropic
  "model": "gpt-4o",     // 模型型号
  "confidence": 0.98,     // 置信度
  "analysis": {...}       // 详细分析
}
```

## 识别策略

### OpenAI识别特征
- 端点：`/v1/chat/completions`
- 请求参数：`model`, `messages`, `temperature`等
- 响应结构：`choices[].message`
- 模型命名：`gpt-3.5-turbo`, `gpt-4o`等

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
└── app.py              # 应用入口
```