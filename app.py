from config import Config
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(Config)

# 导入并注册API蓝图
from app.api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
