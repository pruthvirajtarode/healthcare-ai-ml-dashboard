# Configuration for Healthcare ML Project

# Dataset Configuration
DATASET_CONFIG = {
    'raw_data_path': 'data/healthcare_data.csv',
    'cleaned_data_path': 'data/healthcare_data_cleaned.csv',
    'engineered_data_path': 'data/healthcare_data_engineered.csv',
    'test_split_ratio': 0.2,
    'random_state': 42
}

# Data Quality Rules
DATA_QUALITY = {
    'age': {
        'min': 0,
        'max': 100,
        'fill_method': 'median'
    },
    'bmi': {
        'min': 10,
        'max': 50,
        'fill_method': 'median'
    },
    'blood_pressure': {
        'min': 60,
        'max': 300,
        'fill_method': 'median'
    },
    'glucose': {
        'min': 50,
        'max': 300,
        'fill_method': 'median'
    }
}

# Feature Engineering Configuration
FEATURE_CONFIG = {
    'scale_features': True,
    'scaler_type': 'StandardScaler',
    'drop_original_categorical': False,
    'create_interaction_features': True
}

# ML Model Configuration
ML_CONFIG = {
    'models': ['logistic_regression', 'random_forest'],
    'logistic_regression': {
        'max_iter': 1000,
        'solver': 'lbfgs',
        'class_weight': 'balanced'
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'class_weight': 'balanced',
        'random_state': 42
    },
    'target_variable': 'risk_binary'  # Binary: High Risk (1) vs Low Risk (0)
}

# Risk Classification Rules
RISK_RULES = {
    'high_risk_criteria': [
        {'column': 'Disease_Risk', 'operator': 'in', 'values': ['Heart Risk', 'Diabetes', 'Hypertension']},
        {'column': 'Age', 'operator': '>', 'value': 50},
        {'column': 'BMI', 'operator': '>=', 'value': 30},
        {'column': 'BMI', 'operator': '<', 'value': 18.5},
        {'column': 'Glucose', 'operator': '>', 'value': 125},
        {'column': 'Blood_Pressure', 'operator': '>', 'value': 140}
    ],
    'risk_threshold': 0.5  # Probability threshold for high risk
}

# API Configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'json_sort_keys': False
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'charts': ['age_distribution', 'bmi_distribution', 'disease_risk', 'bp_glucose', 'city_distribution'],
    'tabs': ['overview', 'analytics', 'high-risk', 'kpis', 'predictions'],
    'update_frequency': 'on_demand'
}

# Report Configuration
REPORT_CONFIG = {
    'format': 'json',
    'include_visualizations': False,
    'output_directory': 'data/'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/healthcare_ml.log'
}

# City Options
CITIES = ['Jaipur', 'Delhi', 'Chennai', 'Pune', 'Bangalore', 'Mumbai']

# Disease Types
DISEASE_TYPES = ['Normal', 'Asthma', 'Hypertension', 'Diabetes', 'Heart Risk']

# Health Score Thresholds
HEALTH_SCORE_THRESHOLDS = {
    'excellent': 75,  # >= 75
    'good': 50,       # 50 - 75
    'poor': 0         # < 50
}

# Risk Score Thresholds
RISK_SCORE_THRESHOLDS = {
    'high': 60,       # >= 60
    'medium': 30,     # 30 - 60
    'low': 0          # < 30
}

# Feature Importance Threshold
FEATURE_IMPORTANCE_THRESHOLD = 0.01

# Random State for reproducibility
RANDOM_STATE = 42

# Metrics to Track
METRICS_TO_TRACK = [
    'accuracy',
    'precision',
    'recall',
    'f1_score',
    'roc_auc',
    'confusion_matrix'
]
