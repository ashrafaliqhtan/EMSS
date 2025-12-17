document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize charts
    initExamTypeChart();
    initConflictTrendChart();

    // Initialize DataTable
    initExamScheduleTable();

    // Filter form submission handler
    const filterForm = document.querySelector('.filter-card form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Add loading indicator
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Applying...';
        });
    }

    // Schedule generation modal handler
    const scheduleModal = document.getElementById('generateScheduleModal');
    if (scheduleModal) {
        scheduleModal.addEventListener('shown.bs.modal', function() {
            // Set default end date to 7 days from now
            const today = new Date();
            const nextWeek = new Date(today);
            nextWeek.setDate(nextWeek.getDate() + 7);
            
            document.querySelector('input[name="start_date"]').valueAsDate = today;
            document.querySelector('input[name="end_date"]').valueAsDate = nextWeek;
        });
    }
});

function initExamScheduleTable() {
    const table = document.getElementById('examScheduleTable');
    if (table) {
        // Simple client-side sorting/filtering can be added here
        // For full features, consider using DataTables.js
        table.querySelectorAll('th[data-sortable]').forEach(header => {
            header.addEventListener('click', () => {
                sortTable(table, header.cellIndex, header.dataset.sortable);
            });
        });
    }
}

function sortTable(table, columnIndex, dataType) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAsc = tbody.dataset.sortDirection === 'asc';
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        if (dataType === 'text') {
            return isAsc ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        } else if (dataType === 'date') {
            return isAsc ? 
                new Date(aValue) - new Date(bValue) : 
                new Date(bValue) - new Date(aValue);
        } else if (dataType === 'numeric') {
            return isAsc ? 
                parseFloat(aValue) - parseFloat(bValue) : 
                parseFloat(bValue) - parseFloat(aValue);
        }
        return 0;
    });
    
    // Remove all existing rows
    rows.forEach(row => tbody.removeChild(row));
    
    // Add sorted rows
    rows.forEach(row => tbody.appendChild(row));
    
    // Update sort direction
    tbody.dataset.sortDirection = isAsc ? 'desc' : 'asc';
    
    // Update sort indicators
    table.querySelectorAll('th').forEach(th => th.classList.remove('sorted-asc', 'sorted-desc'));
    const header = table.rows[0].cells[columnIndex];
    header.classList.add(isAsc ? 'sorted-desc' : 'sorted-asc');
}

function initExamTypeChart() {
    const ctx = document.getElementById('examTypeChart');
    if (!ctx) return;
    
    const chartData = JSON.parse(ctx.dataset.chartData || '{}');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartData.labels || ['PBE', 'CBE'],
            datasets: [{
                data: chartData.data || [50, 50],
                backgroundColor: [
                    'rgba(78, 115, 223, 0.8)',
                    'rgba(28, 200, 138, 0.8)'
                ],
                borderColor: [
                    'rgba(78, 115, 223, 1)',
                    'rgba(28, 200, 138, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function initConflictTrendChart() {
    const ctx = document.getElementById('conflictTrendChart');
    if (!ctx) return;
    
    const chartData = JSON.parse(ctx.dataset.chartData || '{}');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Resolved',
                    data: chartData.resolved || [12, 19, 15, 22, 18, 15, 20],
                    backgroundColor: 'rgba(28, 200, 138, 0.1)',
                    borderColor: 'rgba(28, 200, 138, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Unresolved',
                    data: chartData.unresolved || [8, 12, 10, 15, 12, 8, 10],
                    backgroundColor: 'rgba(231, 74, 59, 0.1)',
                    borderColor: 'rgba(231, 74, 59, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    },
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Utility function for AJAX requests
function fetchDashboardData(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return fetch(`/dashboard/data?${queryString}`)
        .then(response => response.json())
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            return null;
        });
}

// Real-time updates (polling every 30 seconds)
function startDashboardUpdates() {
    setInterval(() => {
        fetchDashboardData()
            .then(data => {
                if (data) {
                    updateDashboardMetrics(data);
                }
            });
    }, 30000);
}

function updateDashboardMetrics(data) {
    // Update counters and charts with fresh data
    // This would depend on your specific dashboard elements
    console.log('Updating dashboard with fresh data:', data);
}

// Start updates if enabled
if (window.enableDashboardUpdates) {
    startDashboardUpdates();
}