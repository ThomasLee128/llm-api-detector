from flask import Blueprint, request, jsonify
from app.core.detector import ModelDetector

api_bp = Blueprint('api', __name__)
detector = ModelDetector()

@api_bp.route('/detect', methods=['POST'])
def detect_model():
    """检测模型供应商和型号"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Missing request data'
            }), 400
        
        request_data = data.get('request', {})
        response_data = data.get('response', {})
        
        if not request_data:
            return jsonify({
                'error': 'Missing request data'
            }), 400
        
        result = detector.detect(request_data, response_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/detect/test', methods=['POST'])
def detect_with_test():
    """使用实际API调用检测模型"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Missing request data'
            }), 400
        
        api_url = data.get('api_url')
        api_key = data.get('api_key')
        test_models = data.get('test_models')
        
        if not api_url or not api_key:
            return jsonify({
                'error': 'Missing api_url or api_key'
            }), 400
        
        result = detector.detect_with_test(api_url, api_key, test_models)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy'
    }), 200
