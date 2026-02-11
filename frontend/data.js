// Mock dataset - In production, this would come from the backend API

const mockData = {
    // Overall statistics
    totalPatients: 85,
    highRiskPatients: 42,
    averageAge: 45.3,
    averageBMI: 26.8,
    averageBloodPressure: 143.5,
    averageGlucose: 128.4,
    averageRiskScore: 52.3,
    averageHealthScore: 58.7,

    // Health score distribution
    healthScoreDistribution: {
        excellent: 15,
        good: 32,
        poor: 38
    },

    // Risk score distribution
    riskScoreDistribution: {
        highRisk: 42,
        mediumRisk: 28,
        lowRisk: 15
    },

    // Age groups
    ageGroups: {
        '0-18': 2,
        '18-30': 12,
        '30-45': 25,
        '45-60': 28,
        '60+': 18
    },

    // BMI categories
    bmiCategories: {
        'Underweight': 5,
        'Normal': 22,
        'Overweight': 31,
        'Obese': 27
    },

    // Disease distribution
    diseaseDistribution: {
        'Heart Risk': 18,
        'Diabetes': 15,
        'Hypertension': 20,
        'Asthma': 15,
        'Normal': 17
    },

    // High-risk disease distribution
    highRiskDiseaseBreakdown: {
        'Heart Risk': 18,
        'Diabetes': 12,
        'Hypertension': 12
    },

    // City distribution
    cityDistribution: {
        'Jaipur': 12,
        'Delhi': 14,
        'Chennai': 11,
        'Pune': 10,
        'Bangalore': 18,
        'Mumbai': 20
    },

    // Cardiovascular metrics
    cardiovascularRisk: 58.5,
    hypertensionRiskPatients: 35,

    // Metabolic metrics
    metabolicHealth: 52.3,
    goodMetabolism: 28,
    poorMetabolism: 35,

    // High-risk patient criteria met
    highRiskCriteria: {
        diseaseRisk: 18,
        ageOver50: 28,
        obeseBMI: 27,
        highGlucose: 32,
        highBP: 35
    },

    // ML Model info
    mlModelAccuracy: 85.2,
    mlTrainingAccuracy: 87.5
};

// Mock KPI data
const kpiData = {
    overall: {
        totalPatients: 85,
        avgAge: 45.3,
        avgBMI: 26.8,
        avgBP: 143.5,
        avgGlucose: 128.4
    },
    health: {
        excellent: { count: 15, percentage: 17.6 },
        good: { count: 32, percentage: 37.6 },
        poor: { count: 38, percentage: 44.7 }
    },
    disease: {
        heartRisk: 18,
        diabetes: 15,
        hypertension: 20,
        asthma: 15,
        normal: 17
    },
    risk: {
        highRisk: 42,
        mediumRisk: 28,
        lowRisk: 15
    },
    cardiovascular: {
        avgRisk: 58.5,
        hypertensionCases: 35
    },
    metabolic: {
        avgHealth: 52.3,
        goodMetabolism: 28,
        poorMetabolism: 35
    }
};

// Chart colors
const chartColors = {
    primary: '#2563eb',
    secondary: '#10b981',
    danger: '#ef4444',
    warning: '#f59e0b',
    light: '#e5e7eb'
};

// Chart color palettes
const paletteMulti = [
    '#2563eb',
    '#10b981',
    '#f59e0b',
    '#ef4444',
    '#8b5cf6',
    '#ec4899'
];
