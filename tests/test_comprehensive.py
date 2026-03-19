#!/usr/bin/env python3
"""全面测试脚本，覆盖更多场景"""

import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_openai_variants():
    """测试OpenAI模型变体"""
    detector = ModelDetector()
    
    # 测试gpt-3.5-turbo
    request_data = {
        'endpoint': '/v1/chat/completions',
        'model': 'gpt-3.5-turbo',
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
    print("OpenAI gpt-3.5-turbo测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试gpt-4
    request_data['model'] = 'gpt-4'
    result = detector.detect(request_data, response_data)
    print("OpenAI gpt-4测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_google_variants():
    """测试Google Gemini模型变体"""
    detector = ModelDetector()
    
    # 测试gemini-1.5-pro
    request_data = {
        'endpoint': '/generateContent',
        'model': 'gemini-1.5-pro',
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
    print("Google gemini-1.5-pro测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试gemini-3.1-pro
    request_data['model'] = 'gemini-3.1-pro'
    result = detector.detect(request_data, response_data)
    print("Google gemini-3.1-pro测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_anthropic_variants():
    """测试Anthropic Claude模型变体"""
    detector = ModelDetector()
    
    # 测试claude-3-sonnet
    request_data = {
        'endpoint': '/v1/messages',
        'model': 'claude-3-sonnet-20240229',
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
    print("Anthropic claude-3-sonnet测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试claude-5-sonnet
    request_data['model'] = 'claude-5-sonnet'
    result = detector.detect(request_data, response_data)
    print("Anthropic claude-5-sonnet测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

def test_edge_cases():
    """测试边缘情况"""
    detector = ModelDetector()
    
    # 测试缺少端点
    request_data = {
        'model': 'gpt-4o',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    }
    response_data = {
        'choices': [{'message': {'content': 'Hello!'}}]
    }
    
    result = detector.detect(request_data, response_data)
    print("缺少端点测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试缺少模型名称
    request_data = {
        'endpoint': '/v1/chat/completions',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    }
    
    result = detector.detect(request_data, response_data)
    print("缺少模型名称测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

if __name__ == '__main__':
    print("=== 全面测试大模型API检测系统 ===")
    print()
    test_openai_variants()
    test_google_variants()
    test_anthropic_variants()
    test_edge_cases()
    print("=== 测试完成 ===")
