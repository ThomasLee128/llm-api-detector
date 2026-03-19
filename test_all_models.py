#!/usr/bin/env python3
"""测试所有主流模型的识别能力"""

import sys
sys.path.append('.')
from app.core.detector import ModelDetector

def test_all_models():
    """测试所有主流模型的识别"""
    detector = ModelDetector()
    
    # 测试模型列表
    test_models = [
        # OpenAI
        ('openai', 'gpt-3.5-turbo'),
        ('openai', 'gpt-4'),
        ('openai', 'gpt-4o'),
        ('openai', 'gpt-5'),
        
        # Google
        ('google', 'gemini-1.5-pro'),
        ('google', 'gemini-1.5-ultra'),
        ('google', 'gemini-3.1-pro'),
        ('google', 'gemini-3.1-flash'),
        
        # Anthropic
        ('anthropic', 'claude-3-opus-20240229'),
        ('anthropic', 'claude-3-sonnet-20240229'),
        ('anthropic', 'claude-4.6'),
        ('anthropic', 'claude-5-sonnet'),
        ('anthropic', 'Claude Opus 4.6'),
        ('anthropic', 'claude sonnet 5'),
        
        # Minimax
        ('minimax', 'minimax-m2.5'),
        ('minimax', 'M2.5'),
        ('minimax', 'minimax-m3'),
        
        # DeepSeek
        ('deepseek', 'deepseek-v3.2'),
        ('deepseek', 'DeepSeek-V3'),
        ('deepseek', 'deepseek-coder'),
        
        # Step
        ('step', 'step-3.5-flash'),
        ('step', 'Step 3.5'),
        ('step', 'step-flash'),
        
        # Xiaomi
        ('xiaomi', 'xiaomi-mimo-v2-pro'),
        ('xiaomi', 'MiMo-V2'),
        ('xiaomi', 'mi-mimo'),
        
        # Meta
        ('meta', 'llama-3-70b'),
        ('meta', 'Llama 3 8b'),
        ('meta', 'llama-2-70b'),
        
        # Mistral
        ('mistral', 'mistral-large'),
        ('mistral', 'Mistral 7b'),
        ('mistral', 'mistral-small')
    ]
    
    results = []
    
    for expected_supplier, model_name in test_models:
        # 构造测试请求
        request_data = {
            'endpoint': '/v1/chat/completions',
            'model': model_name,
            'messages': [{'role': 'user', 'content': 'Hello'}]
        }
        
        # 根据供应商添加特定参数
        if expected_supplier == 'openai':
            request_data['temperature'] = 0.7
        elif expected_supplier == 'google':
            request_data['contents'] = [{'role': 'user', 'parts': [{'text': 'Hello'}]}]
            request_data['generationConfig'] = {'temperature': 0.7}
            request_data['endpoint'] = '/generateContent'
        elif expected_supplier == 'anthropic':
            request_data['max_tokens'] = 100
            request_data['endpoint'] = '/v1/messages'
        else:
            # 其他供应商使用OpenAI兼容格式
            request_data['temperature'] = 0.7
        
        # 构造测试响应
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
        
        # 特殊处理Google和Anthropic的响应格式
        if expected_supplier == 'google':
            response_data = {
                'candidates': [
                    {
                        'content': {
                            'parts': [{'text': 'Hello! How can I help you today?'}]
                        }
                    }
                ]
            }
        elif expected_supplier == 'anthropic':
            response_data = {
                'content': [
                    {
                        'text': 'Hello! How can I help you today?'
                    }
                ]
            }
        
        # 执行检测
        result = detector.detect(request_data, response_data)
        result['expected_supplier'] = expected_supplier
        result['model_tested'] = model_name
        results.append(result)
    
    # 按置信度排序
    results.sort(key=lambda x: x['confidence'], reverse=True)
    
    # 打印结果
    print("=== 模型识别测试结果（按置信度排序）===")
    print()
    
    for i, result in enumerate(results, 1):
        expected = result['expected_supplier']
        actual = result['supplier']
        status = "✓" if expected == actual else "✗"
        
        print(f"{i}. {status} {result['model_tested']}")
        print(f"   期望供应商: {expected}")
        print(f"   实际供应商: {actual}")
        print(f"   识别模型: {result['model']}")
        print(f"   置信度: {result['confidence']:.4f}")
        print()
    
    # 统计准确率
    correct = sum(1 for r in results if r['expected_supplier'] == r['supplier'])
    total = len(results)
    accuracy = correct / total if total > 0 else 0
    
    print(f"=== 测试统计 ===")
    print(f"测试模型数: {total}")
    print(f"正确识别: {correct}")
    print(f"准确率: {accuracy:.2f}")
    print()

if __name__ == '__main__':
    test_all_models()
