#!/usr/bin/env python3
"""测试Claude Opus 4.6模型识别"""

import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_claude_opus_detection():
    """测试Claude Opus模型检测"""
    detector = ModelDetector()
    
    # 测试claude opus 4-6模型
    request_data = {
        'endpoint': '/v1/messages',
        'model': 'claude opus 4-6',
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
    print("Claude Opus 4-6测试结果:")
    print(f"供应商: {result['supplier']}")
    print(f"模型: {result['model']}")
    print(f"置信度: {result['confidence']}")
    print()
    
    # 测试其他Claude Opus变体
    test_models = [
        'Claude Opus 4.6',
        'claude-opus-4.6',
        'Claude Opus 4',
        'claude opus 5'
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
    print("=== 测试Claude Opus模型识别 ===")
    print()
    test_claude_opus_detection()
    print("=== 测试完成 ===")
