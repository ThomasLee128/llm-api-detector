#!/usr/bin/env python3
"""独立测试脚本，验证核心检测逻辑"""

# 直接导入detector模块，避免Flask依赖
import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_openai():
    """测试OpenAI检测"""
    detector = ModelDetector()
    
    request_data = {
        'endpoint': '/v1/chat/completions',
        'model': 'gpt-4o',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'temperature': 0.7
    }
    
    response_data = {
        'choices': [
            {
                'message': {
                    'role': 'assistant',
                    'content': 'Hello! How can I help you today?'
                }
            }
        ]
    }
    
    result = detector.detect(request_data, response_data)
    print("OpenAI测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_google():
    """测试Google检测"""
    detector = ModelDetector()
    
    request_data = {
        'endpoint': '/generateContent',
        'contents': [{'role': 'user', 'parts': [{'text': 'Hello'}]}],
        'generationConfig': {'temperature': 0.7}
    }
    
    response_data = {
        'candidates': [
            {
                'content': {
                    'parts': [{'text': 'Hello! How can I help you today?'}]
                }
            }
        ]
    }
    
    result = detector.detect(request_data, response_data)
    print("Google测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_anthropic():
    """测试Anthropic检测"""
    detector = ModelDetector()
    
    request_data = {
        'endpoint': '/v1/messages',
        'model': 'claude-3-opus-20240229',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 100
    }
    
    response_data = {
        'content': [
            {
                'text': 'Hello! How can I help you today?'
            }
        ]
    }
    
    result = detector.detect(request_data, response_data)
    print("Anthropic测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_unknown():
    """测试未知模型检测"""
    detector = ModelDetector()
    
    request_data = {
        'endpoint': '/unknown',
        'model': 'unknown-model'
    }
    
    response_data = {}
    
    result = detector.detect(request_data, response_data)
    print("未知模型测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

if __name__ == '__main__':
    print("=== 大模型API检测系统测试 ===")
    print()
    test_openai()
    test_google()
    test_anthropic()
    test_unknown()
    print("=== 测试完成 ===")
