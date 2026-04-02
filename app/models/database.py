import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from contextlib import contextmanager


class DatabaseManager:
    """数据库管理器 - 使用SQLite存储测试历史"""
    
    def __init__(self, db_path: str = 'test_history.db'):
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_database(self):
        """初始化数据库表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建测试记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id TEXT NOT NULL,
                    api_url TEXT NOT NULL,
                    model_tested TEXT NOT NULL,
                    supplier TEXT,
                    detected_model TEXT,
                    confidence REAL,
                    response_time REAL,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    total_tokens INTEGER,
                    is_model_match BOOLEAN,
                    is_token_consistent BOOLEAN,
                    response_status INTEGER,
                    error TEXT,
                    analysis TEXT,
                    timestamp TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 创建批量测试记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS batch_tests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    api_url TEXT NOT NULL,
                    num_models_tested INTEGER,
                    total_tests INTEGER,
                    successful_tests INTEGER,
                    failed_tests INTEGER,
                    overall_stats TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_id ON test_records(test_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_batch_id ON batch_tests(batch_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_timestamp ON test_records(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_batch_created ON batch_tests(created_at)')
    
    def save_test_record(self, test_id: str, result: Dict[str, Any]) -> int:
        """保存单个测试记录
        
        Args:
            test_id: 测试ID
            result: 测试结果字典
            
        Returns:
            记录ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO test_records (
                    test_id, api_url, model_tested, supplier, detected_model,
                    confidence, response_time, prompt_tokens, completion_tokens,
                    total_tokens, is_model_match, is_token_consistent,
                    response_status, error, analysis, timestamp, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                test_id,
                result.get('analysis', {}).get('endpoint', ''),
                result.get('model_tested', ''),
                result.get('supplier', ''),
                result.get('model', ''),
                result.get('confidence', 0.0),
                result.get('response_time', 0.0),
                result.get('prompt_tokens', 0),
                result.get('completion_tokens', 0),
                result.get('total_tokens', 0),
                1 if result.get('is_model_match', False) else 0,
                1 if result.get('is_token_consistent', False) else 0,
                result.get('response_status'),
                result.get('error'),
                json.dumps(result.get('analysis', {})),
                result.get('timestamp', datetime.now().isoformat()),
                datetime.now().isoformat()
            ))
            
            return cursor.lastrowid
    
    def save_batch_test(self, batch_id: str, api_url: str, batch_result: Dict[str, Any]) -> int:
        """保存批量测试结果
        
        Args:
            batch_id: 批量测试ID
            api_url: API URL
            batch_result: 批量测试结果
            
        Returns:
            批量测试记录ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            test_summary = batch_result.get('test_summary', {})
            
            cursor.execute('''
                INSERT INTO batch_tests (
                    batch_id, api_url, num_models_tested, total_tests,
                    successful_tests, failed_tests, overall_stats, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                batch_id,
                api_url,
                test_summary.get('total_models_tested', 0),
                test_summary.get('total_tests', 0),
                test_summary.get('successful_tests', 0),
                test_summary.get('failed_tests', 0),
                json.dumps(batch_result.get('overall_stats', {})),
                datetime.now().isoformat()
            ))
            
            return cursor.lastrowid
    
    def get_test_history(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取测试历史记录
        
        Args:
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            测试历史记录列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM test_records 
                ORDER BY timestamp DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_batch_test_history(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """获取批量测试历史记录
        
        Args:
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            批量测试历史记录列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM batch_tests 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                result = self._row_to_dict(row)
                if result.get('overall_stats'):
                    result['overall_stats'] = json.loads(result['overall_stats'])
                results.append(result)
            
            return results
    
    def get_test_by_id(self, test_id: str) -> Optional[Dict[str, Any]]:
        """根据测试ID获取单个测试记录
        
        Args:
            test_id: 测试ID
            
        Returns:
            测试记录，不存在则返回None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM test_records WHERE test_id = ?', (test_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row)
            
            return None
    
    def get_batch_test_by_id(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """根据批量测试ID获取批量测试记录
        
        Args:
            batch_id: 批量测试ID
            
        Returns:
            批量测试记录，不存在则返回None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM batch_tests WHERE batch_id = ?', (batch_id,))
            row = cursor.fetchone()
            
            if row:
                result = self._row_to_dict(row)
                if result.get('overall_stats'):
                    result['overall_stats'] = json.loads(result['overall_stats'])
                return result
            
            return None
    
    def get_tests_by_batch_id(self, batch_id: str) -> List[Dict[str, Any]]:
        """获取批量测试下的所有单个测试记录
        
        Args:
            batch_id: 批量测试ID
            
        Returns:
            单个测试记录列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM test_records 
                WHERE test_id = ? 
                ORDER BY model_tested
            ''', (batch_id,))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据
        
        Returns:
            统计数据字典
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 总测试次数
            cursor.execute('SELECT COUNT(*) FROM test_records')
            total_tests = cursor.fetchone()[0]
            
            # 成功测试次数
            cursor.execute('SELECT COUNT(*) FROM test_records WHERE error IS NULL')
            successful_tests = cursor.fetchone()[0]
            
            # 模型匹配次数
            cursor.execute('SELECT COUNT(*) FROM test_records WHERE is_model_match = 1')
            model_match_tests = cursor.fetchone()[0]
            
            # Token一致次数
            cursor.execute('SELECT COUNT(*) FROM test_records WHERE is_token_consistent = 1')
            token_consistent_tests = cursor.fetchone()[0]
            
            # 供应商分布
            cursor.execute('''
                SELECT supplier, COUNT(*) as count 
                FROM test_records 
                WHERE supplier IS NOT NULL AND supplier != ''
                GROUP BY supplier 
                ORDER BY count DESC
            ''')
            supplier_distribution = {row['supplier']: row['count'] for row in cursor.fetchall()}
            
            # 模型分布
            cursor.execute('''
                SELECT detected_model, COUNT(*) as count 
                FROM test_records 
                WHERE detected_model IS NOT NULL AND detected_model != '' AND detected_model != 'unknown'
                GROUP BY detected_model 
                ORDER BY count DESC
                LIMIT 10
            ''')
            model_distribution = {row['detected_model']: row['count'] for row in cursor.fetchall()}
            
            # 平均响应时间
            cursor.execute('SELECT AVG(response_time) FROM test_records WHERE response_time IS NOT NULL')
            avg_response_time = cursor.fetchone()[0] or 0
            
            # 平均置信度
            cursor.execute('SELECT AVG(confidence) FROM test_records WHERE confidence IS NOT NULL')
            avg_confidence = cursor.fetchone()[0] or 0
            
            return {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': total_tests - successful_tests,
                'model_match_rate': round(model_match_tests / total_tests, 2) if total_tests > 0 else 0,
                'token_consistent_rate': round(token_consistent_tests / total_tests, 2) if total_tests > 0 else 0,
                'supplier_distribution': supplier_distribution,
                'model_distribution': model_distribution,
                'avg_response_time': round(avg_response_time, 3),
                'avg_confidence': round(avg_confidence, 3)
            }
    
    def clear_history(self) -> int:
        """清空历史记录
        
        Returns:
            删除的记录数
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM test_records')
            test_count = cursor.rowcount
            
            cursor.execute('DELETE FROM batch_tests')
            batch_count = cursor.rowcount
            
            return test_count + batch_count
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """将SQLite行转换为字典"""
        result = dict(row)
        
        # 转换布尔值
        if 'is_model_match' in result:
            result['is_model_match'] = bool(result['is_model_match'])
        if 'is_token_consistent' in result:
            result['is_token_consistent'] = bool(result['is_token_consistent'])
        
        # 解析JSON
        if 'analysis' in result and result['analysis']:
            try:
                result['analysis'] = json.loads(result['analysis'])
            except json.JSONDecodeError:
                pass
        
        return result
