// API URL (update if needed)
const API_URL = 'http://localhost:5000/api/sensor_data';

// Function to fetch data from API and populate the table
async function fetchSensorData() {
    try {
        const response = await fetch(API_URL);
        const result = await response.json();

        // Verifica si los datos están dentro de "data"
        if (result.data && Array.isArray(result.data)) {
            populateTable(result.data);
        } else {
            console.error('Unexpected response format:', result);
        }
    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

// Populate the table with data
function populateTable(data) {
    const tableBody = document.getElementById('data-table').querySelector('tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.fecha}</td>
            <td>${item.hora}</td>
            <td>${item.idsensor}</td>
            <td>${item.valor}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Apply filters to the table
function applyFilters() {
    const idFilter = document.getElementById('filter-id').value.toLowerCase();
    const dateFilter = document.getElementById('filter-date').value;
    const timeFilter = document.getElementById('filter-time').value;

    const rows = document.querySelectorAll('#data-table tbody tr');
    rows.forEach(row => {
        const [id, date, time, sensorId] = row.children;

        // Filtra por ID, Fecha y Hora
        const matchesId = !idFilter || sensorId.textContent.toLowerCase().includes(idFilter);
        const matchesDate = !dateFilter || date.textContent === dateFilter;
        const matchesTime = !timeFilter || time.textContent.startsWith(timeFilter);  // Cambiar aquí

        if (matchesId && matchesDate && matchesTime) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Reset filters and show all rows
function resetFilters() {
    document.getElementById('filter-id').value = '';
    document.getElementById('filter-date').value = '';
    document.getElementById('filter-time').value = '';
    applyFilters(); // Reapply filters to show all rows
}

// Fetch and display data on page load
window.onload = fetchSensorData;
