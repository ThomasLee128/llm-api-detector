import re
import json
from typing import Dict, Any, Optional, Tuple, List

class ModelDetector:
    """大模型API检测器"""
    
    def __init__(self):
        # 初始化模型模式和端点模式
        self.model_patterns = {
            'openai': [
                r'gpt-3\.5-turbo.*',
                r'gpt-4.*',
                r'gpt-4o.*',
                r'gpt-5.*'
            ],
            'google': [
                r'gemini-.*-pro.*',
                r'gemini-.*-ultra.*',
                r'gemini-.*-flash.*'
            ],
            'anthropic': [
                r'claude-3.*',
                r'claude-4.*',
                r'claude-5.*',
                r'claude.*opus.*',
                r'claude.*sonnet.*'
            ],
            'minimax': [
                r'minimax.*',
                r'm2\.5.*',
                r'm3.*'
            ],
            'deepseek': [
                r'deepseek.*',
                r'v3\.2.*',
                r'v3.*'
            ],
            'step': [
                r'^step.*',
                r'^Step.*'
            ],
            'xiaomi': [
                r'^xiaomi.*',
                r'^mimo.*',
                r'^mi.*',
                r'^MiMo.*'
            ],
            'meta': [
                r'^llama.*',
                r'^Llama.*'
            ],
            'mistral': [
                r'mistral.*',
                r'Mistral.*'
            ],
            'openrouter': [
                r'openrouter.*'
            ]
        }
        
        # OpenRouter上流行的模型列表（基于行业知识）
        self.popular_models = [
            # OpenAI
            'gpt-4o',
            'gpt-4o-2024-08-06',
            'gpt-4-turbo',
            'gpt-3.5-turbo',
            'gpt-5-preview',
            # Google
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-1.5-ultra',
            # Anthropic
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-3.5-sonnet',
            'claude-4-opus',
            'claude-4-sonnet',
            # Meta
            'llama-3-70b',
            'llama-3-8b',
            'llama-3.1-70b',
            'llama-3.1-8b',
            'llama-2-70b',
            'llama-2-13b',
            # Mistral
            'mistral-large',
            'mistral-medium',
            'mistral-small',
            'mistral-7b-v0.1',
            'mistral-7b-v0.2',
            # Minimax
            'minimax-m2.5',
            'minimax-m3',
            # DeepSeek
            'deepseek-v3.2',
            'deepseek-llm-7b-chat',
            # Step
            'step-3.5-flash',
            # Xiaomi
            'xiaomi-mimo-v2-pro',
            # Other popular models
            'mixtral-8x7b',
            'falcon-40b',
            'falcon-7b',
            'bloom-176b',
            'bloom-7b',
            'gpt-j-6b',
            'gpt-neo-2.7b',
            'gpt-neo-1.3b',
            'gpt-neo-0.5b',
            'llama-3-405b',
            'llama-3-14b',
            'gemini-1.0-pro',
            'gemini-1.0-ultra',
            'claude-2',
            'claude-2.1',
            'claude-2.0',
            'gpt-4',
            'gpt-4-32k',
            'gpt-3.5-turbo-16k',
            'gpt-3.5-turbo-instruct',
            'gpt-4-vision-preview',
            'gpt-4o-mini',
            'gemini-1.5-pro-lite',
            'gemini-1.5-flash-lite',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-3.5-sonnet-20240620',
            'claude-4-opus-20240229',
            'claude-4-sonnet-20240229',
            'llama-3-70b-instruct',
            'llama-3-8b-instruct',
            'llama-3.1-70b-instruct',
            'llama-3.1-8b-instruct',
            'llama-2-70b-chat',
            'llama-2-13b-chat',
            'llama-2-7b-chat',
            'mistral-large-20240229',
            'mistral-medium-20240229',
            'mistral-small-20240229',
            'mixtral-8x7b-instruct',
            'falcon-40b-instruct',
            'falcon-7b-instruct',
            'bloom-176b-chat',
            'bloom-7b-chat',
            'gpt-j-6b-chat',
            'gpt-neo-2.7b-chat',
            'gpt-neo-1.3b-chat',
            'gpt-neo-0.5b-chat',
            'minimax-m2.5-chat',
            'minimax-m3-chat',
            'deepseek-v3.2-chat',
            'deepseek-llm-7b-chat-v1',
            'step-3.5-flash-chat',
            'xiaomi-mimo-v2-pro-chat'
        ]
        
        self.endpoint_patterns = {
            'openai': [r'/v1/chat/completions'],
            'google': [r'/generateContent', r'/v1/models/gemini-.*-generateContent'],
            'anthropic': [r'/v1/messages'],
            'minimax': [r'/v1/chat/completions', r'/chat/completions'],
            'deepseek': [r'/v1/chat/completions', r'/chat/completions'],
            'step': [r'/v1/chat/completions', r'/chat/completions'],
            'xiaomi': [r'/v1/chat/completions', r'/chat/completions'],
            'meta': [r'/v1/chat/completions', r'/chat/completions'],
            'mistral': [r'/v1/chat/completions', r'/chat/completions'],
            'openrouter': [r'/v1/chat/completions', r'/chat/completions']
        }
        
        self.request_features = {
            'openai': ['model', 'messages', 'temperature'],
            'google': ['contents', 'generationConfig'],
            'anthropic': ['model', 'messages', 'max_tokens'],
            'minimax': ['model', 'messages', 'temperature'],
            'deepseek': ['model', 'messages', 'temperature'],
            'step': ['model', 'messages', 'temperature'],
            'xiaomi': ['model', 'messages', 'temperature'],
            'meta': ['model', 'messages', 'temperature'],
            'mistral': ['model', 'messages', 'temperature'],
            'openrouter': ['model', 'messages', 'temperature']
        }
        
        self.response_features = {
            'openai': ['choices', 'message'],
            'google': ['candidates', 'content'],
            'anthropic': ['content', 'text'],
            'minimax': ['choices', 'message'],
            'deepseek': ['choices', 'message'],
            'step': ['choices', 'message'],
            'xiaomi': ['choices', 'message'],
            'meta': ['choices', 'message'],
            'mistral': ['choices', 'message'],
            'openrouter': ['choices', 'message']
        }
    
    def detect(self, request_data: Dict[str, Any], response_data: Dict[str, Any]) -> Dict[str, Any]:
        """检测模型供应商和型号"""
        # 提取特征
        endpoint = self._extract_endpoint(request_data)
        model_name = self._extract_model_name(request_data)
        
        # 综合分析
        supplier, confidence = self._detect_supplier(
            endpoint, model_name, request_data, response_data
        )
        
        # 识别模型
        model = self._detect_model(model_name, supplier)
        
        return {
            'supplier': supplier,
            'model': model,
            'confidence': confidence,
            'analysis': {
                'endpoint': endpoint,
                'model_name': model_name,
                'request_features': self._extract_features(request_data),
                'response_features': self._extract_features(response_data)
            }
        }
    
    def detect_with_test(self, api_url: str, api_key: str, test_models: list = None) -> Dict[str, Any]:
        """使用实际API调用检测模型
        
        Args:
            api_url: API端点URL
            api_key: API密钥
            test_models: 要测试的模型列表，默认为常用模型
            
        Returns:
            检测结果
        """
        import requests
        
        if test_models is None:
            # 使用OpenRouter上流行的模型列表作为默认测试模型
            test_models = self.popular_models
        
        results = []
        
        for model in test_models:
            try:
                # 构造测试请求
                payload = {
                    'model': model,
                    'messages': [{'role': 'user', 'content': 'Hello, test message'}],
                    'temperature': 0.7
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }
                
                # 发送请求
                response = requests.post(api_url, json=payload, headers=headers, timeout=10)
                response_data = response.json()
                
                # 分析响应
                request_data = {
                    'endpoint': api_url,
                    'model': model,
                    'messages': payload['messages'],
                    'temperature': payload['temperature']
                }
                
                result = self.detect(request_data, response_data)
                result['model_tested'] = model
                result['response_status'] = response.status_code
                results.append(result)
                
            except Exception as e:
                results.append({
                    'model_tested': model,
                    'error': str(e)
                })
        
        # 分析结果
        valid_results = [r for r in results if 'error' not in r]
        
        if valid_results:
            # 按置信度排序
            sorted_results = sorted(valid_results, key=lambda x: x['confidence'], reverse=True)
            
            # 构建友好格式的结果
            formatted_results = []
            for result in sorted_results:
                formatted_results.append({
                    'supplier': result['supplier'],
                    'model': result['model'],
                    'confidence': round(result['confidence'], 3)
                })
            
            # 选择置信度最高的结果
            best_result = sorted_results[0]
            return {
                'best_match': best_result,
                'sorted_results': formatted_results,
                'all_results': results
            }
        else:
            return {
                'error': 'All test requests failed',
                'all_results': results
            }
    
    def _extract_endpoint(self, request_data: Dict[str, Any]) -> Optional[str]:
        """提取端点路径"""
        return request_data.get('endpoint') or request_data.get('path')
    
    def _extract_model_name(self, request_data: Dict[str, Any]) -> Optional[str]:
        """提取模型名称"""
        return request_data.get('model')
    
    def _detect_supplier(self, endpoint: Optional[str], model_name: Optional[str], 
                        request_data: Dict[str, Any], response_data: Dict[str, Any]) -> Tuple[str, float]:
        """检测供应商"""
        scores = {
            'openai': 0,
            'google': 0,
            'anthropic': 0,
            'minimax': 0,
            'deepseek': 0,
            'step': 0,
            'xiaomi': 0,
            'meta': 0,
            'mistral': 0,
            'openrouter': 0
        }
        
        # 端点匹配
        if endpoint:
            for supplier, patterns in self.endpoint_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, endpoint):
                        scores[supplier] += 3
        
        # 模型名称匹配
        if model_name:
            for supplier, patterns in self.model_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, model_name, re.IGNORECASE):
                        # 为所有供应商增加模型名称匹配的权重
                        # 特别是对于非OpenAI兼容格式的供应商
                        scores[supplier] += 12
        
        # 请求特征匹配 - 只有当供应商的特定特征存在时才加分
        for supplier, features in self.request_features.items():
            for feature in features:
                if feature in request_data:
                    # 对于OpenAI，'temperature'是重要特征
                    if supplier == 'openai' and feature == 'temperature':
                        scores[supplier] += 2
                    # 对于Google，'generationConfig'是重要特征
                    elif supplier == 'google' and feature == 'generationConfig':
                        scores[supplier] += 2
                    # 对于Anthropic，'max_tokens'是重要特征
                    elif supplier == 'anthropic' and feature == 'max_tokens':
                        scores[supplier] += 2
                    else:
                        scores[supplier] += 1
        
        # 响应特征匹配 - 只有当供应商的特定特征存在时才加分
        for supplier, features in self.response_features.items():
            for feature in features:
                if self._has_feature(response_data, feature):
                    # 对于OpenAI，'choices'和'message'是重要特征
                    if supplier == 'openai' and (feature == 'choices' or feature == 'message'):
                        scores[supplier] += 2
                    # 对于Google，'candidates'和'content'是重要特征
                    elif supplier == 'google' and (feature == 'candidates' or feature == 'content'):
                        scores[supplier] += 2
                    # 对于Anthropic，'content'和'text'是重要特征
                    elif supplier == 'anthropic' and (feature == 'content' or feature == 'text'):
                        scores[supplier] += 2
                    else:
                        scores[supplier] += 1
        
        # 计算置信度
        total_score = sum(scores.values())
        if total_score == 0:
            return 'unknown', 0.0
        
        # 检查最高分是否显著高于其他分数
        best_score = max(scores.values())
        other_scores = sum(scores.values()) - best_score
        
        # 对于只有一个非零分数的情况，直接返回该供应商
        non_zero_scores = [score for score in scores.values() if score > 0]
        if len(non_zero_scores) == 1:
            best_supplier = max(scores, key=scores.get)
            confidence = best_score / sum(scores.values())
            return best_supplier, confidence
        
        # 对于多个非零分数的情况，要求最高分至少是第二高分的1.5倍
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) >= 2:
            second_best_score = sorted_scores[1]
        else:
            second_best_score = 0
        
        # 如果最高分至少是第二高分的1.5倍，或者只有一个非零分数，则认为识别成功
        if second_best_score > 0 and best_score < 1.5 * second_best_score:
            # 调试：打印得分情况
            print(f"Debug: Scores={scores}, Best score={best_score}, Second best={second_best_score}")
            return 'unknown', 0.0
        
        best_supplier = max(scores, key=scores.get)
        confidence = best_score / total_score
        
        return best_supplier, confidence
    
    def _detect_model(self, model_name: Optional[str], supplier: str) -> str:
        """检测模型型号"""
        if not model_name:
            return 'unknown'
        
        # 验证模型名称是否匹配供应商
        patterns = self.model_patterns.get(supplier, [])
        for pattern in patterns:
            if re.search(pattern, model_name):
                return model_name
        
        return 'unknown'
    
    def _has_feature(self, data: Dict[str, Any], feature: str) -> bool:
        """检查数据是否包含特征"""
        if feature in data:
            return True
        
        # 递归检查嵌套结构
        for value in data.values():
            if isinstance(value, dict):
                if self._has_feature(value, feature):
                    return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        if self._has_feature(item, feature):
                            return True
        
        return False
    
    def _extract_features(self, data: Dict[str, Any]) -> list:
        """提取数据特征"""
        features = []
        
        def extract(obj, path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    features.append(new_path)
                    extract(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    features.append(new_path)
                    extract(item, new_path)
        
        extract(data)
        return features
