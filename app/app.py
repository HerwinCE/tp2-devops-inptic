from flask import Flask, Response, render_template_string, jsonify
import time
import os
import random
import platform
import psutil
from datetime import datetime

app = Flask(__name__)

request_count = 0
start_time = time.time()

# Template HTML moderne avec animations
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>INPTIC DevOps Platform - Gestion des Étudiants</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #00d4ff;
            --primary-dark: #0099cc;
            --secondary: #6c63ff;
            --dark: #0a0e17;
            --darker: #06090f;
            --light: #e0e0e0;
            --success: #00ff88;
            --warning: #ffaa00;
            --danger: #ff4757;
            --card-bg: rgba(20, 30, 45, 0.7);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: linear-gradient(135deg, var(--darker) 0%, #0f1525 100%);
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: var(--light);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* Animation des particules */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .particle {
            position: absolute;
            background: var(--primary);
            border-radius: 50%;
            opacity: 0.3;
            animation: float 15s infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0.2; }
            25% { transform: translateY(-30px) translateX(20px); opacity: 0.5; }
            75% { transform: translateY(30px) translateX(-20px); opacity: 0.3; }
        }

        /* Navigation */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(6, 9, 15, 0.95);
            backdrop-filter: blur(10px);
            z-index: 100;
            padding: 15px 30px;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .logo i {
            color: var(--primary);
            margin-right: 8px;
        }

        .nav-links {
            display: flex;
            gap: 25px;
            flex-wrap: wrap;
        }

        .nav-links a {
            color: var(--light);
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 500;
        }

        .nav-links a:hover {
            color: var(--primary);
        }

        /* Container principal */
        .container {
            max-width: 1400px;
            margin: 80px auto 40px;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Hero section */
        .hero {
            text-align: center;
            margin-bottom: 60px;
            animation: fadeInUp 0.8s ease;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 15px;
        }

        .hero p {
            color: #8892b0;
            font-size: 1.1rem;
        }

        .badge {
            display: inline-block;
            background: rgba(0, 212, 255, 0.15);
            border: 1px solid var(--primary);
            border-radius: 30px;
            padding: 5px 15px;
            font-size: 0.8rem;
            margin-top: 15px;
        }

        /* Cartes de métriques */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .metric-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(0, 212, 255, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.5s ease;
            animation-fill-mode: both;
        }

        .metric-card:nth-child(1) { animation-delay: 0.1s; }
        .metric-card:nth-child(2) { animation-delay: 0.2s; }
        .metric-card:nth-child(3) { animation-delay: 0.3s; }
        .metric-card:nth-child(4) { animation-delay: 0.4s; }

        .metric-card:hover {
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(0, 212, 255, 0.4);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .metric-header i {
            font-size: 2rem;
            color: var(--primary);
        }

        .metric-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #8892b0;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 10px 0;
        }

        .metric-unit {
            font-size: 0.8rem;
            color: #8892b0;
        }

        .trend {
            font-size: 0.8rem;
            margin-top: 10px;
        }

        .trend.up { color: var(--success); }
        .trend.down { color: var(--danger); }

        /* Section services */
        .services-section {
            background: rgba(15, 25, 40, 0.5);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 212, 255, 0.15);
        }

        .section-title {
            font-size: 1.5rem;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title i {
            color: var(--primary);
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .service-item {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s;
        }

        .service-item:hover {
            background: rgba(0, 212, 255, 0.1);
            transform: scale(1.05);
        }

        .service-item i {
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
        }

        .service-item .status {
            font-size: 0.7rem;
            color: var(--success);
        }

        /* Boutons d'action */
        .actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }

        .btn {
            padding: 14px 32px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            border: none;
            font-family: inherit;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: var(--darker);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
        }

        .btn-outline {
            background: transparent;
            border: 1px solid var(--primary);
            color: var(--primary);
        }

        .btn-outline:hover {
            background: rgba(0, 212, 255, 0.1);
            transform: translateY(-2px);
        }

        .btn-danger {
            border-color: var(--danger);
            color: var(--danger);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            border-top: 1px solid rgba(0, 212, 255, 0.15);
            margin-top: 40px;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .footer-links a {
            color: #8892b0;
            text-decoration: none;
            transition: all 0.3s;
        }

        .footer-links a:hover {
            color: var(--primary);
        }

        /* Animations */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 255, 136, 0.15);
            border-radius: 30px;
            padding: 4px 12px;
            font-size: 0.7rem;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .nav-container { flex-direction: column; text-align: center; }
            .metric-value { font-size: 1.8rem; }
        }
    </style>
</head>
<body>

<div class="particles" id="particles"></div>

<nav class="navbar">
    <div class="nav-container">
        <div class="logo">
            <i class="fas fa-cloud-upload-alt"></i> INPTIC DevOps
        </div>
        <div class="nav-links">
            <a href="/"><i class="fas fa-home"></i> Accueil</a>
            <a href="/metrics"><i class="fas fa-chart-line"></i> Métriques</a>
            <a href="/health"><i class="fas fa-heartbeat"></i> Health</a>
            <a href="http://192.168.44.10:3000" target="_blank"><i class="fas fa-chart-pie"></i> Grafana</a>
            <a href="http://192.168.44.10:8084" target="_blank"><i class="fab fa-jenkins"></i> Jenkins</a>
            <a href="http://192.168.44.10:9091" target="_blank"><i class="fas fa-fire"></i> Prometheus</a>
        </div>
    </div>
</nav>

<div class="container">
    <div class="hero">
        <h1><i class="fas fa-graduation-cap"></i> Gestion des Étudiants</h1>
        <p>Plateforme DevOps de supervision et d'automatisation</p>
        <div class="badge">
            <i class="fas fa-code-branch"></i> CI/CD Pipeline | <i class="fas fa-chart-line"></i> Monitoring | <i class="fas fa-docker"></i> Containerisé
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">REQUÊTES HTTP</span>
                <i class="fas fa-globe"></i>
            </div>
            <div class="metric-value" id="requestCount">{{ request_count }}</div>
            <div class="metric-unit">requêtes totales</div>
            <div class="trend up" id="trendReq">📈 +0 req/min</div>
        </div>

        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">UPTIME</span>
                <i class="fas fa-clock"></i>
            </div>
            <div class="metric-value" id="uptime">{{ uptime }}</div>
            <div class="metric-unit">secondes</div>
            <div class="trend up" id="trendUptime">⏱️ En service</div>
        </div>

        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">STATUT</span>
                <i class="fas fa-microchip"></i>
            </div>
            <div class="metric-value" id="status">
                <span class="live-dot" style="display: inline-block; margin-right: 8px;"></span> ACTIF
            </div>
            <div class="metric-unit">opérationnel</div>
            <div class="trend"><span class="live-badge"><span class="live-dot"></span> LIVE</span></div>
        </div>

        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">SERVEUR</span>
                <i class="fas fa-server"></i>
            </div>
            <div class="metric-value" id="server">{{ server }}</div>
            <div class="metric-unit">plateforme</div>
            <div class="trend"><i class="fab fa-linux"></i> Linux</div>
        </div>
    </div>

    <div class="services-section">
        <div class="section-title">
            <i class="fas fa-cubes"></i>
            <span>Infrastructure DevOps</span>
        </div>
        <div class="services-grid">
            <div class="service-item">
                <i class="fab fa-docker" style="color: #2496ed;"></i>
                <div>Docker</div>
                <div class="status">✅ Conteneurisé</div>
            </div>
            <div class="service-item">
                <i class="fab fa-jenkins" style="color: #d33833;"></i>
                <div>Jenkins</div>
                <div class="status">✅ CI/CD Actif</div>
            </div>
            <div class="service-item">
                <i class="fas fa-fire" style="color: #e6522c;"></i>
                <div>Prometheus</div>
                <div class="status">✅ Monitoring</div>
            </div>
            <div class="service-item">
                <i class="fas fa-chart-line" style="color: #f47d20;"></i>
                <div>Grafana</div>
                <div class="status">✅ Visualisation</div>
            </div>
        </div>
    </div>

    <div class="actions">
        <button class="btn btn-primary" onclick="generateRequest()">
            <i class="fas fa-bolt"></i> Générer une requête
        </button>
        <button class="btn btn-outline" onclick="refreshMetrics()">
            <i class="fas fa-sync-alt"></i> Actualiser
        </button>
        <button class="btn btn-outline btn-danger" onclick="generateBatch(10)">
            <i class="fas fa-fire"></i> Batch x10
        </button>
    </div>

    <div class="footer">
        <div class="footer-links">
            <a href="/metrics"><i class="fas fa-chart-line"></i> Métriques Prometheus</a>
            <a href="/health"><i class="fas fa-heartbeat"></i> Health Check</a>
            <a href="http://192.168.44.10:3000"><i class="fas fa-chart-pie"></i> Tableau de bord Grafana</a>
            <a href="http://192.168.44.10:8084"><i class="fab fa-jenkins"></i> Pipeline Jenkins</a>
        </div>
        <p>© 2024 INPTIC - Infrastructure DevOps avec Docker, Jenkins, Prometheus & Grafana</p>
        <p><small>API REST | Métriques en temps réel | CI/CD Automatisé</small></p>
    </div>
</div>

<script>
    let lastCount = {{ request_count }};
    
    async function generateRequest() {
        await fetch('/');
        await refreshMetrics();
        animateButton('btn-primary');
    }
    
    async function generateBatch(n) {
        for (let i = 0; i < n; i++) {
            await fetch('/');
            await new Promise(r => setTimeout(r, 50));
        }
        await refreshMetrics();
        animateButton('btn-danger');
    }
    
    async function refreshMetrics() {
        const response = await fetch('/metrics');
        const text = await response.text();
        
        const countMatch = text.match(/http_requests_total (\d+)/);
        const uptimeMatch = text.match(/app_uptime_seconds (\d+)/);
        
        if (countMatch) {
            const newCount = parseInt(countMatch[1]);
            const diff = newCount - lastCount;
            document.getElementById('requestCount').textContent = newCount;
            const trendEl = document.getElementById('trendReq');
            if (diff > 0) {
                trendEl.innerHTML = `📈 +${diff} req/min`;
                trendEl.className = 'trend up';
            }
            lastCount = newCount;
        }
        if (uptimeMatch) {
            document.getElementById('uptime').textContent = uptimeMatch[1];
        }
    }
    
    function animateButton(className) {
        const btn = document.querySelector(`.${className}`);
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => { btn.style.transform = ''; }, 200);
    }
    
    // Création des particules
    function createParticles() {
        const container = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.width = particle.style.height = Math.random() * 4 + 1 + 'px';
            particle.style.animationDelay = Math.random() * 5 + 's';
            particle.style.animationDuration = Math.random() * 10 + 10 + 's';
            container.appendChild(particle);
        }
    }
    
    setInterval(refreshMetrics, 5000);
    refreshMetrics();
    createParticles();
</script>
</body>
</html>
'''

def get_server_info():
    return {
        'hostname': platform.node(),
        'os': platform.system(),
        'release': platform.release()
    }

@app.route('/')
def home():
    server_info = get_server_info()
    return render_template_string(HTML_TEMPLATE, 
                                  request_count=request_count,
                                  uptime=int(time.time() - start_time),
                                  server=f"{server_info['hostname']}")

@app.route('/metrics')
def metrics():
    global request_count
    request_count += 1
    metrics_data = f"""# HELP http_requests_total Total des requêtes HTTP
# TYPE http_requests_total counter
http_requests_total {request_count}
# HELP app_uptime_seconds Temps de fonctionnement de l'application
# TYPE app_uptime_seconds gauge
app_uptime_seconds {int(time.time() - start_time)}
# HELP requests_per_minute Requêtes par minute
# TYPE requests_per_minute gauge
requests_per_minute 0
"""
    return Response(metrics_data, mimetype='text/plain')

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "gestion-etudiants-api",
        "version": "2.0.0"
    }

@app.route('/api/info')
def api_info():
    return jsonify({
        "service": "INPTIC DevOps Platform",
        "version": "2.0.0",
        "endpoints": {
            "/": "Accueil",
            "/metrics": "Métriques Prometheus",
            "/health": "Health check",
            "/api/info": "Informations API"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
