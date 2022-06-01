const URL = 'http://127.0.0.1:6060';

const colors = [];
for(let i = 0;i<100;i++){
    colors.push(`rgba(${Math.floor((Math.random() * (255 - 0 + 1)) + 0)}, ${Math.floor((Math.random() * (255 - 0 + 1)) + 0)}, ${Math.floor((Math.random() * (255 - 0 + 1)) + 0)})`);
}

//Por cada gráfica se debe hacer una petición
fetch(`${URL}/administration/dashboard_char_regulation/`).then(res => res.json()).then(res => {
    const config = {
        type: 'bar',
        data: {
            labels: ['Nacional', 'Internacional'],
            datasets: [{
                label: 'Edificios por normativa',
                backgroundColor: colors,
                borderColor: colors,
                data: res
            }]
        },
        options: {}
    }
    const ctx = document.getElementById('buildingsByRegulation').getContext('2d');
    if (ctx !== null) {
        const myChart = new Chart(
            ctx,
            config
        );
    }
}).catch(err => err);

fetch(`${URL}/administration/dashboard_buildings_by_type/`).then(res => res.json()).then(res => {
    const data = res.map(info => info.cantidad);
    const labels = res.map(info => info.site_type);

    const config = {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                label: 'Edificios por tipo',
                backgroundColor: colors,
                borderColor: ['rgb(255, 99, 132)',
                    'rgb(255, 159, 64)'],
                data
            }]
        },
        options: {}
    }
    const ctx = document.getElementById('buildingsByType').getContext('2d');
    if (ctx !== null) {
        const myChart = new Chart(
            ctx,
            config
        );
    }

}).catch(err => err)



fetch(`${URL}/administration/dashboard_building_inspection_state/`).then(res => res.json()).then(res => {
    const config = {
        type: 'bar',
        data: {
            labels:['Aprobados','No Aprobados','Sin información'],
            datasets: [{
                label: 'Edificios por estado de inspección',
                backgroundColor: colors,
                borderColor: ['rgb(255, 99, 132)',
                    'rgb(255, 159, 64)'],
                data: res
            }]
        },
        options: {}
    }
    const ctx = document.getElementById('buildingsByInspectionState').getContext('2d');
    if (ctx !== null) {
        const myChart = new Chart(
            ctx,
            config
        );
    }

}).catch(err => err)

