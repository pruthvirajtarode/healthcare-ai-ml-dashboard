import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class HealthcareEDA:
    """
    Exploratory Data Analysis for Healthcare dataset
    Generates comprehensive insights and visualizations
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        """Load cleaned dataset"""
        self.df = pd.read_csv(self.filepath)
        print(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def get_basic_statistics(self):
        """Generate basic statistics"""
        print("\n=== BASIC STATISTICS ===")
        
        stats = {
            'dataset_info': {
                'total_records': len(self.df),
                'total_features': len(self.df.columns),
                'feature_names': list(self.df.columns)
            },
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'describe_stats': self.df.describe().round(2).to_dict()
        }
        
        print("\nDataset Info:")
        print(f"Total Records: {stats['dataset_info']['total_records']}")
        print(f"Total Features: {stats['dataset_info']['total_features']}")
        print("\nFeature Statistics:")
        print(self.df.describe().round(2))
        
        self.analysis_results['basic_statistics'] = stats
        return stats
    
    def analyze_age_distribution(self):
        """Analyze age distribution"""
        print("\n=== AGE DISTRIBUTION ANALYSIS ===")
        
        age_stats = {
            'mean_age': float(self.df['Age'].mean()),
            'median_age': float(self.df['Age'].median()),
            'std_age': float(self.df['Age'].std()),
            'min_age': float(self.df['Age'].min()),
            'max_age': float(self.df['Age'].max()),
            'age_groups': {}
        }
        
        # Age grouping
        age_bins = [0, 18, 30, 45, 60, 100]
        age_labels = ['0-18', '18-30', '30-45', '45-60', '60+']
        self.df['Age_Group'] = pd.cut(self.df['Age'], bins=age_bins, labels=age_labels)
        
        age_group_counts = self.df['Age_Group'].value_counts().sort_index()
        age_stats['age_groups'] = age_group_counts.to_dict()
        
        print(f"Mean Age: {age_stats['mean_age']:.2f}")
        print(f"Median Age: {age_stats['median_age']:.2f}")
        print(f"Age Range: {age_stats['min_age']:.0f} - {age_stats['max_age']:.0f}")
        print("\nAge Group Distribution:")
        print(age_group_counts)
        
        self.analysis_results['age_analysis'] = age_stats
        return age_stats
    
    def analyze_bmi_distribution(self):
        """Analyze BMI distribution and categories"""
        print("\n=== BMI DISTRIBUTION ANALYSIS ===")
        
        bmi_stats = {
            'mean_bmi': float(self.df['BMI'].mean()),
            'median_bmi': float(self.df['BMI'].median()),
            'std_bmi': float(self.df['BMI'].std()),
            'min_bmi': float(self.df['BMI'].min()),
            'max_bmi': float(self.df['BMI'].max()),
            'bmi_categories': {}
        }
        
        # BMI Categories (WHO)
        # Underweight: < 18.5, Normal: 18.5-24.9, Overweight: 25-29.9, Obese: >= 30
        def categorize_bmi(bmi):
            if bmi < 18.5:
                return 'Underweight'
            elif 18.5 <= bmi < 25:
                return 'Normal'
            elif 25 <= bmi < 30:
                return 'Overweight'
            else:
                return 'Obese'
        
        self.df['BMI_Category'] = self.df['BMI'].apply(categorize_bmi)
        bmi_category_counts = self.df['BMI_Category'].value_counts()
        bmi_stats['bmi_categories'] = bmi_category_counts.to_dict()
        
        print(f"Mean BMI: {bmi_stats['mean_bmi']:.2f}")
        print(f"Median BMI: {bmi_stats['median_bmi']:.2f}")
        print(f"BMI Range: {bmi_stats['min_bmi']:.2f} - {bmi_stats['max_bmi']:.2f}")
        print("\nBMI Category Distribution:")
        print(bmi_category_counts)
        
        self.analysis_results['bmi_analysis'] = bmi_stats
        return bmi_stats
    
    def analyze_blood_pressure(self):
        """Analyze blood pressure distribution"""
        print("\n=== BLOOD PRESSURE ANALYSIS ===")
        
        bp_stats = {
            'mean_bp': float(self.df['Blood_Pressure'].mean()),
            'median_bp': float(self.df['Blood_Pressure'].median()),
            'std_bp': float(self.df['Blood_Pressure'].std()),
            'min_bp': float(self.df['Blood_Pressure'].min()),
            'max_bp': float(self.df['Blood_Pressure'].max()),
            'bp_categories': {}
        }
        
        # BP Categories
        def categorize_bp(bp):
            if bp < 120:
                return 'Normal'
            elif 120 <= bp < 140:
                return 'Elevated'
            elif 140 <= bp < 160:
                return 'Stage 1 Hypertension'
            else:
                return 'Stage 2 Hypertension'
        
        self.df['BP_Category'] = self.df['Blood_Pressure'].apply(categorize_bp)
        bp_category_counts = self.df['BP_Category'].value_counts()
        bp_stats['bp_categories'] = bp_category_counts.to_dict()
        
        print(f"Mean BP: {bp_stats['mean_bp']:.2f}")
        print(f"Median BP: {bp_stats['median_bp']:.2f}")
        print(f"BP Range: {bp_stats['min_bp']:.0f} - {bp_stats['max_bp']:.0f}")
        print("\nBP Category Distribution:")
        print(bp_category_counts)
        
        self.analysis_results['bp_analysis'] = bp_stats
        return bp_stats
    
    def analyze_glucose(self):
        """Analyze glucose distribution"""
        print("\n=== GLUCOSE DISTRIBUTION ANALYSIS ===")
        
        glucose_stats = {
            'mean_glucose': float(self.df['Glucose'].mean()),
            'median_glucose': float(self.df['Glucose'].median()),
            'std_glucose': float(self.df['Glucose'].std()),
            'min_glucose': float(self.df['Glucose'].min()),
            'max_glucose': float(self.df['Glucose'].max()),
            'glucose_categories': {}
        }
        
        # Glucose Categories (fasting)
        def categorize_glucose(glucose):
            if glucose < 100:
                return 'Normal'
            elif 100 <= glucose < 126:
                return 'Prediabetic'
            else:
                return 'Diabetic'
        
        self.df['Glucose_Category'] = self.df['Glucose'].apply(categorize_glucose)
        glucose_category_counts = self.df['Glucose_Category'].value_counts()
        glucose_stats['glucose_categories'] = glucose_category_counts.to_dict()
        
        print(f"Mean Glucose: {glucose_stats['mean_glucose']:.2f}")
        print(f"Median Glucose: {glucose_stats['median_glucose']:.2f}")
        print(f"Glucose Range: {glucose_stats['min_glucose']:.0f} - {glucose_stats['max_glucose']:.0f}")
        print("\nGlucose Category Distribution:")
        print(glucose_category_counts)
        
        self.analysis_results['glucose_analysis'] = glucose_stats
        return glucose_stats
    
    def analyze_disease_risk(self):
        """Analyze disease risk distribution"""
        print("\n=== DISEASE RISK ANALYSIS ===")
        
        risk_distribution = self.df['Disease_Risk'].value_counts()
        risk_percentage = (risk_distribution / len(self.df) * 100).round(2)
        
        risk_stats = {
            'disease_distribution': risk_distribution.to_dict(),
            'disease_percentage': risk_percentage.to_dict(),
            'high_risk_count': len(self.df[self.df['Disease_Risk'] == 'Heart Risk'])
        }
        
        print("\nDisease Risk Distribution:")
        for disease, count in risk_distribution.items():
            percentage = (count / len(self.df)) * 100
            print(f"{disease}: {count} ({percentage:.2f}%)")
        
        self.analysis_results['disease_risk_analysis'] = risk_stats
        return risk_stats
    
    def analyze_geographical_distribution(self):
        """Analyze city-wise distribution"""
        print("\n=== GEOGRAPHICAL DISTRIBUTION ===")
        
        city_distribution = self.df['City'].value_counts()
        
        city_stats = {
            'city_distribution': city_distribution.to_dict(),
            'total_cities': len(city_distribution)
        }
        
        print(f"\nTotal Cities: {city_stats['total_cities']}")
        print("\nPatients by City:")
        print(city_distribution)
        
        self.analysis_results['geographical_analysis'] = city_stats
        return city_stats
    
    def analyze_correlations(self):
        """Analyze correlations between features"""
        print("\n=== CORRELATION ANALYSIS ===")
        
        numeric_cols = ['Age', 'BMI', 'Blood_Pressure', 'Glucose']
        correlation_matrix = self.df[numeric_cols].corr()
        
        # Convert to serializable format
        correlation_dict = {}
        for col in correlation_matrix.columns:
            correlation_dict[col] = correlation_matrix[col].round(3).to_dict()
        
        print("\nCorrelation Matrix:")
        print(correlation_matrix.round(3))
        
        self.analysis_results['correlation_analysis'] = correlation_dict
        return correlation_dict
    
    def identify_high_risk_patients(self):
        """Identify high-risk patients"""
        print("\n=== HIGH-RISK PATIENT IDENTIFICATION ===")
        
        # Criteria for high-risk:
        # 1. Disease Risk = 'Heart Risk' or 'Diabetes' or 'Hypertension'
        # 2. Age > 50
        # 3. BMI >= 30 or BMI < 18.5
        # 4. Glucose > 125
        # 5. BP > 140
        
        high_risk = self.df[
            ((self.df['Disease_Risk'].isin(['Heart Risk', 'Diabetes', 'Hypertension'])) |
             (self.df['Age'] > 50) |
             (self.df['BMI'] >= 30) |
             (self.df['Glucose'] > 125) |
             (self.df['Blood_Pressure'] > 140))
        ]
        
        high_risk_stats = {
            'total_high_risk_patients': len(high_risk),
            'percentage_high_risk': round(len(high_risk) / len(self.df) * 100, 2),
            'high_risk_by_disease': high_risk['Disease_Risk'].value_counts().to_dict(),
            'average_age': round(high_risk['Age'].mean(), 2),
            'average_bmi': round(high_risk['BMI'].mean(), 2),
            'average_glucose': round(high_risk['Glucose'].mean(), 2)
        }
        
        print(f"\nTotal High-Risk Patients: {high_risk_stats['total_high_risk_patients']}")
        print(f"Percentage: {high_risk_stats['percentage_high_risk']}%")
        print(f"\nAverage Metrics (High-Risk):")
        print(f"  Age: {high_risk_stats['average_age']:.2f}")
        print(f"  BMI: {high_risk_stats['average_bmi']:.2f}")
        print(f"  Glucose: {high_risk_stats['average_glucose']:.2f}")
        print("\nHigh-Risk by Disease:")
        print(high_risk['Disease_Risk'].value_counts())
        
        self.analysis_results['high_risk_analysis'] = high_risk_stats
        self.high_risk_df = high_risk
        return high_risk_stats, high_risk
    
    def perform_eda(self):
        """Execute full EDA pipeline"""
        print("="*60)
        print("HEALTHCARE EXPLORATORY DATA ANALYSIS")
        print("="*60)
        
        self.load_data()
        self.get_basic_statistics()
        self.analyze_age_distribution()
        self.analyze_bmi_distribution()
        self.analyze_blood_pressure()
        self.analyze_glucose()
        self.analyze_disease_risk()
        self.analyze_geographical_distribution()
        self.analyze_correlations()
        self.identify_high_risk_patients()
        
        print("\n" + "="*60)
        print("EDA COMPLETE")
        print("="*60)
        
        return self.analysis_results
    
    def save_analysis_report(self, output_path):
        """Save analysis report as JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        print(f"\nAnalysis report saved to: {output_path}")
        return output_path
    
    def save_high_risk_patients(self, output_path):
        """Save high-risk patients to CSV"""
        self.high_risk_df.to_csv(output_path, index=False)
        print(f"High-risk patients saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    # Initialize EDA
    data_path = Path(__file__).parent.parent / "data" / "healthcare_data_cleaned.csv"
    eda = HealthcareEDA(str(data_path))
    
    # Perform EDA
    results = eda.perform_eda()
    
    # Save reports
    report_path = Path(__file__).parent.parent / "data" / "eda_report.json"
    eda.save_analysis_report(str(report_path))
    
    high_risk_path = Path(__file__).parent.parent / "data" / "high_risk_patients.csv"
    eda.save_high_risk_patients(str(high_risk_path))
