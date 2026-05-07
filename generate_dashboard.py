import pandas as pd
import base64

# Read data
df = pd.read_excel('datasets/titanic.xls')
csv_data = df.to_csv(index=False)
encoded_csv = base64.b64encode(csv_data.encode('utf-8')).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Titanic Survival Dashboard</title>
<meta name="description" content="Interactive Analysis of the RMS Titanic Passenger Dataset">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
    --bg-color: #0b1120;
    --card-bg: rgba(30, 41, 59, 0.7);
    --card-border: rgba(255, 255, 255, 0.1);
    --primary: #0ea5e9;
    --primary-glow: rgba(14, 165, 233, 0.3);
    --accent: #f43f5e;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --success: #10b981;
    --warning: #f59e0b;
}}
body {{
    font-family: 'Outfit', sans-serif;
    background: radial-gradient(circle at top, #1e293b 0%, var(--bg-color) 100%);
    color: var(--text-main);
    min-height: 100vh;
    padding: 24px;
}}
.dashboard {{ max-width: 1440px; margin: 0 auto; }}
header {{ text-align: center; margin-bottom: 40px; position: relative; }}
header h1 {{
    font-size: 36px; font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px; letter-spacing: -0.5px;
}}
header p {{ color: var(--text-muted); font-size: 15px; font-weight: 300; }}
.glass-panel {{
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.glass-panel:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}}
.filters {{
    display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 32px;
    align-items: flex-end;
}}
.filter-group {{ display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 150px; }}
.filter-group label {{ font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }}
.filter-group select {{
    background: rgba(15, 23, 42, 0.8); border: 1px solid var(--card-border);
    color: var(--text-main); padding: 10px 14px; border-radius: 10px;
    font-size: 14px; font-family: inherit; outline: none; transition: border-color 0.2s, box-shadow 0.2s;
    cursor: pointer;
}}
.filter-group select:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-glow); }}
.btn-reset {{
    background: linear-gradient(135deg, #0ea5e9, #3b82f6);
    color: #fff; border: none; padding: 11px 24px; border-radius: 10px;
    font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.2s, transform 0.1s;
    font-family: inherit; height: fit-content;
}}
.btn-reset:hover {{ opacity: 0.9; transform: scale(1.02); }}
.btn-reset:active {{ transform: scale(0.98); }}

.kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 32px; }}
.kpi-card {{ position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: center; }}
.kpi-card::before {{
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
}}
.kpi-card:nth-child(1)::before {{ background: #38bdf8; }}
.kpi-card:nth-child(2)::before {{ background: #10b981; }}
.kpi-card:nth-child(3)::before {{ background: #f59e0b; }}
.kpi-card:nth-child(4)::before {{ background: #8b5cf6; }}

.kpi-title {{ font-size: 13px; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
.kpi-value {{ font-size: 36px; font-weight: 800; line-height: 1.1; margin-bottom: 4px; }}
.kpi-card:nth-child(1) .kpi-value {{ color: #38bdf8; }}
.kpi-card:nth-child(2) .kpi-value {{ color: #10b981; }}
.kpi-card:nth-child(3) .kpi-value {{ color: #f59e0b; }}
.kpi-card:nth-child(4) .kpi-value {{ color: #c4b5fd; }}
.kpi-subtext {{ font-size: 12px; color: rgba(248, 250, 252, 0.5); }}

.charts-row {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px; }}
.charts-row-equal {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
.chart-container {{ position: relative; height: 320px; width: 100%; }}
.chart-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
.chart-header h3 {{ font-size: 16px; font-weight: 600; color: var(--text-main); }}

.data-table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 10px; }}
.data-table th {{
    text-align: left; padding: 12px 16px; font-size: 12px; font-weight: 600;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;
    border-bottom: 1px solid var(--card-border); background: rgba(15, 23, 42, 0.4);
}}
.data-table th:first-child {{ border-top-left-radius: 8px; }}
.data-table th:last-child {{ border-top-right-radius: 8px; }}
.data-table td {{
    padding: 14px 16px; font-size: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: #e2e8f0;
}}
.data-table tr:last-child td {{ border-bottom: none; }}
.data-table tr:hover td {{ background: rgba(255, 255, 255, 0.03); }}
.badge {{ padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
.badge-survived {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
.badge-perished {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }}

footer {{ text-align: center; margin-top: 40px; padding: 20px 0; color: var(--text-muted); font-size: 13px; }}

@media (max-width: 1024px) {{ .charts-row, .charts-row-equal {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="dashboard">
    <header>
        <h1>Titanic Survival Dashboard</h1>
        <p>Interactive Analysis of RMS Titanic Passenger Demographics and Survival Rates</p>
    </header>

    <div class="glass-panel filters" id="filters">
        <div class="filter-group">
            <label>Passenger Class</label>
            <select id="classFilter" onchange="updateDashboard()">
                <option value="All">All Classes</option>
                <option value="1">1st Class</option>
                <option value="2">2nd Class</option>
                <option value="3">3rd Class</option>
            </select>
        </div>
        <div class="filter-group">
            <label>Gender</label>
            <select id="genderFilter" onchange="updateDashboard()">
                <option value="All">All Genders</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>
        </div>
        <div class="filter-group">
            <label>Embarked From</label>
            <select id="embarkedFilter" onchange="updateDashboard()">
                <option value="All">All Ports</option>
                <option value="S">Southampton (S)</option>
                <option value="C">Cherbourg (C)</option>
                <option value="Q">Queenstown (Q)</option>
            </select>
        </div>
        <button class="btn-reset" onclick="resetFilters()">Reset Filters</button>
    </div>

    <div class="kpi-grid">
        <div class="glass-panel kpi-card">
            <div class="kpi-title">Total Passengers</div>
            <div class="kpi-value" id="kpiTotal">0</div>
            <div class="kpi-subtext">in selected view</div>
        </div>
        <div class="glass-panel kpi-card">
            <div class="kpi-title">Overall Survival Rate</div>
            <div class="kpi-value" id="kpiSurvivalRate">0%</div>
            <div class="kpi-subtext" id="kpiSurvivalSub">0 survived</div>
        </div>
        <div class="glass-panel kpi-card">
            <div class="kpi-title">Average Age</div>
            <div class="kpi-value" id="kpiAvgAge">0</div>
            <div class="kpi-subtext">years old</div>
        </div>
        <div class="glass-panel kpi-card">
            <div class="kpi-title">Average Fare</div>
            <div class="kpi-value" id="kpiAvgFare">$0</div>
            <div class="kpi-subtext">per ticket</div>
        </div>
    </div>

    <div class="charts-row">
        <div class="glass-panel">
            <div class="chart-header">
                <h3>Survival by Age Group</h3>
            </div>
            <div class="chart-container"><canvas id="ageChart"></canvas></div>
        </div>
        <div class="glass-panel">
            <div class="chart-header">
                <h3>Gender Distribution</h3>
            </div>
            <div class="chart-container"><canvas id="genderChart"></canvas></div>
        </div>
    </div>

    <div class="charts-row-equal">
        <div class="glass-panel">
            <div class="chart-header">
                <h3>Survival by Passenger Class</h3>
            </div>
            <div class="chart-container"><canvas id="classChart"></canvas></div>
        </div>
        <div class="glass-panel">
            <div class="chart-header">
                <h3>Embarkation Port Analysis</h3>
            </div>
            <div class="chart-container"><canvas id="embarkChart"></canvas></div>
        </div>
    </div>

    <div class="glass-panel">
        <div class="chart-header">
            <h3>Recent Passengers (Sample)</h3>
        </div>
        <div style="overflow-x:auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Class</th>
                        <th>Gender</th>
                        <th>Age</th>
                        <th>Fare</th>
                        <th>Port</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <!-- Rows injected via JS -->
                </tbody>
            </table>
        </div>
    </div>

    <footer>
        Titanic Data Interactive Dashboard &copy; 2026 | Prepared for Data Analysis Report
    </footer>
</div>

<script>
// Base64 Encoded CSV Data
const RAW_CSV = atob("{encoded_csv}");

let fullData = [];
let charts = {{}};

// Parse CSV
function parseCSV(csvText) {{
    const lines = csvText.trim().split('\\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const result = [];
    
    for(let i = 1; i < lines.length; i++) {{
        // Basic CSV parsing handling quotes (naive approach for this dataset)
        const currentLine = lines[i];
        if(!currentLine) continue;
        
        let row = [];
        let insideQuote = false;
        let currentVal = '';
        
        for(let j = 0; j < currentLine.length; j++) {{
            const char = currentLine[j];
            if(char === '"') {{
                insideQuote = !insideQuote;
            }} else if(char === ',' && !insideQuote) {{
                row.push(currentVal);
                currentVal = '';
            }} else {{
                currentVal += char;
            }}
        }}
        row.push(currentVal);
        
        const obj = {{}};
        headers.forEach((header, index) => {{
            obj[header] = row[index] ? row[index].trim() : null;
        }});
        result.push(obj);
    }}
    return result;
}}

function initDashboard() {{
    fullData = parseCSV(RAW_CSV);
    
    // Set chart defaults
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.9)';
    Chart.defaults.plugins.tooltip.titleColor = '#f8fafc';
    Chart.defaults.plugins.tooltip.bodyColor = '#e2e8f0';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    
    updateDashboard();
}}

function resetFilters() {{
    document.getElementById('classFilter').value = 'All';
    document.getElementById('genderFilter').value = 'All';
    document.getElementById('embarkedFilter').value = 'All';
    updateDashboard();
}}

function updateDashboard() {{
    const pClass = document.getElementById('classFilter').value;
    const gender = document.getElementById('genderFilter').value;
    const embarked = document.getElementById('embarkedFilter').value;
    
    // Filter data
    const filteredData = fullData.filter(row => {{
        if(pClass !== 'All' && row.pclass !== pClass) return false;
        if(gender !== 'All' && row.sex !== gender) return false;
        if(embarked !== 'All' && row.embarked !== embarked) return false;
        return true;
    }});
    
    updateKPIs(filteredData);
    updateCharts(filteredData);
    updateTable(filteredData);
}}

function updateKPIs(data) {{
    const total = data.length;
    const survived = data.filter(d => d.survived === '1').length;
    const survivalRate = total > 0 ? ((survived / total) * 100).toFixed(1) : 0;
    
    let sumAge = 0, countAge = 0;
    let sumFare = 0, countFare = 0;
    
    data.forEach(d => {{
        if(d.age && !isNaN(parseFloat(d.age))) {{ sumAge += parseFloat(d.age); countAge++; }}
        if(d.fare && !isNaN(parseFloat(d.fare))) {{ sumFare += parseFloat(d.fare); countFare++; }}
    }});
    
    const avgAge = countAge > 0 ? (sumAge / countAge).toFixed(1) : 0;
    const avgFare = countFare > 0 ? (sumFare / countFare).toFixed(2) : 0;
    
    document.getElementById('kpiTotal').textContent = total.toLocaleString();
    document.getElementById('kpiSurvivalRate').textContent = survivalRate + '%';
    document.getElementById('kpiSurvivalSub').textContent = `${{survived.toLocaleString()}} survived`;
    document.getElementById('kpiAvgAge').textContent = avgAge;
    document.getElementById('kpiAvgFare').textContent = '$' + avgFare;
}}

function destroyChart(id) {{
    if(charts[id]) charts[id].destroy();
}}

function updateCharts(data) {{
    // 1. Age Chart (Bar) - Binning ages
    const ageBins = {{ '0-10': [0,0], '11-20': [0,0], '21-30': [0,0], '31-40': [0,0], '41-50': [0,0], '50+': [0,0] }};
    data.forEach(d => {{
        if(d.age && !isNaN(parseFloat(d.age))) {{
            const a = parseFloat(d.age);
            let bin = '50+';
            if(a <= 10) bin = '0-10';
            else if(a <= 20) bin = '11-20';
            else if(a <= 30) bin = '21-30';
            else if(a <= 40) bin = '31-40';
            else if(a <= 50) bin = '41-50';
            
            ageBins[bin][0]++; // total
            if(d.survived === '1') ageBins[bin][1]++; // survived
        }}
    }});
    
    const ageLabels = Object.keys(ageBins);
    const ageTotal = ageLabels.map(k => ageBins[k][0]);
    const ageSurvived = ageLabels.map(k => ageBins[k][1]);
    const ageNotSurvived = ageLabels.map(k => ageBins[k][0] - ageBins[k][1]);
    
    destroyChart('ageChart');
    charts['ageChart'] = new Chart(document.getElementById('ageChart').getContext('2d'), {{
        type: 'bar',
        data: {{
            labels: ageLabels,
            datasets: [
                {{ label: 'Survived', data: ageSurvived, backgroundColor: 'rgba(16, 185, 129, 0.8)', borderRadius: 4 }},
                {{ label: 'Perished', data: ageNotSurvived, backgroundColor: 'rgba(244, 63, 94, 0.8)', borderRadius: 4 }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            scales: {{
                x: {{ stacked: true, grid: {{ display: false }} }},
                y: {{ stacked: true, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}
            }},
            plugins: {{ legend: {{ position: 'top', labels: {{ usePointStyle: true }} }} }}
        }}
    }});
    
    // 2. Gender Chart (Doughnut)
    let maleS = 0, maleD = 0, femS = 0, femD = 0;
    data.forEach(d => {{
        if(d.sex === 'male') {{ if(d.survived === '1') maleS++; else maleD++; }}
        if(d.sex === 'female') {{ if(d.survived === '1') femS++; else femD++; }}
    }});
    
    destroyChart('genderChart');
    charts['genderChart'] = new Chart(document.getElementById('genderChart').getContext('2d'), {{
        type: 'doughnut',
        data: {{
            labels: ['Female Survived', 'Female Perished', 'Male Survived', 'Male Perished'],
            datasets: [{{
                data: [femS, femD, maleS, maleD],
                backgroundColor: ['#34d399', '#fb7185', '#38bdf8', '#818cf8'],
                borderWidth: 0, hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '65%',
            plugins: {{ legend: {{ position: 'right', labels: {{ usePointStyle: true }} }} }}
        }}
    }});
    
    // 3. Class Chart
    const clsBins = {{ '1st': [0,0], '2nd': [0,0], '3rd': [0,0] }};
    data.forEach(d => {{
        let c = d.pclass === '1' ? '1st' : (d.pclass === '2' ? '2nd' : '3rd');
        if(c) {{
            clsBins[c][0]++;
            if(d.survived === '1') clsBins[c][1]++;
        }}
    }});
    
    destroyChart('classChart');
    charts['classChart'] = new Chart(document.getElementById('classChart').getContext('2d'), {{
        type: 'bar',
        data: {{
            labels: Object.keys(clsBins),
            datasets: [
                {{ label: 'Survival Rate %', data: Object.keys(clsBins).map(k => clsBins[k][0] ? Math.round((clsBins[k][1]/clsBins[k][0])*100) : 0), backgroundColor: '#8b5cf6', borderRadius: 4 }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            scales: {{ y: {{ max: 100, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}, x: {{ grid: {{ display: false }} }} }},
            plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{ label: function(c) {{ return c.raw + '%'; }} }} }} }}
        }}
    }});
    
    // 4. Embark Chart
    const portMap = {{ 'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown' }};
    const embBins = {{}};
    data.forEach(d => {{
        if(d.embarked && portMap[d.embarked]) {{
            const p = portMap[d.embarked];
            embBins[p] = (embBins[p] || 0) + 1;
        }}
    }});
    
    destroyChart('embarkChart');
    charts['embarkChart'] = new Chart(document.getElementById('embarkChart').getContext('2d'), {{
        type: 'pie',
        data: {{
            labels: Object.keys(embBins),
            datasets: [{{
                data: Object.values(embBins),
                backgroundColor: ['#f59e0b', '#0ea5e9', '#ec4899'],
                borderWidth: 0, hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ position: 'right', labels: {{ usePointStyle: true }} }} }}
        }}
    }});
}}

function updateTable(data) {{
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    
    // show up to 10 rows
    const sample = data.slice(0, 10);
    sample.forEach(d => {{
        const tr = document.createElement('tr');
        
        const portMap = {{ 'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown' }};
        const port = portMap[d.embarked] || 'Unknown';
        const cls = d.pclass === '1' ? '1st' : (d.pclass === '2' ? '2nd' : '3rd');
        const badge = d.survived === '1' ? '<span class="badge badge-survived">Survived</span>' : '<span class="badge badge-perished">Perished</span>';
        const age = d.age && !isNaN(parseFloat(d.age)) ? Math.round(parseFloat(d.age)) : '-';
        const fare = d.fare && !isNaN(parseFloat(d.fare)) ? '$' + parseFloat(d.fare).toFixed(2) : '-';
        const name = d.name ? d.name.replace(/"/g, '') : 'Unknown';
        
        tr.innerHTML = `
            <td>${{name}}</td>
            <td>${{cls}}</td>
            <td style="text-transform: capitalize;">${{d.sex || '-'}}</td>
            <td>${{age}}</td>
            <td>${{fare}}</td>
            <td>${{port}}</td>
            <td>${{badge}}</td>
        `;
        tbody.appendChild(tr);
    }});
}}

// Initialize
window.onload = initDashboard;
</script>
</body>
</html>
"""

with open('Titanic_Interactive_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Dashboard created successfully!")
