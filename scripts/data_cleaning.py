import pandas as pd
import numpy as np
import json
from pathlib import Path

class HealthcareDataCleaner:
    """
    Data cleaning and preprocessing for Healthcare dataset
    Handles:
    - Missing values
    - Invalid age values (>100)
    - Negative BMI or Glucose values
    - Extreme BP values
    - Data validation and cleaning
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.cleaning_report = {}
        
    def load_data(self):
        """Load dataset from CSV"""
        self.df = pd.read_csv(self.filepath)
        print(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def get_initial_statistics(self):
        """Get initial data quality statistics"""
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_rows': self.df.duplicated().sum(),
            'data_types': self.df.dtypes.astype(str).to_dict()
        }
        self.cleaning_report['initial_stats'] = stats
        return stats
    
    def handle_missing_values(self):
        """
        Handle missing values strategy:
        - Age: Fill with median
        - BMI: Fill with median
        - Blood_Pressure: Fill with median
        - Glucose: Fill with median
        """
        print("\n=== Handling Missing Values ===")
        missing_before = self.df.isnull().sum().to_dict()
        
        numeric_columns = ['Age', 'BMI', 'Blood_Pressure', 'Glucose']
        for col in numeric_columns:
            if col in self.df.columns:
                median_val = self.df[col].median()
                missing_count = self.df[col].isnull().sum()
                if missing_count > 0:
                    self.df[col].fillna(median_val, inplace=True)
                    print(f"  {col}: Filled {missing_count} missing values with median ({median_val:.2f})")
        
        self.cleaning_report['missing_values_handled'] = missing_before
        print(f"Missing values after handling:\n{self.df.isnull().sum()}")
        return self.df
    
    def handle_invalid_ages(self):
        """Remove or fix invalid age values (>100 or <0)"""
        print("\n=== Handling Invalid Ages ===")
        invalid_ages = self.df[(self.df['Age'] > 100) | (self.df['Age'] < 0)]
        print(f"Invalid ages found: {len(invalid_ages)}")
        if len(invalid_ages) > 0:
            print(f"Invalid age records:\n{invalid_ages[['Patient_ID', 'Name', 'Age']]}")
        
        # Remove rows with invalid ages
        before_count = len(self.df)
        self.df = self.df[(self.df['Age'] <= 100) & (self.df['Age'] >= 0)]
        after_count = len(self.df)
        print(f"Removed {before_count - after_count} rows with invalid ages")
        
        self.cleaning_report['invalid_ages_removed'] = before_count - after_count
        self.df.reset_index(drop=True, inplace=True)
        return self.df
    
    def handle_invalid_bmi(self):
        """Remove or fix negative BMI values"""
        print("\n=== Handling Invalid BMI ===")
        invalid_bmi = self.df[self.df['BMI'] < 0]
        print(f"Invalid BMI values found: {len(invalid_bmi)}")
        if len(invalid_bmi) > 0:
            print(f"Invalid BMI records:\n{invalid_bmi[['Patient_ID', 'Name', 'BMI']]}")
        
        # Fill negative BMI with median of valid BMI
        valid_bmi_median = self.df[self.df['BMI'] > 0]['BMI'].median()
        negative_count = len(self.df[self.df['BMI'] < 0])
        self.df.loc[self.df['BMI'] < 0, 'BMI'] = valid_bmi_median
        print(f"Fixed {negative_count} negative BMI values with median ({valid_bmi_median:.2f})")
        
        self.cleaning_report['invalid_bmi_fixed'] = negative_count
        return self.df
    
    def handle_invalid_glucose(self):
        """Remove or fix negative Glucose values"""
        print("\n=== Handling Invalid Glucose ===")
        invalid_glucose = self.df[self.df['Glucose'] < 0]
        print(f"Invalid Glucose values found: {len(invalid_glucose)}")
        if len(invalid_glucose) > 0:
            print(f"Invalid Glucose records:\n{invalid_glucose[['Patient_ID', 'Name', 'Glucose']]}")
        
        # Fill negative glucose with median of valid glucose
        valid_glucose_median = self.df[self.df['Glucose'] > 0]['Glucose'].median()
        negative_count = len(self.df[self.df['Glucose'] < 0])
        self.df.loc[self.df['Glucose'] < 0, 'Glucose'] = valid_glucose_median
        print(f"Fixed {negative_count} negative Glucose values with median ({valid_glucose_median:.2f})")
        
        self.cleaning_report['invalid_glucose_fixed'] = negative_count
        return self.df
    
    def handle_invalid_blood_pressure(self):
        """Handle extreme BP values (BP > 300 or < 80)"""
        print("\n=== Handling Invalid Blood Pressure ===")
        # Normal BP should be around 90-130. Extreme values (>300) are data entry errors
        extreme_bp = self.df[(self.df['Blood_Pressure'] > 300) | (self.df['Blood_Pressure'] < 60)]
        print(f"Extreme BP values found: {len(extreme_bp)}")
        if len(extreme_bp) > 0:
            print(f"Extreme BP records:\n{extreme_bp[['Patient_ID', 'Name', 'Blood_Pressure']]}")
        
        # Fix extreme values with median
        valid_bp_median = self.df[(self.df['Blood_Pressure'] >= 60) & (self.df['Blood_Pressure'] <= 300)]['Blood_Pressure'].median()
        extreme_count = len(self.df[(self.df['Blood_Pressure'] > 300) | (self.df['Blood_Pressure'] < 60)])
        self.df.loc[(self.df['Blood_Pressure'] > 300) | (self.df['Blood_Pressure'] < 60), 'Blood_Pressure'] = valid_bp_median
        print(f"Fixed {extreme_count} extreme BP values with median ({valid_bp_median:.2f})")
        
        self.cleaning_report['invalid_bp_fixed'] = extreme_count
        return self.df
    
    def validate_disease_risk(self):
        """Validate disease risk categories"""
        print("\n=== Validating Disease Risk ===")
        valid_risks = ['Heart Risk', 'Hypertension', 'Diabetes', 'Asthma', 'Normal']
        invalid_risks = self.df[~self.df['Disease_Risk'].isin(valid_risks)]
        print(f"Invalid disease risk values: {len(invalid_risks)}")
        if len(invalid_risks) > 0:
            print(f"Unique invalid values: {invalid_risks['Disease_Risk'].unique()}")
        
        self.cleaning_report['disease_risk_validation'] = len(invalid_risks)
        return self.df
    
    def clean_data(self):
        """Execute full cleaning pipeline"""
        print("="*60)
        print("HEALTHCARE DATA CLEANING PROCESS")
        print("="*60)
        
        self.load_data()
        self.get_initial_statistics()
        self.handle_missing_values()
        self.handle_invalid_ages()
        self.handle_invalid_bmi()
        self.handle_invalid_glucose()
        self.handle_invalid_blood_pressure()
        self.validate_disease_risk()
        
        print("\n" + "="*60)
        print("CLEANING COMPLETE")
        print("="*60)
        print(f"Final dataset: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
        return self.df
    
    def save_cleaned_data(self, output_path):
        """Save cleaned dataset"""
        self.df.to_csv(output_path, index=False)
        print(f"\nCleaned data saved to: {output_path}")
        return output_path
    
    def get_cleaning_report(self):
        """Get detailed cleaning report"""
        return self.cleaning_report


if __name__ == "__main__":
    # Initialize cleaner
    data_path = Path(__file__).parent.parent / "data" / "healthcare_data.csv"
    cleaner = HealthcareDataCleaner(str(data_path))
    
    # Clean data
    cleaned_df = cleaner.clean_data()
    
    # Save cleaned data
    output_path = Path(__file__).parent.parent / "data" / "healthcare_data_cleaned.csv"
    cleaner.save_cleaned_data(str(output_path))
    
    # Save cleaning report
    report_path = Path(__file__).parent.parent / "data" / "cleaning_report.json"
    with open(report_path, 'w') as f:
        json.dump(cleaner.get_cleaning_report(), f, indent=2)
    print(f"Cleaning report saved to: {report_path}")
