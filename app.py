from config import Config

# 只在直接运行时导入Flask
if __name__ == '__main__':
    from flask import Flask
    from app.api.routes import api_bp
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 注册API路由
    app.register_blueprint(api_bp, url_prefix='/api')
    
    app.run(host='0.0.0.0', port=5000)
