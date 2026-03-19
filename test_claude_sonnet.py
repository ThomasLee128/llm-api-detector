#!/usr/bin/env python3
"""测试Claude Sonnet族系模型识别"""

import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_claude_sonnet_detection():
    """测试Claude Sonnet模型检测"""
    detector = ModelDetector()
    
    # 测试基础Claude Sonnet模型
    request_data = {
        'endpoint': '/v1/messages',
        'model': 'claude sonnet',
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
    
    # 测试各种Claude Sonnet变体
    test_models = [
        'claude sonnet',
        'Claude Sonnet',
        'claude-sonnet',
        'Claude-Sonnet',
        'claude sonnet 3',
        'Claude Sonnet 3',
        'claude-sonnet-3',
        'claude sonnet 4',
        'Claude Sonnet 4',
        'claude-sonnet-4',
        'claude sonnet 5',
        'Claude Sonnet 5',
        'claude-sonnet-5',
        'claude sonnet 20240229',
        'Claude Sonnet 20240229',
        'claude-sonnet-20240229'
    ]
    
    for model in test_models:
        request_data['model'] = model
        result = detector.detect(request_data, response_data)
        print(f"{model}测试结果:")
        print(f"供应商: {result['supplier']}")
        print(f"模型: {result['model']}")
        print(f"置信度: {result['confidence']}")
        print()

if __name__ == '__main__':
    print("=== 测试Claude Sonnet族系模型识别 ===")
    print()
    test_claude_sonnet_detection()
    print("=== 测试完成 ===")
