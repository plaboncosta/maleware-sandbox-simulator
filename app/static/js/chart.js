function renderFilesystemChart(logs) {
    const labels = [];
    const data = [];

    logs.forEach(e => {
        if (e.fs_event) {
            labels.push(e.fs_event.substring(0, 60));
            data.push(1);
        }
    });

    new Chart(document.getElementById('fsChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Filesystem Events',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
