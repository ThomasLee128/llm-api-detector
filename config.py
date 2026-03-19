# 项目配置文件

class Config:
    """应用配置"""
    SECRET_KEY = 'dev'
    DEBUG = True
    
    # 模型识别配置
    MODEL_PATTERNS = {
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
    
    # 端点特征
    ENDPOINT_PATTERNS = {
        'openai': [
            r'/v1/chat/completions'
        ],
        'google': [
            r'/generateContent',
            r'/v1/models/gemini-.*-generateContent'
        ],
        'anthropic': [
            r'/v1/messages'
        ],
        'minimax': [r'/v1/chat/completions', r'/chat/completions'],
        'deepseek': [r'/v1/chat/completions', r'/chat/completions'],
        'step': [r'/v1/chat/completions', r'/chat/completions'],
        'xiaomi': [r'/v1/chat/completions', r'/chat/completions'],
        'meta': [r'/v1/chat/completions', r'/chat/completions'],
        'mistral': [r'/v1/chat/completions', r'/chat/completions'],
        'openrouter': [r'/v1/chat/completions', r'/chat/completions']
    }
    
    # 请求特征
    REQUEST_FEATURES = {
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
    
    # 响应特征
    RESPONSE_FEATURES = {
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
