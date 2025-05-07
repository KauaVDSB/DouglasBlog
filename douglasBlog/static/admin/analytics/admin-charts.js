const charts = {};


async function fetchData(period, path){
    let url = `/api/analytics/${period}`;
    if (path){
        url += `?path=${encodeURIComponent(path)}`
    }

    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
    }

    return await res.json()
}

async function buildChart(ctxId, label, data) {
    
    if (charts[ctxId]){
        charts[ctxId].destroy();
    }
    
    const ctx = document.getElementById(ctxId).getContext('2d');

    charts[ctxId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.period.slice(0,10)),
            datasets: [{
                label,
                data: data.map(d => d.views),
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
}


async function renderAllCharts() {
    try{
        const path = document.getElementById('filter-path').value;

        const [dailyData, weeklyData, monthlyData] = await Promise.all([
            fetchData('daily',   path),
            fetchData('weekly',  path),
            fetchData('monthly', path),
        ])

        buildChart('chartDaily',   "Visitas Diárias",  dailyData);
        buildChart('chartWeekly',  "Visitas Semanais", weeklyData);
        buildChart('chartMonthly', "Visitas Mensais",  monthlyData);
    }
    catch (err) {
        console.error("Falha ao renderizar gráficos:", err);
    }
}

document.getElementById('filter-path')
        .addEventListener('change', renderAllCharts);

document.addEventListener('DOMContentLoaded', renderAllCharts);
