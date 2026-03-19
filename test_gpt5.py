#!/usr/bin/env python3
"""测试GPT-5模型识别"""

import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_gpt5_detection():
    """测试GPT-5模型检测"""
    detector = ModelDetector()
    
    # 测试GPT-5模型
    request_data = {
        'endpoint': '/v1/chat/completions',
        'model': 'gpt-5',
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
    print("GPT-5测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试GPT-5的变体
    request_data['model'] = 'gpt-5-turbo'
    result = detector.detect(request_data, response_data)
    print("GPT-5-turbo测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()

if __name__ == '__main__':
    print("=== 测试GPT-5模型识别 ===")
    print()
    test_gpt5_detection()
    print("=== 测试完成 ===")
