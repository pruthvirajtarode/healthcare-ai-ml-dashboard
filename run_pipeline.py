"""
Healthcare ML Project - Master Pipeline Script
Executes the complete data engineering and ML pipeline
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from data_cleaning import HealthcareDataCleaner
from eda_analysis import HealthcareEDA
from feature_engineering import HealthcareFeatureEngineering
from ml_preparation import HealthcareMLPreparation

def main():
    print("="*70)
    print("HEALTHCARE AI/ML PROJECT - COMPLETE PIPELINE")
    print("="*70)
    
    data_dir = Path(__file__).parent / "data"
    
    # Step 1: Data Cleaning
    print("\n\n### STEP 1: DATA CLEANING ###\n")
    raw_data_path = data_dir / "healthcare_data.csv"
    cleaned_data_path = data_dir / "healthcare_data_cleaned.csv"
    
    cleaner = HealthcareDataCleaner(str(raw_data_path))
    cleaned_df = cleaner.clean_data()
    cleaner.save_cleaned_data(str(cleaned_data_path))
    
    # Step 2: EDA
    print("\n\n### STEP 2: EXPLORATORY DATA ANALYSIS ###\n")
    eda = HealthcareEDA(str(cleaned_data_path))
    eda_results = eda.perform_eda()
    eda.save_analysis_report(str(data_dir / "eda_report.json"))
    eda.save_high_risk_patients(str(data_dir / "high_risk_patients.csv"))
    
    # Step 3: Feature Engineering
    print("\n\n### STEP 3: FEATURE ENGINEERING & KPI CREATION ###\n")
    fe = HealthcareFeatureEngineering(str(cleaned_data_path))
    engineered_df = fe.engineer_features()
    fe.save_engineered_data(str(data_dir / "healthcare_data_engineered.csv"))
    fe.save_kpi_report(str(data_dir / "kpi_report.json"))
    
    # Step 4: ML Preparation
    print("\n\n### STEP 4: ML MODEL PREPARATION ###\n")
    ml_prep = HealthcareMLPreparation(str(data_dir / "healthcare_data_engineered.csv"))
    ml_prep.prepare_ml_dataset()
    ml_prep.save_preparation_report(str(data_dir / "ml_preparation_report.json"))
    ml_prep.save_training_data(str(data_dir / "ml_training_data"))
    
    print("\n" + "="*70)
    print("PIPELINE EXECUTION COMPLETE!")
    print("="*70)
    print("\nOutput Files Generated:")
    print(f"  1. {cleaned_data_path.name} - Cleaned dataset")
    print(f"  2. {(data_dir / 'eda_report.json').name} - EDA analysis results")
    print(f"  3. {(data_dir / 'high_risk_patients.csv').name} - High-risk patient list")
    print(f"  4. {(data_dir / 'healthcare_data_engineered.csv').name} - Engineered features dataset")
    print(f"  5. {(data_dir / 'kpi_report.json').name} - KPI metrics")
    print(f"  6. {(data_dir / 'ml_preparation_report.json').name} - ML preparation report")
    print(f"  7. {(data_dir / 'ml_training_data').name}/ - ML training/test data")
    print("\nNext Steps:")
    print("  - Review reports in /data directory")
    print("  - Start frontend application")
    print("  - Deploy ML models to production")

if __name__ == "__main__":
    main()
