import uuid
import threading
from flask import Blueprint, request, jsonify
from dataclasses import asdict
from app.core.detector import EnhancedModelDetector
from app.core.task_manager import task_manager, TaskStatus
from app.models import DatabaseManager

api_bp = Blueprint('api', __name__)
detector = EnhancedModelDetector()
db = DatabaseManager()


def run_batch_test(task_id: str, api_url: str, api_key: str, models: list, num_tests: int):
    """在后台线程中运行批量测试"""
    try:
        task_manager.start_task(task_id, '开始执行检测...')
        
        # 定义进度回调
        def progress_callback(progress: float, message: str):
            task_manager.update_progress(task_id, progress, message)
        
        # 执行批量测试
        result = detector.batch_test(
            api_url=api_url,
            api_key=api_key,
            models=models,
            num_tests=num_tests,
            auto_strategy=True,
            progress_callback=progress_callback
        )
        
        # 保存到数据库
        db.save_batch_test(task_id, api_url, result)
        for test_result in result.get('all_results', []):
            db.save_test_record(task_id, test_result)
        
        task_manager.complete_task(task_id, result, '检测完成！')
        
    except Exception as e:
        task_manager.fail_task(task_id, str(e), '检测失败')


@api_bp.route('/detect/single', methods=['POST'])
def detect_single_model():
    """检测单个模型"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        api_url = data.get('api_url')
        api_key = data.get('api_key')
        model = data.get('model')
        test_prompt = data.get('test_prompt')
        strategy = data.get('strategy', 'full')
        
        if not api_url or not api_key or not model:
            return jsonify({'error': 'Missing api_url, api_key or model'}), 400
        
        # 执行检测
        result = detector.detect_model(api_url, api_key, model, test_prompt, strategy)
        result_dict = asdict(result)
        
        # 保存到数据库
        test_id = str(uuid.uuid4())
        db.save_test_record(test_id, result_dict)
        
        return jsonify({
            'test_id': test_id,
            'result': result_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/detect/batch/start', methods=['POST'])
def start_batch_test():
    """启动批量测试（后台异步执行）"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        api_url = data.get('api_url')
        api_key = data.get('api_key')
        models = data.get('models')
        num_tests = data.get('num_tests', 3)
        
        if not api_url or not api_key:
            return jsonify({'error': 'Missing api_url or api_key'}), 400
        
        if not models or len(models) == 0:
            return jsonify({'error': 'No models selected'}), 400
        
        # 创建任务
        task_id = task_manager.create_task()
        
        # 在后台线程中运行
        thread = threading.Thread(
            target=run_batch_test,
            args=(task_id, api_url, api_key, models, num_tests)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'message': 'Batch test started'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/detect/batch/progress/<task_id>', methods=['GET'])
def get_batch_progress(task_id):
    """获取批量测试进度"""
    try:
        progress = task_manager.get_progress(task_id)
        
        if not progress:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(progress.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/detect/batch', methods=['POST'])
def detect_batch_sync():
    """同步批量检测（保留用于兼容）"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        api_url = data.get('api_url')
        api_key = data.get('api_key')
        models = data.get('models')
        num_tests = data.get('num_tests', 3)
        
        if not api_url or not api_key:
            return jsonify({'error': 'Missing api_url or api_key'}), 400
        
        # 执行批量检测
        batch_result = detector.batch_test(api_url, api_key, models, num_tests)
        
        # 保存到数据库
        batch_id = str(uuid.uuid4())
        db.save_batch_test(batch_id, api_url, batch_result)
        
        for result in batch_result.get('all_results', []):
            db.save_test_record(batch_id, result)
        
        return jsonify({
            'batch_id': batch_id,
            'result': batch_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/models/fetch', methods=['POST'])
def fetch_available_models():
    """获取API端点可用的模型列表"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Missing request data'}), 400
        
        api_url = data.get('api_url')
        api_key = data.get('api_key')
        
        if not api_url or not api_key:
            return jsonify({'error': 'Missing api_url or api_key'}), 400
        
        models = detector.fetch_available_models(api_url, api_key)
        
        return jsonify({
            'models': models,
            'total': len(models)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/tests', methods=['GET'])
def get_test_history():
    """获取测试历史记录"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        history = db.get_test_history(limit, offset)
        return jsonify({
            'history': history,
            'total': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/batches', methods=['GET'])
def get_batch_history():
    """获取批量测试历史记录"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        history = db.get_batch_test_history(limit, offset)
        return jsonify({
            'history': history,
            'total': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/test/<test_id>', methods=['GET'])
def get_test_by_id(test_id):
    """根据ID获取单个测试记录"""
    try:
        record = db.get_test_by_id(test_id)
        if not record:
            return jsonify({'error': 'Test not found'}), 404
        
        return jsonify({'record': record}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/batch/<batch_id>', methods=['GET'])
def get_batch_by_id(batch_id):
    """根据ID获取批量测试记录"""
    try:
        batch = db.get_batch_test_by_id(batch_id)
        if not batch:
            return jsonify({'error': 'Batch test not found'}), 404
        
        tests = db.get_tests_by_batch_id(batch_id)
        return jsonify({
            'batch': batch,
            'tests': tests
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    try:
        stats = db.get_statistics()
        return jsonify({'statistics': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/clear', methods=['DELETE'])
def clear_history():
    """清空历史记录"""
    try:
        count = db.clear_history()
        return jsonify({
            'message': f'Cleared {count} records',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/models', methods=['GET'])
def get_popular_models():
    """获取流行模型列表"""
    try:
        return jsonify({
            'models': detector.popular_models
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy'}), 200
