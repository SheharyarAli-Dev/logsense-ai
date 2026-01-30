// Only declare these once at the top
const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const resultsDiv = document.getElementById("results");

// Handle form submit
form.addEventListener("submit", async (e) => {
    e.preventDefault();  // Prevent default page reload

    if (!fileInput.files.length) {
        alert("Please choose a log file.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    resultsDiv.innerHTML = "<p>Uploading and processing log...</p>";

    try {
        const response = await fetch("/upload-log", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json(); // ✅ data defined here
        displayResults(data);               // Display table, fixes, root cause
        renderCategoryChart(data);          // Draw pie chart

    } catch (err) {
        console.error(err);
        resultsDiv.innerHTML = "<p style='color:red;'>Error uploading file.</p>";
    }
});

// Function to display results in the frontend
function displayResults(data) {
    resultsDiv.innerHTML = "";

    // Root cause + severity
    const root = document.createElement("h3");
    root.textContent = `Root Cause: ${data.analysis.root_cause}`;
    resultsDiv.appendChild(root);

    const severity = document.createElement("p");
    severity.textContent = `Severity: ${data.analysis.severity}`;
    resultsDiv.appendChild(severity);

    // Suggested fixes
    if (data.suggested_fixes) {
        const fixesTitle = document.createElement("p");
        fixesTitle.textContent = "Suggested Fixes:";
        resultsDiv.appendChild(fixesTitle);

        const fixesList = document.createElement("ul");
        data.suggested_fixes.forEach(fix => {
            const li = document.createElement("li");
            li.textContent = fix;
            fixesList.appendChild(li);
        });
        resultsDiv.appendChild(fixesList);
    }

    // Logs table
    const table = document.createElement("table");
    table.innerHTML = `
        <tr>
            <th>Timestamp</th>
            <th>Level</th>
            <th>Message</th>
            <th>Category</th>
        </tr>
    `;

    data.sample_logs.forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${log.timestamp}</td>
            <td>${log.level}</td>
            <td>${log.message}</td>
            <td>${log.category}</td>
        `;

        // Color-code categories
        switch (log.category) {
            case "Normal": row.style.backgroundColor = "#d4edda"; break;
            case "Memory Issue": row.style.backgroundColor = "#fff3cd"; break;
            case "Crash Issue": row.style.backgroundColor = "#f8d7da"; break;
            case "General Error": row.style.backgroundColor = "#ffe5b4"; break;
            default: row.style.backgroundColor = "#e2e3e5"; 
        }

        table.appendChild(row);
    });

    resultsDiv.appendChild(table);
}

// Function to render category pie chart using Chart.js
function renderCategoryChart(data) {
    const categoryCounts = {};

    data.sample_logs.forEach(log => {
        categoryCounts[log.category] = (categoryCounts[log.category] || 0) + 1;
    });

    const labels = Object.keys(categoryCounts);
    const counts = Object.values(categoryCounts);

    // Destroy previous chart if exists
    if (window.categoryChartInstance) {
        window.categoryChartInstance.destroy();
    }

    const ctx = document.getElementById("categoryChart").getContext("2d");
    window.categoryChartInstance = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: labels.map(label => {
                    switch(label) {
                        case "Normal": return "#28a745";
                        case "Memory Issue": return "#ffc107";
                        case "Crash Issue": return "#dc3545";
                        case "General Error": return "#fd7e14";
                        default: return "#6c757d";
                    }
                })
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom" },
                title: { display: true, text: "Log Category Distribution" }
            }
        }
    });
}
