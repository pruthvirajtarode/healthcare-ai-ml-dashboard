import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder

class HealthcareFeatureEngineering:
    """
    Feature Engineering and KPI Creation for Healthcare ML
    Creates derived features and key performance indicators
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.kpis = {}
        self.feature_info = {}
        
    def load_data(self):
        """Load cleaned dataset"""
        self.df = pd.read_csv(self.filepath)
        print(f"Dataset loaded: {self.df.shape}")
        return self.df
    
    def create_health_score(self):
        """
        Create composite health score (0-100)
        Based on normalized health metrics
        """
        print("\n=== Creating Health Score ===")
        
        # Normalize individual metrics
        # Age: younger is better (normalize 0-100 to 100-0)
        age_score = 100 - (self.df['Age'] / 100) * 100
        
        # BMI: normal range (18.5-24.9) is best score (100)
        bmi_score = self.df['BMI'].apply(lambda x: 
            100 if (18.5 <= x <= 24.9) else
            100 - (abs(x - 21.5) / 21.5) * 100
        )
        bmi_score = np.clip(bmi_score, 0, 100)
        
        # Blood Pressure: lower is better, normal is <120
        bp_score = 100 - (self.df['Blood_Pressure'] / 300) * 100
        bp_score = np.clip(bp_score, 0, 100)
        
        # Glucose: lower is better, normal is <100
        glucose_score = 100 - (self.df['Glucose'] / 300) * 100
        glucose_score = np.clip(glucose_score, 0, 100)
        
        # Composite health score (weighted average)
        self.df['Health_Score'] = (
            age_score * 0.2 +
            bmi_score * 0.3 +
            bp_score * 0.25 +
            glucose_score * 0.25
        )
        
        print(f"Health Score Range: {self.df['Health_Score'].min():.2f} - {self.df['Health_Score'].max():.2f}")
        print(f"Average Health Score: {self.df['Health_Score'].mean():.2f}")
        
        self.feature_info['health_score'] = {
            'min': float(self.df['Health_Score'].min()),
            'max': float(self.df['Health_Score'].max()),
            'mean': float(self.df['Health_Score'].mean()),
            'description': 'Composite health score (0-100, higher is better)'
        }
        
        return self.df
    
    def create_risk_score(self):
        """
        Create risk score based on multiple factors
        Higher score = higher risk
        """
        print("\n=== Creating Risk Score ===")
        
        risk_score = 0
        
        # Age risk (>50 increases risk)
        age_risk = self.df['Age'].apply(lambda x: (x - 50) / 50 if x > 50 else 0)
        risk_score += age_risk * 15
        
        # BMI risk
        bmi_risk = self.df['BMI'].apply(lambda x:
            0 if (18.5 <= x <= 24.9) else
            10 if (25 <= x < 30) else
            20
        )
        risk_score += bmi_risk
        
        # Blood Pressure risk
        bp_risk = self.df['Blood_Pressure'].apply(lambda x:
            0 if x < 120 else
            10 if x < 140 else
            20
        )
        risk_score += bp_risk
        
        # Glucose risk
        glucose_risk = self.df['Glucose'].apply(lambda x:
            0 if x < 100 else
            15 if x < 126 else
            25
        )
        risk_score += glucose_risk
        
        # Disease risk
        disease_risk_map = {
            'Normal': 0,
            'Asthma': 15,
            'Hypertension': 20,
            'Diabetes': 25,
            'Heart Risk': 30
        }
        disease_risk = self.df['Disease_Risk'].map(disease_risk_map)
        risk_score += disease_risk
        
        self.df['Risk_Score'] = risk_score
        
        print(f"Risk Score Range: {self.df['Risk_Score'].min():.2f} - {self.df['Risk_Score'].max():.2f}")
        print(f"Average Risk Score: {self.df['Risk_Score'].mean():.2f}")
        
        self.feature_info['risk_score'] = {
            'min': float(self.df['Risk_Score'].min()),
            'max': float(self.df['Risk_Score'].max()),
            'mean': float(self.df['Risk_Score'].mean()),
            'description': 'Composite risk score (higher = more risk)'
        }
        
        return self.df
    
    def create_age_group_features(self):
        """Create age group categorical features"""
        print("\n=== Creating Age Group Features ===")
        
        age_bins = [0, 18, 30, 45, 60, 100]
        age_labels = ['Child_Teen', 'Young_Adult', 'Middle_Age', 'Senior', 'Elderly']
        self.df['Age_Group'] = pd.cut(self.df['Age'], bins=age_bins, labels=age_labels)
        
        # One-hot encoding for age groups
        age_dummies = pd.get_dummies(self.df['Age_Group'], prefix='AgeGroup')
        self.df = pd.concat([self.df, age_dummies], axis=1)
        
        print(f"Age Group distribution:\n{self.df['Age_Group'].value_counts()}")
        
        return self.df
    
    def create_bmi_features(self):
        """Create BMI derived features"""
        print("\n=== Creating BMI Features ===")
        
        # BMI Category
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
        
        # BMI deviation from normal range (18.5-24.9)
        self.df['BMI_Deviation'] = self.df['BMI'].apply(lambda x:
            0 if (18.5 <= x <= 24.9) else
            abs(x - 21.5)  # Deviation from center of normal range
        )
        
        # One-hot encoding for BMI category
        bmi_dummies = pd.get_dummies(self.df['BMI_Category'], prefix='BMI')
        self.df = pd.concat([self.df, bmi_dummies], axis=1)
        
        print(f"BMI Category distribution:\n{self.df['BMI_Category'].value_counts()}")
        
        return self.df
    
    def create_metabolic_features(self):
        """Create metabolic health indicators"""
        print("\n=== Creating Metabolic Features ===")
        
        # Glucose-to-BMI ratio (indicator of metabolic stress)
        self.df['Glucose_BMI_Ratio'] = (self.df['Glucose'] / (self.df['BMI'] + 1)).round(2)
        
        # Metabolic health score
        self.df['Metabolic_Health'] = (
            (125 - self.df['Glucose']) / 125 * 50 +
            (100 - abs(self.df['BMI'] - 22)) / 100 * 50
        )
        self.df['Metabolic_Health'] = np.clip(self.df['Metabolic_Health'], 0, 100)
        
        print(f"Metabolic Health Score - Mean: {self.df['Metabolic_Health'].mean():.2f}")
        
        return self.df
    
    def create_cardiovascular_features(self):
        """Create cardiovascular health indicators"""
        print("\n=== Creating Cardiovascular Features ===")
        
        # Cardiovascular risk score
        self.df['Cardiovascular_Risk'] = (
            (self.df['Blood_Pressure'] / 300) * 50 +
            (self.df['Age'] / 100) * 30 +
            abs(self.df['BMI'] - 22) / 22 * 20
        )
        self.df['Cardiovascular_Risk'] = np.clip(self.df['Cardiovascular_Risk'], 0, 100)
        
        # BP ratio indicator
        self.df['Hypertension_Risk'] = (self.df['Blood_Pressure'] > 140).astype(int)
        
        print(f"Cardiovascular Risk - Mean: {self.df['Cardiovascular_Risk'].mean():.2f}")
        
        return self.df
    
    def create_disease_risk_encoding(self):
        """Encode disease risk categories"""
        print("\n=== Encoding Disease Risk ===")
        
        disease_risk_priority_map = {
            'Normal': 1,
            'Asthma': 2,
            'Hypertension': 3,
            'Diabetes': 4,
            'Heart Risk': 5
        }
        
        self.df['Disease_Risk_Priority'] = self.df['Disease_Risk'].map(disease_risk_priority_map)
        
        # One-hot encoding for disease risk
        disease_dummies = pd.get_dummies(self.df['Disease_Risk'], prefix='Disease')
        self.df = pd.concat([self.df, disease_dummies], axis=1)
        
        print(f"Disease Risk encoding complete")
        
        return self.df
    
    def encode_categorical_features(self):
        """Encode remaining categorical features"""
        print("\n=== Encoding Categorical Features ===")
        
        # Encode City
        le_city = LabelEncoder()
        self.df['City_Encoded'] = le_city.fit_transform(self.df['City'])
        
        # Create city distribution features
        city_dummies = pd.get_dummies(self.df['City'], prefix='City')
        self.df = pd.concat([self.df, city_dummies], axis=1)
        
        print(f"City encoding complete - {len(le_city.classes_)} unique cities")
        
        return self.df
    
    def create_interaction_features(self):
        """Create interaction features"""
        print("\n=== Creating Interaction Features ===")
        
        # Age-BMI interaction (risk increases significantly when both high)
        self.df['Age_BMI_Interaction'] = (self.df['Age'] * self.df['BMI']) / 1000
        
        # BP-Glucose interaction
        self.df['BP_Glucose_Interaction'] = (self.df['Blood_Pressure'] * self.df['Glucose']) / 10000
        
        # Combined metabolic stress
        self.df['Metabolic_Stress'] = (
            (self.df['BMI'] - 22) ** 2 +
            (self.df['Glucose'] - 100) ** 2 / 100
        )
        
        print(f"Interaction features created")
        
        return self.df
    
    def calculate_kpis(self):
        """Calculate Key Performance Indicators"""
        print("\n=== CALCULATING KPIS ===")
        
        # Overall Health Metrics
        self.kpis['overall_metrics'] = {
            'total_patients': len(self.df),
            'average_age': round(self.df['Age'].mean(), 2),
            'average_bmi': round(self.df['BMI'].mean(), 2),
            'average_blood_pressure': round(self.df['Blood_Pressure'].mean(), 2),
            'average_glucose': round(self.df['Glucose'].mean(), 2),
        }
        
        # Health Score KPIs
        self.kpis['health_score_kpis'] = {
            'average_health_score': round(self.df['Health_Score'].mean(), 2),
            'patients_excellent_health': len(self.df[self.df['Health_Score'] >= 75]),
            'patients_good_health': len(self.df[(self.df['Health_Score'] >= 50) & (self.df['Health_Score'] < 75)]),
            'patients_poor_health': len(self.df[self.df['Health_Score'] < 50]),
        }
        
        # Risk Score KPIs
        self.kpis['risk_score_kpis'] = {
            'average_risk_score': round(self.df['Risk_Score'].mean(), 2),
            'high_risk_patients': len(self.df[self.df['Risk_Score'] >= 60]),
            'medium_risk_patients': len(self.df[(self.df['Risk_Score'] >= 30) & (self.df['Risk_Score'] < 60)]),
            'low_risk_patients': len(self.df[self.df['Risk_Score'] < 30]),
        }
        
        # Disease-specific KPIs
        self.kpis['disease_kpis'] = {
            'heart_risk_patients': len(self.df[self.df['Disease_Risk'] == 'Heart Risk']),
            'diabetes_patients': len(self.df[self.df['Disease_Risk'] == 'Diabetes']),
            'hypertension_patients': len(self.df[self.df['Disease_Risk'] == 'Hypertension']),
            'asthma_patients': len(self.df[self.df['Disease_Risk'] == 'Asthma']),
            'normal_health_patients': len(self.df[self.df['Disease_Risk'] == 'Normal']),
        }
        
        # Cardiovascular Health KPIs
        self.kpis['cardiovascular_kpis'] = {
            'average_cardiovascular_risk': round(self.df['Cardiovascular_Risk'].mean(), 2),
            'hypertension_risk_patients': len(self.df[self.df['Hypertension_Risk'] == 1]),
        }
        
        # Metabolic Health KPIs
        self.kpis['metabolic_kpis'] = {
            'average_metabolic_health': round(self.df['Metabolic_Health'].mean(), 2),
            'patients_with_good_metabolism': len(self.df[self.df['Metabolic_Health'] >= 70]),
            'patients_with_poor_metabolism': len(self.df[self.df['Metabolic_Health'] < 50]),
        }
        
        # BMI Distribution KPIs
        bmi_dist = self.df['BMI_Category'].value_counts()
        self.kpis['bmi_distribution'] = bmi_dist.to_dict()
        
        # Age Group Distribution KPIs
        age_dist = self.df['Age_Group'].value_counts()
        self.kpis['age_group_distribution'] = age_dist.to_dict()
        
        # City Distribution KPIs (top 5)
        city_dist = self.df['City'].value_counts().head(5)
        self.kpis['city_distribution_top5'] = city_dist.to_dict()
        
        # Print KPIs
        print("\n--- Overall Metrics ---")
        for key, val in self.kpis['overall_metrics'].items():
            print(f"{key}: {val}")
        
        print("\n--- Health Score KPIs ---")
        for key, val in self.kpis['health_score_kpis'].items():
            print(f"{key}: {val}")
        
        print("\n--- Risk Score KPIs ---")
        for key, val in self.kpis['risk_score_kpis'].items():
            print(f"{key}: {val}")
        
        return self.kpis
    
    def engineer_features(self):
        """Execute full feature engineering pipeline"""
        print("="*60)
        print("HEALTHCARE FEATURE ENGINEERING & KPI CREATION")
        print("="*60)
        
        self.load_data()
        self.create_health_score()
        self.create_risk_score()
        self.create_age_group_features()
        self.create_bmi_features()
        self.create_metabolic_features()
        self.create_cardiovascular_features()
        self.create_disease_risk_encoding()
        self.encode_categorical_features()
        self.create_interaction_features()
        self.calculate_kpis()
        
        print("\n" + "="*60)
        print("FEATURE ENGINEERING COMPLETE")
        print("="*60)
        print(f"Final dataset shape: {self.df.shape}")
        print(f"New features created: {self.df.shape[1] - 8}")  # 8 original columns
        
        return self.df
    
    def save_engineered_data(self, output_path):
        """Save engineered dataset"""
        self.df.to_csv(output_path, index=False)
        print(f"\nEngineered data saved to: {output_path}")
        return output_path
    
    def save_kpi_report(self, output_path):
        """Save KPI report as JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.kpis, f, indent=2)
        print(f"KPI report saved to: {output_path}")
        return output_path
    
    def get_feature_summary(self):
        """Get summary of all engineered features"""
        summary = {
            'original_features': ['Patient_ID', 'Name', 'Age', 'BMI', 'Blood_Pressure', 'Glucose', 'Disease_Risk', 'City'],
            'engineered_features': list(self.df.columns[8:]),
            'total_features': len(self.df.columns),
            'feature_info': self.feature_info
        }
        return summary


if __name__ == "__main__":
    # Initialize feature engineering
    data_path = Path(__file__).parent.parent / "data" / "healthcare_data_cleaned.csv"
    fe = HealthcareFeatureEngineering(str(data_path))
    
    # Engineer features
    engineered_df = fe.engineer_features()
    
    # Save results
    output_path = Path(__file__).parent.parent / "data" / "healthcare_data_engineered.csv"
    fe.save_engineered_data(str(output_path))
    
    kpi_path = Path(__file__).parent.parent / "data" / "kpi_report.json"
    fe.save_kpi_report(str(kpi_path))
    
    # Display feature summary
    print("\n=== FEATURE ENGINEERING SUMMARY ===")
    summary = fe.get_feature_summary()
    print(f"Original Features: {len(summary['original_features'])}")
    print(f"Engineered Features: {len(summary['engineered_features'])}")
    print(f"Total Features: {summary['total_features']}")
