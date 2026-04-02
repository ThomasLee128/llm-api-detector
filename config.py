import os


class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # 数据库配置
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'test_history.db'
    
    # API配置
    API_TIMEOUT = 30  # 秒
    
    # 测试配置
    DEFAULT_NUM_TESTS = 3
    MAX_TEST_MODELS = 20
