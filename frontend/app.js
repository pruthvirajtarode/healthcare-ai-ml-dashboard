/**
 * Switch between tabs - MUST BE FIRST
 */
function switchTab(tabName) {
    console.log('switchTab called with:', tabName);
    
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Highlight active button - find button that calls this tab
    const activeButton = Array.from(buttons).find(btn => 
        btn.getAttribute('onclick') === `switchTab('${tabName}')`
    );
    if (activeButton) {
        activeButton.classList.add('active');
    }

    // Refresh charts if switching to analytics tab
    if (typeof charts !== 'undefined' && tabName === 'analytics') {
        setTimeout(() => {
            Object.values(charts).forEach(chart => {
                if (chart) chart.resize();
            });
        }, 100);
    }
}

// Chart instances for cleanup
let charts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Healthcare Dashboard Initialized');
    updateDashboard();
    initializeCharts();
});

/**
 * Update dashboard with data
 */
function updateDashboard() {
    // Overview tab
    document.getElementById('totalPatients').textContent = mockData.totalPatients.toLocaleString();
    document.getElementById('highRiskCount').textContent = mockData.highRiskPatients.toLocaleString();
    document.getElementById('avgRiskScore').textContent = mockData.averageRiskScore.toFixed(1);
    document.getElementById('avgHealthScore').textContent = mockData.averageHealthScore.toFixed(1);

    // High-Risk tab
    const highRiskPct = ((mockData.highRiskPatients / mockData.totalPatients) * 100).toFixed(1);
    document.getElementById('highRiskPercentage').textContent = highRiskPct + '%';
    document.getElementById('highRiskHeartDiseases').textContent = mockData.highRiskDiseaseBreakdown['Heart Risk'];
    document.getElementById('highRiskDiabetes').textContent = mockData.highRiskDiseaseBreakdown['Diabetes'];
    document.getElementById('highRiskHypertension').textContent = mockData.highRiskDiseaseBreakdown['Hypertension'];

    // KPIs tab
    document.getElementById('kpiAvgAge').textContent = kpiData.overall.avgAge.toFixed(1);
    document.getElementById('kpiAvgBMI').textContent = kpiData.overall.avgBMI.toFixed(1);
    document.getElementById('kpiAvgBP').textContent = kpiData.overall.avgBP.toFixed(1);
    document.getElementById('kpiAvgGlucose').textContent = kpiData.overall.avgGlucose.toFixed(1);

    // Health distribution
    document.getElementById('healthExcellent').textContent = kpiData.health.excellent.count;
    document.getElementById('healthExcellentPct').textContent = kpiData.health.excellent.percentage.toFixed(1) + '%';
    document.getElementById('healthGood').textContent = kpiData.health.good.count;
    document.getElementById('healthGoodPct').textContent = kpiData.health.good.percentage.toFixed(1) + '%';
    document.getElementById('healthPoor').textContent = kpiData.health.poor.count;
    document.getElementById('healthPoorPct').textContent = kpiData.health.poor.percentage.toFixed(1) + '%';

    // Disease distribution
    document.getElementById('diseaseHeart').textContent = kpiData.disease.heartRisk;
    document.getElementById('diseaseDiabetes').textContent = kpiData.disease.diabetes;
    document.getElementById('diseaseHypertension').textContent = kpiData.disease.hypertension;
    document.getElementById('diseaseAsthma').textContent = kpiData.disease.asthma;
    document.getElementById('diseaseNormal').textContent = kpiData.disease.normal;
}

/**
 * Initialize all charts
 */
function initializeCharts() {
    createAgeDistributionChart();
    createBMIDistributionChart();
    createDiseaseRiskChart();
    createBPGlucoseChart();
    createCityDistributionChart();
    createHighRiskProfileChart();
}

/**
 * Age Distribution Chart
 */
function createAgeDistributionChart() {
    const ctx = document.getElementById('ageDistributionChart');
    if (!ctx) return;

    if (charts.ageDistribution) {
        charts.ageDistribution.destroy();
    }

    const labels = Object.keys(mockData.ageGroups);
    const data = Object.values(mockData.ageGroups);

    charts.ageDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Patients',
                data: data,
                backgroundColor: paletteMulti,
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Age Group Distribution'
                },
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        }
    });
}

/**
 * BMI Distribution Chart
 */
function createBMIDistributionChart() {
    const ctx = document.getElementById('bmiDistributionChart');
    if (!ctx) return;

    if (charts.bmiDistribution) {
        charts.bmiDistribution.destroy();
    }

    const labels = Object.keys(mockData.bmiCategories);
    const data = Object.values(mockData.bmiCategories);

    charts.bmiDistribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: paletteMulti,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'BMI Category Distribution'
                },
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

/**
 * Disease Risk Chart
 */
function createDiseaseRiskChart() {
    const ctx = document.getElementById('diseaseRiskChart');
    if (!ctx) return;

    if (charts.diseaseRisk) {
        charts.diseaseRisk.destroy();
    }

    const labels = Object.keys(mockData.diseaseDistribution);
    const data = Object.values(mockData.diseaseDistribution);

    charts.diseaseRisk = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: paletteMulti,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Disease Risk Distribution'
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Blood Pressure and Glucose Scatter Chart
 */
function createBPGlucoseChart() {
    const ctx = document.getElementById('bpGlucoseChart');
    if (!ctx) return;

    if (charts.bpGlucose) {
        charts.bpGlucose.destroy();
    }

    // Generate sample scatter data
    const scatterData = [];
    for (let i = 0; i < mockData.totalPatients; i++) {
        scatterData.push({
            x: Math.random() * 300 + 80,  // BP: 80-380
            y: Math.random() * 200 + 80   // Glucose: 80-280
        });
    }

    charts.bpGlucose = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Patient BP vs Glucose',
                data: scatterData,
                backgroundColor: '#2563eb',
                showLine: false,
                borderWidth: 1,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Blood Pressure vs Glucose Level'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Blood Pressure (mmHg)'
                    },
                    min: 60,
                    max: 300
                },
                y: {
                    title: {
                        display: true,
                        text: 'Glucose Level (mg/dL)'
                    },
                    min: 60,
                    max: 300
                }
            }
        }
    });
}

/**
 * City Distribution Chart
 */
function createCityDistributionChart() {
    const ctx = document.getElementById('cityDistributionChart');
    if (!ctx) return;

    if (charts.cityDistribution) {
        charts.cityDistribution.destroy();
    }

    const labels = Object.keys(mockData.cityDistribution);
    const data = Object.values(mockData.cityDistribution);

    charts.cityDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patients per City',
                data: data,
                backgroundColor: '#2563eb',
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Geographic Distribution by City'
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 2
                    }
                }
            }
        }
    });
}

/**
 * High-Risk Patient Profile Chart
 */
function createHighRiskProfileChart() {
    const ctx = document.getElementById('highRiskProfileChart');
    if (!ctx) return;

    if (charts.highRiskProfile) {
        charts.highRiskProfile.destroy();
    }

    const labels = Object.keys(mockData.highRiskCriteria);
    const data = Object.values(mockData.highRiskCriteria);

    charts.highRiskProfile = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Disease Risk',
                'Age Over 50',
                'Obese BMI',
                'High Glucose',
                'High BP'
            ],
            datasets: [{
                label: 'High-Risk Patients Meeting Criteria',
                data: data,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'High-Risk Patient Characteristics'
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 40,
                    ticks: {
                        stepSize: 10
                    }
                }
            }
        }
    });
}

/**
 * Predict Risk for patient
 */
function predictRisk(event) {
    event.preventDefault();

    // Get form values
    const patientName = document.getElementById('predName').value;
    const age = parseInt(document.getElementById('predAge').value);
    const bmi = parseFloat(document.getElementById('predBMI').value);
    const bp = parseInt(document.getElementById('predBP').value);
    const glucose = parseInt(document.getElementById('predGlucose').value);
    const disease = document.getElementById('predDisease').value;

    // Calculate risk score based on input
    let riskScore = 0;

    // Age risk (>50 increases risk)
    riskScore += age > 50 ? (age - 50) * 0.5 : 0;

    // BMI risk
    if (bmi < 18.5 || bmi >= 30) riskScore += 20;
    else if (bmi >= 25) riskScore += 10;

    // BP risk
    if (bp >= 140) riskScore += 20;
    else if (bp >= 120) riskScore += 10;

    // Glucose risk
    if (glucose >= 126) riskScore += 25;
    else if (glucose >= 100) riskScore += 15;

    // Disease risk
    const diseaseRiskMap = {
        'Normal': 0,
        'Asthma': 15,
        'Hypertension': 20,
        'Diabetes': 25,
        'Heart Risk': 30
    };
    riskScore += diseaseRiskMap[disease] || 0;

    // Normalize to 0-100
    riskScore = Math.min(100, riskScore);

    // Convert to probability (0-1)
    const riskProbability = riskScore / 100;
    const isHighRisk = riskProbability >= 0.5;

    // Display result
    displayPredictionResult(patientName, riskProbability, isHighRisk, age, bmi, bp, glucose, disease);
}

/**
 * Display prediction result
 */
function displayPredictionResult(name, probability, isHighRisk, age, bmi, bp, glucose, disease) {
    const resultDiv = document.getElementById('predictionResult');
    const contentDiv = document.getElementById('resultContent');

    const probabilityPercent = (probability * 100).toFixed(1);
    const riskLabel = isHighRisk ? 'HIGH RISK' : 'LOW RISK';
    const riskColor = isHighRisk ? 'high' : 'low';

    const html = `
        <div class="${riskColor === 'high' ? 'result-container high-risk' : ''}">
            <div class="risk-indicator">
                <span class="risk-badge ${riskColor}">${riskLabel}</span>
                <div>
                    <strong>Risk Assessment:</strong> ${name ? name + ' has' : 'This patient has'} a <strong>${probabilityPercent}%</strong> probability of being high-risk
                </div>
            </div>

            <div class="risk-probability">
                Risk Probability: ${probabilityPercent}%
                <div class="risk-probability-bar">
                    <div class="risk-probability-fill" style="width: ${probability * 100}%">
                        ${probabilityPercent}%
                    </div>
                </div>
            </div>

            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.5); border-radius: 8px;">
                <strong>Patient Profile${name ? ' - ' + name : ''}:</strong>
                <ul style="margin-top: 10px; margin-left: 20px;">
                    <li>Age: ${age} years</li>
                    <li>BMI: ${bmi} (${getBMICategory(bmi)})</li>
                    <li>Blood Pressure: ${bp} mmHg (${getBPCategory(bp)})</li>
                    <li>Glucose: ${glucose} mg/dL (${getGlucoseCategory(glucose)})</li>
                    <li>Disease: ${disease}</li>
                </ul>
            </div>

            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.5); border-radius: 8px;">
                <strong>Recommendations:</strong>
                <ul style="margin-top: 10px; margin-left: 20px;">
                    ${getRecommendations(isHighRisk, age, bmi, bp, glucose, disease)}
                </ul>
            </div>
        </div>
    `;

    contentDiv.innerHTML = html;
    resultDiv.classList.remove('hidden');
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Get BMI category
 */
function getBMICategory(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal';
    if (bmi < 30) return 'Overweight';
    return 'Obese';
}

/**
 * Get BP category
 */
function getBPCategory(bp) {
    if (bp < 120) return 'Normal';
    if (bp < 140) return 'Elevated';
    if (bp < 160) return 'Stage 1 Hypertension';
    return 'Stage 2 Hypertension';
}

/**
 * Get Glucose category
 */
function getGlucoseCategory(glucose) {
    if (glucose < 100) return 'Normal';
    if (glucose < 126) return 'Prediabetic';
    return 'Diabetic';
}

/**
 * Get medical recommendations
 */
function getRecommendations(isHighRisk, age, bmi, bp, glucose, disease) {
    let recommendations = [];

    if (isHighRisk) {
        recommendations.push('<li><strong>Immediate Action:</strong> Schedule comprehensive medical evaluation</li>');
        recommendations.push('<li>Consult with cardiologist for cardiovascular assessment</li>');
    }

    if (bmi >= 30) {
        recommendations.push('<li>Weight management program - target BMI < 25</li>');
        recommendations.push('<li>Regular physical activity: 150 minutes/week</li>');
    }

    if (bp >= 140) {
        recommendations.push('<li>Blood pressure management - target < 140/90 mmHg</li>');
        recommendations.push('<li>Reduce sodium intake, increase potassium-rich foods</li>');
    }

    if (glucose >= 126) {
        recommendations.push('<li>Diabetes screening and management</li>');
        recommendations.push('<li>Dietary modifications - reduce sugar/refined carbs</li>');
    }

    if (age > 50) {
        recommendations.push('<li>Annual health check-up recommended</li>');
        recommendations.push('<li>Preventive screening based on age and gender</li>');
    }

    if (disease === 'Heart Risk') {
        recommendations.push('<li>Cardiology consultation and ECG screening</li>');
    }

    if (disease === 'Diabetes') {
        recommendations.push('<li>Endocrinology consultation and glucose monitoring</li>');
    }

    if (disease === 'Hypertension') {
        recommendations.push('<li>Regular BP monitoring and medication adherence</li>');
    }

    if (recommendations.length === 0) {
        recommendations.push('<li>Maintain current healthy lifestyle</li>');
        recommendations.push('<li>Regular health check-ups (annual)</li>');
    }

    return recommendations.join('');
}
