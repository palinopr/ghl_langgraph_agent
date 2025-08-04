"""Simple UI for Agent Inbox - works with cloud deployment"""

def get_simple_html():
    """Get a simple HTML UI that works with relative API paths"""
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Inbox - Battery Consultation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f7fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .metric {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #2196f3;
        }
        .metric-label {
            color: #666;
            margin-top: 5px;
        }
        .conversations {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
        }
        .conversation-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .conversation-item:hover {
            background: #f8f9fa;
        }
        .customer-name {
            font-weight: 500;
            margin-bottom: 5px;
        }
        .conversation-meta {
            font-size: 0.9em;
            color: #666;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .error {
            color: #f44336;
            padding: 20px;
            text-align: center;
        }
        .refresh-btn {
            background: #2196f3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            float: right;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔋 Agent Inbox - Battery Consultation</h1>
        
        <button class="refresh-btn" onclick="loadData()">Refresh</button>
        
        <div class="metrics" id="metrics">
            <div class="loading">Loading metrics...</div>
        </div>
        
        <div class="conversations">
            <h2>Active Conversations</h2>
            <div id="conversationList">
                <div class="loading">Loading conversations...</div>
            </div>
        </div>
    </div>
    
    <script>
        // Use relative paths that work with deployment
        const API_BASE = window.location.pathname.replace(/\/inbox.*/, '') + '/inbox';
        
        async function loadData() {
            await loadMetrics();
            await loadConversations();
        }
        
        async function loadMetrics() {
            try {
                const response = await fetch(`${API_BASE}/metrics`);
                if (!response.ok) throw new Error('Failed to load metrics');
                
                const metrics = await response.json();
                
                document.getElementById('metrics').innerHTML = `
                    <div class="metric">
                        <div class="metric-value">${metrics.total_conversations || 0}</div>
                        <div class="metric-label">Total Conversations</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${metrics.completed_appointments || 0}</div>
                        <div class="metric-label">Appointments Booked</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${metrics.qualified_leads || 0}</div>
                        <div class="metric-label">Qualified Leads</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${(metrics.conversion_rate || 0).toFixed(1)}%</div>
                        <div class="metric-label">Conversion Rate</div>
                    </div>
                `;
            } catch (error) {
                document.getElementById('metrics').innerHTML = 
                    '<div class="error">Error loading metrics: ' + error.message + '</div>';
            }
        }
        
        async function loadConversations() {
            try {
                const response = await fetch(`${API_BASE}/conversations?limit=10`);
                if (!response.ok) throw new Error('Failed to load conversations');
                
                const conversations = await response.json();
                
                if (conversations.length === 0) {
                    document.getElementById('conversationList').innerHTML = 
                        '<div class="loading">No active conversations</div>';
                    return;
                }
                
                document.getElementById('conversationList').innerHTML = conversations.map(conv => `
                    <div class="conversation-item" onclick="alert('Contact ID: ${conv.contact_id}')">
                        <div class="customer-name">${conv.customer_name || 'Unknown Customer'}</div>
                        <div class="conversation-meta">
                            ${conv.housing_type || 'Type not specified'} • 
                            ${(conv.equipment_list || []).length} equipment items
                        </div>
                        <div class="conversation-meta">
                            Stage: ${conv.stage || 'unknown'} • 
                            Sentiment: ${conv.sentiment || 'neutral'}
                        </div>
                    </div>
                `).join('');
                
            } catch (error) {
                document.getElementById('conversationList').innerHTML = 
                    '<div class="error">Error loading conversations: ' + error.message + '</div>';
            }
        }
        
        // Auto refresh every 30 seconds
        setInterval(loadData, 30000);
        
        // Initial load
        loadData();
    </script>
</body>
</html>
"""