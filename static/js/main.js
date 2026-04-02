let popularModels = [];
let selectedModels = new Set();
let fetchedModels = [];
let currentTaskId = null;
let pollingInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initApiKeyToggles();
    initFetchModelsButton();
    initSingleFetchModelsButton();
    loadPopularModels();
    initBatchTestForm();
    initSingleTestForm();
    initHistoryPanel();
    initStatisticsPanel();
    initModal();
});

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.tab-panel');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabName = item.dataset.tab;
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            panels.forEach(panel => panel.classList.remove('active'));
            document.getElementById(`${tabName}-panel`).classList.add('active');
            
            if (tabName === 'history') {
                loadTestsHistory();
                loadBatchesHistory();
            } else if (tabName === 'statistics') {
                loadStatistics();
            }
        });
    });
}

function initApiKeyToggles() {
    const toggleSingleKey = document.getElementById('toggleSingleKey');
    const singleApiKey = document.getElementById('singleApiKey');
    
    if (toggleSingleKey && singleApiKey) {
        toggleSingleKey.addEventListener('click', () => {
            if (singleApiKey.type === 'password') {
                singleApiKey.type = 'text';
                toggleSingleKey.textContent = '🙈';
            } else {
                singleApiKey.type = 'password';
                toggleSingleKey.textContent = '👁️';
            }
        });
    }
    
    const toggleBatchKey = document.getElementById('toggleBatchKey');
    const batchApiKey = document.getElementById('batchApiKey');
    
    if (toggleBatchKey && batchApiKey) {
        toggleBatchKey.addEventListener('click', () => {
            if (batchApiKey.type === 'password') {
                batchApiKey.type = 'text';
                toggleBatchKey.textContent = '🙈';
            } else {
                batchApiKey.type = 'password';
                toggleBatchKey.textContent = '👁️';
            }
        });
    }
}

function initFetchModelsButton() {
    const fetchBtn = document.getElementById('fetchModelsBtn');
    if (!fetchBtn) return;
    
    fetchBtn.addEventListener('click', async () => {
        const apiUrl = document.getElementById('batchApiUrl').value;
        const apiKey = document.getElementById('batchApiKey').value;
        
        if (!apiUrl || !apiKey) {
            alert('请先输入API URL和API Key');
            return;
        }
        
        const btnText = fetchBtn.querySelector('.btn-text');
        const btnLoading = fetchBtn.querySelector('.btn-loading');
        
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
        fetchBtn.disabled = true;
        
        try {
            const response = await fetch('/api/models/fetch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_url: apiUrl, api_key: apiKey })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.models.length === 0) {
                alert('未获取到模型列表');
                return;
            }
            
            fetchedModels = data.models;
            populateModelList(fetchedModels);
            
            document.getElementById('modelSelectionGroup').style.display = 'block';
            document.getElementById('testConfigGroup').style.display = 'block';
            document.getElementById('startTestGroup').style.display = 'flex';
            
            alert(`成功获取 ${data.models.length} 个模型`);
            
        } catch (error) {
            alert('获取模型失败: ' + error.message);
        } finally {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            fetchBtn.disabled = false;
        }
    });
    
    const resetBtn = document.getElementById('resetFormBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetBatchForm);
    }
}

function initSingleFetchModelsButton() {
    const fetchBtn = document.getElementById('singleFetchModelsBtn');
    if (!fetchBtn) return;
    
    fetchBtn.addEventListener('click', async () => {
        const apiUrl = document.getElementById('singleApiUrl').value;
        const apiKey = document.getElementById('singleApiKey').value;
        
        if (!apiUrl || !apiKey) {
            alert('请先输入API URL和API Key');
            return;
        }
        
        const btnText = fetchBtn.querySelector('.btn-text');
        const btnLoading = fetchBtn.querySelector('.btn-loading');
        
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
        fetchBtn.disabled = true;
        
        try {
            const response = await fetch('/api/models/fetch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_url: apiUrl, api_key: apiKey })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.models.length === 0) {
                alert('未获取到模型列表');
                return;
            }
            
            populateSingleModelSelect(data.models);
            alert(`成功获取 ${data.models.length} 个模型`);
            
        } catch (error) {
            alert('获取模型失败: ' + error.message);
        } finally {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            fetchBtn.disabled = false;
        }
    });
}

function populateSingleModelSelect(models) {
    const select = document.getElementById('singleModel');
    if (!select) return;
    
    select.innerHTML = '<option value="">选择模型...</option>';
    
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = model.id;
        option.textContent = model.name + (model.owned_by ? ` (${model.owned_by})` : '');
        select.appendChild(option);
    });
}

function initSingleTestForm() {
    const form = document.getElementById('singleTestForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const apiUrl = document.getElementById('singleApiUrl').value;
        const apiKey = document.getElementById('singleApiKey').value;
        const model = document.getElementById('singleModel').value || document.getElementById('singleModelCustom').value;
        const testPrompt = document.getElementById('singlePrompt').value;
        
        if (!apiUrl || !apiKey || !model) {
            alert('请填写必填项');
            return;
        }
        
        const btn = document.getElementById('singleTestBtn');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');
        
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
        btn.disabled = true;
        
        try {
            const response = await fetch('/api/detect/single', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    api_url: apiUrl,
                    api_key: apiKey,
                    model: model,
                    test_prompt: testPrompt,
                    strategy: 'full'
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            document.getElementById('singleTestId').textContent = `测试ID: ${data.test_id}`;
            displaySingleTestResult(data.result);
            
        } catch (error) {
            alert('测试失败: ' + error.message);
        } finally {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            btn.disabled = false;
        }
    });
}

function displaySingleTestResult(result) {
    const content = document.getElementById('singleResultContent');
    const card = document.getElementById('singleResultCard');
    if (!content || !card) return;
    
    const riskClass = result.is_model_match ? 'success' : 'danger';
    const riskText = result.is_model_match ? '✓ 模型匹配' : '✗ 模型不匹配';
    
    content.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <span class="info-label">请求模型</span>
                <span class="info-value">${escapeHtml(result.model_tested)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">检测模型</span>
                <span class="info-value">${escapeHtml(result.model)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">供应商</span>
                <span class="info-value">${escapeHtml(result.supplier)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">置信度</span>
                <span class="info-value">${(result.confidence * 100).toFixed(1)}%</span>
            </div>
            <div class="info-item">
                <span class="info-label">响应时间</span>
                <span class="info-value">${result.response_time.toFixed(2)}s</span>
            </div>
        </div>
        
        <!-- Token使用详情（突出显示） -->
        <div style="margin-top: 1.5rem; padding: 1.25rem; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: var(--radius);">
            <h4 style="margin: 0 0 1rem 0; color: #1e40af; font-size: 1rem;">💰 Token使用（请与平台账单核对）</h4>
            <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 120px;">
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.25rem;">提示词Token</div>
                    <div style="font-family: monospace; font-size: 1.5rem; font-weight: 700; color: #1e40af;">${result.prompt_tokens}</div>
                </div>
                <div style="flex: 1; min-width: 120px;">
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.25rem;">完成Token</div>
                    <div style="font-family: monospace; font-size: 1.5rem; font-weight: 700; color: #1e40af;">${result.completion_tokens}</div>
                </div>
                <div style="flex: 1; min-width: 120px;">
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.25rem;">总计Token</div>
                    <div style="font-family: monospace; font-size: 1.5rem; font-weight: 700; color: #1e3a8a;">${result.total_tokens}</div>
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
            <span class="badge badge-${riskClass}" style="font-size: 1rem; padding: 0.75rem 1.5rem;">${riskText}</span>
        </div>
        ${result.error ? `
            <div style="margin-top: 1.5rem; padding: 1rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: var(--radius); color: #991b1b;">
                <strong>错误:</strong> ${escapeHtml(result.error)}
            </div>
        ` : ''}
        ${result.analysis?.response_content ? `
            <div style="margin-top: 1.5rem;">
                <div class="info-label" style="margin-bottom: 0.5rem;">响应内容</div>
                <div style="background: var(--bg-color); padding: 1rem; border-radius: var(--radius); font-size: 0.9rem; white-space: pre-wrap;">
                    ${escapeHtml(result.analysis.response_content)}
                </div>
            </div>
        ` : ''}
    `;
    
    card.style.display = 'block';
}

function populateModelList(models) {
    const list = document.getElementById('modelList');
    if (!list) return;
    
    list.innerHTML = '';
    selectedModels.clear();
    
    models.forEach(model => {
        const item = document.createElement('div');
        item.className = 'model-item';
        item.innerHTML = `
            <input type="checkbox" id="model-${model.id}" value="${model.id}">
            <label for="model-${model.id}">
                ${model.name}
                ${model.owned_by ? `<span style="color: var(--text-secondary); font-size: 0.85rem;">(${model.owned_by})</span>` : ''}
            </label>
        `;
        
        const checkbox = item.querySelector('input');
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                selectedModels.add(model.id);
                item.classList.add('selected');
            } else {
                selectedModels.delete(model.id);
                item.classList.remove('selected');
            }
        });
        
        item.addEventListener('click', (e) => {
            if (e.target.tagName !== 'INPUT') {
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change'));
            }
        });
        
        list.appendChild(item);
    });
    
    const selectAllBtn = document.getElementById('selectAllModels');
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', () => {
            document.querySelectorAll('#modelList .model-item input').forEach(cb => {
                cb.checked = true;
                cb.dispatchEvent(new Event('change'));
            });
        });
    }
    
    const clearAllBtn = document.getElementById('clearAllModels');
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            document.querySelectorAll('#modelList .model-item input').forEach(cb => {
                cb.checked = false;
                cb.dispatchEvent(new Event('change'));
            });
        });
    }
}

function resetBatchForm() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    
    document.getElementById('modelSelectionGroup').style.display = 'none';
    document.getElementById('testConfigGroup').style.display = 'none';
    document.getElementById('startTestGroup').style.display = 'none';
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('batchResultCard').style.display = 'none';
    
    document.getElementById('modelList').innerHTML = '';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressText').textContent = '准备中...';
    document.getElementById('progressPercent').textContent = '0%';
    document.getElementById('progressLog').innerHTML = '';
    
    // 重置按钮状态
    const startBtn = document.getElementById('startTestBtn');
    if (startBtn) {
        const btnText = startBtn.querySelector('.btn-text');
        const btnLoading = startBtn.querySelector('.btn-loading');
        if (btnText) btnText.style.display = 'inline';
        if (btnLoading) btnLoading.style.display = 'none';
        startBtn.disabled = false;
    }
    
    // 重置获取模型按钮
    const fetchBtn = document.getElementById('fetchModelsBtn');
    if (fetchBtn) {
        const btnText = fetchBtn.querySelector('.btn-text');
        const btnLoading = fetchBtn.querySelector('.btn-loading');
        if (btnText) btnText.style.display = 'inline';
        if (btnLoading) btnLoading.style.display = 'none';
        fetchBtn.disabled = false;
    }
    
    selectedModels.clear();
    fetchedModels = [];
    currentTaskId = null;
}

function initBatchTestForm() {
    const startBtn = document.getElementById('startTestBtn');
    if (!startBtn) return;
    
    startBtn.addEventListener('click', async () => {
        const apiUrl = document.getElementById('batchApiUrl').value;
        const apiKey = document.getElementById('batchApiKey').value;
        const numTests = parseInt(document.getElementById('numTests').value);
        const models = Array.from(selectedModels);
        
        if (models.length === 0) {
            alert('请至少选择一个模型');
            return;
        }
        
        const btnText = startBtn.querySelector('.btn-text');
        const btnLoading = startBtn.querySelector('.btn-loading');
        
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
        startBtn.disabled = true;
        
        document.getElementById('progressSection').style.display = 'block';
        document.getElementById('progressBar').style.width = '0%';
        document.getElementById('progressText').textContent = '启动检测...';
        document.getElementById('progressPercent').textContent = '0%';
        document.getElementById('progressLog').innerHTML = '';
        
        try {
            const response = await fetch('/api/detect/batch/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    api_url: apiUrl,
                    api_key: apiKey,
                    models: models,
                    num_tests: numTests
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            currentTaskId = data.task_id;
            startPolling(currentTaskId);
            
        } catch (error) {
            alert('启动检测失败: ' + error.message);
            
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            startBtn.disabled = false;
        }
    });
}

function startPolling(taskId) {
    pollingInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/detect/batch/progress/${taskId}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            updateProgressDisplay(data);
            
            if (data.status === 'completed' || data.status === 'failed') {
                clearInterval(pollingInterval);
                pollingInterval = null;
                
                const startBtn = document.getElementById('startTestBtn');
                if (startBtn) {
                    const btnText = startBtn.querySelector('.btn-text');
                    const btnLoading = startBtn.querySelector('.btn-loading');
                    btnText.style.display = 'inline';
                    btnLoading.style.display = 'none';
                    startBtn.disabled = false;
                }
                
                if (data.status === 'completed' && data.result) {
                    displayBatchResult({ batch_id: taskId, result: data.result });
                } else if (data.status === 'failed') {
                    alert('检测失败: ' + (data.error || '未知错误'));
                }
            }
            
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 500);
}

function updateProgressDisplay(data) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const progressPercent = document.getElementById('progressPercent');
    const progressLog = document.getElementById('progressLog');
    
    const percent = Math.round(data.progress * 100);
    progressBar.style.width = `${percent}%`;
    progressText.textContent = data.message || '处理中...';
    progressPercent.textContent = `${percent}%`;
    
    if (data.logs && data.logs.length > 0) {
        progressLog.innerHTML = data.logs.map(log => `<div>${escapeHtml(log)}</div>`).join('');
        progressLog.scrollTop = progressLog.scrollHeight;
    }
}

async function loadPopularModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        popularModels = data.models || [];
    } catch (error) {
        console.error('Failed to load models:', error);
    }
}

function displayBatchResult(data) {
    const card = document.getElementById('batchResultCard');
    const content = document.getElementById('batchResultContent');
    const testId = document.getElementById('batchTestId');
    
    if (!card || !content || !testId) return;
    
    testId.textContent = `ID: ${data.batch_id}`;
    
    const result = data.result;
    const summary = result.test_summary;
    const overall = result.overall_stats;
    const modelStats = result.model_stats || {};
    
    // 统计数据
    let lowRisk = 0, mediumRisk = 0, highRisk = 0, criticalRisk = 0, failed = 0;
    const allModelResults = [];
    
    Object.entries(modelStats).forEach(([model, stats]) => {
        if (stats.status === 'all_failed') {
            failed++;
            allModelResults.push({
                model: model,
                risk: 'failed',
                match_rate: 0,
                detected: '全部失败',
                response_time: 0,
                description: 'API调用失败'
            });
        } else {
            const matchRate = stats.model_match_rate;
            let risk = 'low';
            let description = '正常';
            
            if (matchRate === 0) {
                risk = 'critical';
                description = '模型被完全偷换！';
            } else if (matchRate < 0.5) {
                risk = 'high';
                description = '模型匹配率低，可能被降级';
            } else if (matchRate < 0.8) {
                risk = 'medium';
                description = '模型匹配率一般，需关注';
            } else if (stats.avg_response_time < 0.5 || stats.avg_response_time > 10) {
                risk = 'medium';
                description = '响应时间异常';
            }
            
            if (risk === 'low') lowRisk++;
            else if (risk === 'medium') mediumRisk++;
            else if (risk === 'high') highRisk++;
            else if (risk === 'critical') criticalRisk++;
            
            allModelResults.push({
                model: model,
                risk: risk,
                match_rate: matchRate,
                detected: stats.detected_model || stats.detected_supplier || '未知',
                response_time: stats.avg_response_time,
                prompt_tokens: stats.avg_prompt_tokens || 0,
                completion_tokens: stats.avg_completion_tokens || 0,
                total_tokens: stats.avg_total_tokens || 0,
                description: description
            });
        }
    });
    
    // 找出严重风险的模型
    const criticalModels = allModelResults.filter(m => m.risk === 'critical');
    const highModels = allModelResults.filter(m => m.risk === 'high');
    
    content.innerHTML = `
        <!-- 风险概览卡片 -->
        <div style="background: var(--bg-color); padding: 1.25rem; border-radius: var(--radius); border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; font-size: 1.1rem;">📊 风险概览</h3>
            </div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: #dcfce7; color: #166534; border-radius: 9999px; font-weight: 500;">
                    🟢 ${lowRisk} 正常
                </span>
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: #fef9c3; color: #854d0e; border-radius: 9999px; font-weight: 500;">
                    🟡 ${mediumRisk} 需关注
                </span>
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: #fecaca; color: #991b1b; border-radius: 9999px; font-weight: 500;">
                    🔴 ${highRisk} 高风险
                </span>
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: #fee2e2; color: #7f1d1d; border-radius: 9999px; font-weight: 500;">
                    💀 ${criticalRisk} 严重
                </span>
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: #f3f4f6; color: #374151; border-radius: 9999px; font-weight: 500;">
                    ❓ ${failed} 失败
                </span>
            </div>
        </div>
        
        <!-- 严重风险高亮区 -->
        ${criticalModels.length > 0 ? `
            <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 1.25rem; border-radius: var(--radius); margin-bottom: 1.5rem;">
                <h3 style="margin: 0 0 1rem 0; color: #991b1b; font-size: 1.1rem;">💀 严重问题 TOP ${Math.min(criticalModels.length, 5)}</h3>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    ${criticalModels.slice(0, 5).map((m, idx) => `
                        <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: white; border-radius: var(--radius); border: 1px solid #fecaca;">
                            <span style="font-weight: 700; color: #991b1b; width: 24px;">${idx + 1}.</span>
                            <span style="flex: 1; font-weight: 500;">${escapeHtml(m.model)}</span>
                            <span style="color: #6b7280;">→</span>
                            <span style="font-family: monospace; background: #fef2f2; padding: 0.25rem 0.5rem; border-radius: 4px;">${escapeHtml(m.detected)}</span>
                            <span style="color: #991b1b; font-weight: 500;">⚠️ ${escapeHtml(m.description)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
        
        ${highModels.length > 0 ? `
            <div style="background: #fefce8; border: 1px solid #fef08a; padding: 1.25rem; border-radius: var(--radius); margin-bottom: 1.5rem;">
                <h3 style="margin: 0 0 1rem 0; color: #854d0e; font-size: 1.1rem;">🔴 高风险模型</h3>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    ${highModels.slice(0, 5).map(m => `
                        <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; background: white; border-radius: var(--radius); border: 1px solid #fef08a;">
                            <span style="flex: 1; font-weight: 500;">${escapeHtml(m.model)}</span>
                            <span style="color: #6b7280;">匹配率: ${(m.match_rate * 100).toFixed(0)}%</span>
                            <span style="font-family: monospace; background: #fefce8; padding: 0.25rem 0.5rem; border-radius: 4px;">${escapeHtml(m.detected)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
        
        <!-- Token使用概览 -->
        <div style="margin-top: 1.5rem; padding: 1.25rem; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: var(--radius);">
            <h4 style="margin: 0 0 1rem 0; color: #1e40af; font-size: 1rem;">💰 Token使用汇总（请与平台账单核对）</h4>
            <p style="margin: 0; color: #1e3a8a; font-size: 0.9rem;">
                各模型的详细Token使用请查看下方表格的"Token"列
            </p>
        </div>
        
        <!-- 详细检测结果表 -->
        <div style="border: 1px solid var(--border-color); border-radius: var(--radius); overflow: hidden;">
            <div style="background: var(--bg-color); padding: 1rem; border-bottom: 1px solid var(--border-color);">
                <h3 style="margin: 0; font-size: 1rem;">📋 详细检测结果</h3>
            </div>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: var(--bg-color);">
                            <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">模型</th>
                            <th style="text-align: center; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">风险</th>
                            <th style="text-align: center; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">匹配率</th>
                            <th style="text-align: left; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">检测模型</th>
                            <th style="text-align: center; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">响应</th>
                            <th style="text-align: center; padding: 0.75rem 1rem; font-weight: 500; border-bottom: 1px solid var(--border-color);">Token</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${allModelResults.map(m => `
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 0.75rem 1rem; font-family: monospace; font-size: 0.9rem;">${escapeHtml(m.model)}</td>
                                <td style="padding: 0.75rem 1rem; text-align: center;">
                                    ${m.risk === 'low' ? '<span style="display: inline-block; width: 20px; height: 20px; background: #22c55e; border-radius: 50%;"></span>' : 
                                      m.risk === 'medium' ? '<span style="display: inline-block; width: 20px; height: 20px; background: #eab308; border-radius: 50%;"></span>' :
                                      m.risk === 'high' ? '<span style="display: inline-block; width: 20px; height: 20px; background: #ef4444; border-radius: 50%;"></span>' :
                                      m.risk === 'critical' ? '<span style="display: inline-block; width: 20px; height: 20px; background: #7f1d1d; border-radius: 50%;"></span>' :
                                      '<span style="display: inline-block; width: 20px; height: 20px; background: #6b7280; border-radius: 50%;"></span>'}
                                </td>
                                <td style="padding: 0.75rem 1rem; text-align: center; font-weight: 500;">
                                    ${m.risk === 'failed' ? '-' : `${(m.match_rate * 100).toFixed(0)}%`}
                                </td>
                                <td style="padding: 0.75rem 1rem; font-family: monospace; font-size: 0.85rem; color: var(--text-secondary);">
                                    ${escapeHtml(m.detected)}
                                </td>
                                <td style="padding: 0.75rem 1rem; text-align: center;">
                                    ${m.risk === 'failed' ? '-' : `${m.response_time.toFixed(2)}s`}
                                </td>
                                <td style="padding: 0.75rem 1rem; text-align: center; font-family: monospace; font-size: 0.85rem;">
                                    ${m.risk === 'failed' ? '-' : `${m.prompt_tokens}+${m.completion_tokens}=${m.total_tokens}`}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 总体建议 -->
        <div style="margin-top: 1.5rem; background: #eff6ff; border: 1px solid #bfdbfe; padding: 1.25rem; border-radius: var(--radius);">
            <h3 style="margin: 0 0 0.75rem 0; color: #1e40af; font-size: 1rem;">📝 总体建议</h3>
            <ul style="margin: 0; padding-left: 1.25rem; color: #1e3a8a; line-height: 1.8;">
                ${criticalRisk > 0 ? `<li><strong>立即停用</strong> ${criticalRisk} 个严重风险模型（被完全偷换）</li>` : ''}
                ${highRisk > 0 ? `<li><strong>联系供应商</strong> 询问 ${highRisk} 个高风险模型的问题</li>` : ''}
                ${mediumRisk > 0 ? `<li><strong>多测试几次</strong> ${mediumRisk} 个需关注模型，确认是否有问题</li>` : ''}
                ${failed > 0 ? `<li><strong>检查Key权限</strong>，确认 ${failed} 个失败模型是否有权限访问</li>` : ''}
                ${criticalRisk + highRisk === 0 ? '<li>✅ 整体情况良好，大部分模型正常</li>' : ''}
            </ul>
        </div>
    `;
    
    card.style.display = 'block';
}

function initHistoryPanel() {
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadTestsHistory();
            loadBatchesHistory();
        });
    }
    
    const clearBtn = document.getElementById('clearHistory');
    if (clearBtn) {
        clearBtn.addEventListener('click', async () => {
            if (!confirm('确定要清空所有历史记录吗？')) return;
            
            try {
                const response = await fetch('/api/history/clear', { method: 'DELETE' });
                const data = await response.json();
                
                if (data.error) throw new Error(data.error);
                
                alert(`已清空 ${data.count} 条记录`);
                loadTestsHistory();
                loadBatchesHistory();
                
            } catch (error) {
                alert('清空失败: ' + error.message);
            }
        });
    }
    
    document.querySelectorAll('.history-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const historyType = tab.dataset.history;
            document.querySelectorAll('.history-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.querySelectorAll('.history-list').forEach(list => list.classList.remove('active'));
            document.getElementById(`${historyType}History`).classList.add('active');
        });
    });
    
    loadTestsHistory();
    loadBatchesHistory();
}

async function loadTestsHistory() {
    const container = document.getElementById('testsHistory');
    if (!container) return;
    
    try {
        const response = await fetch('/api/history/tests?limit=50');
        const data = await response.json();
        
        if (data.history.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">暂无测试记录</div>';
            return;
        }
        
        container.innerHTML = data.history.map(record => `
            <div class="history-item" onclick="showTestDetail('${record.test_id}')">
                <div class="history-item-header">
                    <div class="history-item-title">${escapeHtml(record.model_tested)}</div>
                    <div class="history-item-time">${formatTime(record.timestamp)}</div>
                </div>
                <div class="history-item-details">
                    <span class="badge ${record.is_model_match ? 'badge-success' : 'badge-danger'}">
                        模型: ${record.is_model_match ? '匹配' : '不匹配'}
                    </span>
                    <span class="badge ${record.is_token_consistent ? 'badge-success' : 'badge-warning'}">
                        Token: ${record.is_token_consistent ? '一致' : '异常'}
                    </span>
                    <span class="badge badge-info">${record.response_time.toFixed(2)}s</span>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = `<div style="color: var(--danger-color);">加载失败: ${escapeHtml(error.message)}</div>`;
    }
}

async function loadBatchesHistory() {
    const container = document.getElementById('batchesHistory');
    if (!container) return;
    
    try {
        const response = await fetch('/api/history/batches?limit=50');
        const data = await response.json();
        
        if (data.history.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">暂无批量测试记录</div>';
            return;
        }
        
        container.innerHTML = data.history.map(record => {
            const stats = record.overall_stats || {};
            return `
            <div class="history-item" onclick="showBatchDetail('${record.batch_id}')">
                <div class="history-item-header">
                    <div class="history-item-title">
                        批量测试 - ${record.num_models_tested}个模型
                    </div>
                    <div class="history-item-time">${formatTime(record.created_at)}</div>
                </div>
                <div class="history-item-details">
                    <span class="badge badge-info">${record.total_tests}次测试</span>
                    <span class="badge badge-success">${record.successful_tests}成功</span>
                    <span class="badge badge-danger">${record.failed_tests}失败</span>
                </div>
            </div>
        `;
        }).join('');
        
    } catch (error) {
        container.innerHTML = `<div style="color: var(--danger-color);">加载失败: ${escapeHtml(error.message)}</div>`;
    }
}

function initStatisticsPanel() {
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadStatistics);
    }
    loadStatistics();
}

async function loadStatistics() {
    const container = document.getElementById('statisticsContent');
    if (!container) return;
    
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        const stats = data.statistics;
        
        container.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">总测试次数</span>
                        <span class="stat-card-icon">📊</span>
                    </div>
                    <div class="stat-card-value">${stats.total_tests}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">成功测试</span>
                        <span class="stat-card-icon">✅</span>
                    </div>
                    <div class="stat-card-value">${stats.successful_tests}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">模型匹配率</span>
                        <span class="stat-card-icon">🎯</span>
                    </div>
                    <div class="stat-card-value">${(stats.model_match_rate * 100).toFixed(1)}%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">Token一致率</span>
                        <span class="stat-card-icon">💰</span>
                    </div>
                    <div class="stat-card-value">${(stats.token_consistent_rate * 100).toFixed(1)}%</div>
                </div>
            </div>
        `;
        
    } catch (error) {
        container.innerHTML = `<div style="color: var(--danger-color);">加载失败: ${escapeHtml(error.message)}</div>`;
    }
}

function initModal() {
    const modal = document.getElementById('detailModal');
    const closeBtn = document.getElementById('closeModal');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }
    
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    }
}

async function showTestDetail(testId) {
    const modal = document.getElementById('detailModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    if (!modal || !title || !body) return;
    
    title.textContent = '测试详情';
    body.innerHTML = '<div style="text-align: center; padding: 2rem;">加载中...</div>';
    modal.classList.add('active');
    
    try {
        const response = await fetch(`/api/history/test/${testId}`);
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        const record = data.record;
        body.innerHTML = `
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">测试ID</span>
                    <span class="info-value">${escapeHtml(record.test_id)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">测试时间</span>
                    <span class="info-value">${formatTime(record.timestamp)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">请求模型</span>
                    <span class="info-value">${escapeHtml(record.model_tested)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">检测模型</span>
                    <span class="info-value">${escapeHtml(record.detected_model)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">供应商</span>
                    <span class="info-value">${escapeHtml(record.supplier)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">模型匹配</span>
                    <span class="badge ${record.is_model_match ? 'badge-success' : 'badge-danger'}">
                        ${record.is_model_match ? '✓ 匹配' : '✗ 不匹配'}
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Token一致</span>
                    <span class="badge ${record.is_token_consistent ? 'badge-success' : 'badge-danger'}">
                        ${record.is_token_consistent ? '✓ 一致' : '✗ 异常'}
                    </span>
                </div>
            </div>
            ${record.analysis?.response_content ? `
                <div style="margin-top: 1.5rem;">
                    <div class="info-label" style="margin-bottom: 0.5rem;">响应内容</div>
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: var(--radius); font-size: 0.9rem; white-space: pre-wrap;">
                        ${escapeHtml(record.analysis.response_content)}
                    </div>
                </div>
            ` : ''}
            ${record.error ? `
                <div style="margin-top: 1.5rem;">
                    <div class="info-label" style="margin-bottom: 0.5rem;">错误信息</div>
                    <div style="background: #fee2e2; color: #991b1b; padding: 1rem; border-radius: var(--radius);">
                        ${escapeHtml(record.error)}
                    </div>
                </div>
            ` : ''}
        `;
        
    } catch (error) {
        body.innerHTML = `<div style="color: var(--danger-color);">加载失败: ${escapeHtml(error.message)}</div>`;
    }
}

async function showBatchDetail(batchId) {
    const modal = document.getElementById('detailModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    if (!modal || !title || !body) return;
    
    title.textContent = '批量测试详情';
    body.innerHTML = '<div style="text-align: center; padding: 2rem;">加载中...</div>';
    modal.classList.add('active');
    
    try {
        const response = await fetch(`/api/history/batch/${batchId}`);
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        const batch = data.batch;
        const tests = data.tests;
        
        body.innerHTML = `
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">批量测试ID</span>
                    <span class="info-value">${escapeHtml(batch.batch_id)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">测试时间</span>
                    <span class="info-value">${formatTime(batch.created_at)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">测试模型数</span>
                    <span class="info-value">${batch.num_models_tested}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">总测试次数</span>
                    <span class="info-value">${batch.total_tests}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">成功/失败</span>
                    <span>
                        <span class="badge badge-success">${batch.successful_tests}</span>
                        <span class="badge badge-danger">${batch.failed_tests}</span>
                    </span>
                </div>
            </div>
            <div style="margin-top: 1.5rem;">
                <h4 style="margin-bottom: 1rem;">测试详情列表</h4>
                <div style="max-height: 400px; overflow-y: auto;">
                    ${tests.map(test => `
                        <div style="padding: 0.75rem; border-bottom: 1px solid var(--border-color);">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                                <span style="font-weight: 500;">${escapeHtml(test.model_tested)}</span>
                                <span style="font-size: 0.85rem; color: var(--text-secondary);">${formatTime(test.timestamp)}</span>
                            </div>
                            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                ${test.error ? 
                                    `<span class="badge badge-danger">失败</span>` :
                                    `
                                    <span class="badge ${test.is_model_match ? 'badge-success' : 'badge-danger'}">模型: ${test.is_model_match ? '匹配' : '不匹配'}</span>
                                    <span class="badge ${test.is_token_consistent ? 'badge-success' : 'badge-warning'}">Token: ${test.is_token_consistent ? '一致' : '异常'}</span>
                                    <span class="badge badge-info">${test.response_time.toFixed(2)}s</span>
                                    <span class="badge badge-info">${test.detected_model || test.supplier}</span>
                                    `
                                }
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
    } catch (error) {
        body.innerHTML = `<div style="color: var(--danger-color);">加载失败: ${escapeHtml(error.message)}</div>`;
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTime(isoString) {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}
