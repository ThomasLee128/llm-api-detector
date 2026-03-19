import unittest
from app.core.detector import ModelDetector

class TestModelDetector(unittest.TestCase):
    """测试模型检测器"""
    
    def setUp(self):
        self.detector = ModelDetector()
    
    def test_openai_detection(self):
        """测试OpenAI模型检测"""
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
        
        result = self.detector.detect(request_data, response_data)
        self.assertEqual(result['supplier'], 'openai')
        self.assertEqual(result['model'], 'gpt-4o')
        self.assertGreater(result['confidence'], 0.8)
    
    def test_google_detection(self):
        """测试Google Gemini模型检测"""
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
        
        result = self.detector.detect(request_data, response_data)
        self.assertEqual(result['supplier'], 'google')
        self.assertGreater(result['confidence'], 0.8)
    
    def test_anthropic_detection(self):
        """测试Anthropic Claude模型检测"""
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
        
        result = self.detector.detect(request_data, response_data)
        self.assertEqual(result['supplier'], 'anthropic')
        self.assertEqual(result['model'], 'claude-3-opus-20240229')
        self.assertGreater(result['confidence'], 0.8)
    
    def test_unknown_detection(self):
        """测试未知模型检测"""
        request_data = {
            'endpoint': '/unknown',
            'model': 'unknown-model'
        }
        
        response_data = {}
        
        result = self.detector.detect(request_data, response_data)
        self.assertEqual(result['supplier'], 'unknown')
        self.assertEqual(result['model'], 'unknown')
        self.assertEqual(result['confidence'], 0.0)

if __name__ == '__main__':
    unittest.main()
