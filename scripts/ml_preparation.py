import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class HealthcareMLPreparation:
    """
    ML Model Preparation for Healthcare Risk Prediction
    Prepares data for training, tests baseline models
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.model_results = {}
        
    def load_data(self):
        """Load engineered dataset"""
        self.df = pd.read_csv(self.filepath)
        print(f"Dataset loaded: {self.df.shape}")
        return self.df
    
    def prepare_features_and_target(self):
        """Prepare features and target variable"""
        print("\n=== PREPARING FEATURES AND TARGET ===")
        
        # Define feature columns to use
        feature_cols = [
            'Age', 'BMI', 'Blood_Pressure', 'Glucose',
            'Health_Score', 'Risk_Score',
            'BMI_Deviation', 'Glucose_BMI_Ratio',
            'Metabolic_Health', 'Cardiovascular_Risk',
            'Disease_Risk_Priority',
            'Age_BMI_Interaction', 'BP_Glucose_Interaction', 'Metabolic_Stress',
            'City_Encoded'
        ]
        
        # Select features
        X = self.df[feature_cols].copy()
        
        # Create target variable: High Risk vs Others
        # High Risk if Risk_Score >= 60 or Disease_Risk is 'Heart Risk'
        y = ((self.df['Risk_Score'] >= 60) | (self.df['Disease_Risk'] == 'Heart Risk')).astype(int)
        
        feature_missing = X.isnull().sum()
        if feature_missing.any():
            print(f"Missing values in features:\n{feature_missing[feature_missing > 0]}")
            X.fillna(X.median(), inplace=True)
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        print(f"Target class balance: {y.value_counts(normalize=True).round(4)}")
        
        self.X = X
        self.y = y
        
        return X, y
    
    def handle_class_imbalance(self):
        """Handle class imbalance if present"""
        print("\n=== HANDLING CLASS IMBALANCE ===")
        
        class_balance = (self.y.sum() / len(self.y)) * 100
        print(f"High-risk samples: {self.y.sum()} ({class_balance:.2f}%)")
        
        # Calculate class weights for imbalanced data
        n_samples = len(self.y)
        n_positive = self.y.sum()
        n_negative = n_samples - n_positive
        
        weight_positive = n_samples / (2 * n_positive) if n_positive > 0 else 1
        weight_negative = n_samples / (2 * n_negative) if n_negative > 0 else 1
        
        self.class_weights = {0: weight_negative, 1: weight_positive}
        print(f"Class weights: 0={self.class_weights[0]:.3f}, 1={self.class_weights[1]:.3f}")
        
        return self.class_weights
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        print("\n=== SPLITTING DATA ===")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state,
            stratify=self.y  # Maintain class balance in splits
        )
        
        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")
        print(f"Training set class distribution:\n{self.y_train.value_counts()}")
        print(f"Test set class distribution:\n{self.y_test.value_counts()}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def scale_features(self):
        """Scale numeric features"""
        print("\n=== SCALING FEATURES ===")
        
        # Fit scaler on training data
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Convert back to DataFrame for reference
        self.X_train_scaled_df = pd.DataFrame(
            self.X_train_scaled,
            columns=self.X_train.columns,
            index=self.X_train.index
        )
        self.X_test_scaled_df = pd.DataFrame(
            self.X_test_scaled,
            columns=self.X_test.columns,
            index=self.X_test.index
        )
        
        print(f"Features scaled using StandardScaler")
        print(f"Training set - Mean: {self.X_train_scaled.mean():.4f}, Std: {self.X_train_scaled.std():.4f}")
        print(f"Test set - Mean: {self.X_test_scaled.mean():.4f}, Std: {self.X_test_scaled.std():.4f}")
        
        return self.X_train_scaled, self.X_test_scaled
    
    def train_baseline_models(self):
        """Train baseline ML models for risk prediction"""
        print("\n=== TRAINING BASELINE MODELS ===")
        
        models = {}
        results = {}
        
        # Model 1: Logistic Regression
        print("\n--- Logistic Regression ---")
        lr_model = LogisticRegression(
            class_weight='balanced',
            max_iter=1000,
            random_state=42
        )
        lr_model.fit(self.X_train_scaled, self.y_train)
        lr_pred = lr_model.predict(self.X_test_scaled)
        lr_pred_proba = lr_model.predict_proba(self.X_test_scaled)[:, 1]
        
        lr_accuracy = accuracy_score(self.y_test, lr_pred)
        print(f"Accuracy: {lr_accuracy:.4f}")
        print(f"Classification Report:\n{classification_report(self.y_test, lr_pred)}")
        
        models['logistic_regression'] = lr_model
        results['logistic_regression'] = {
            'accuracy': float(lr_accuracy),
            'predictions': lr_pred.tolist(),
            'probabilities': lr_pred_proba.tolist(),
            'feature_importance': dict(zip(self.X_train.columns, lr_model.coef_[0]))
        }
        
        # Model 2: Random Forest
        print("\n--- Random Forest ---")
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        rf_model.fit(self.X_train_scaled, self.y_train)
        rf_pred = rf_model.predict(self.X_test_scaled)
        rf_pred_proba = rf_model.predict_proba(self.X_test_scaled)[:, 1]
        
        rf_accuracy = accuracy_score(self.y_test, rf_pred)
        print(f"Accuracy: {rf_accuracy:.4f}")
        print(f"Classification Report:\n{classification_report(self.y_test, rf_pred)}")
        
        # Feature importance
        feature_importance = dict(zip(self.X_train.columns, rf_model.feature_importances_))
        feature_importance_sorted = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
        print(f"\nTop 10 Important Features:")
        for i, (feat, imp) in enumerate(list(feature_importance_sorted.items())[:10], 1):
            print(f"{i}. {feat}: {imp:.4f}")
        
        models['random_forest'] = rf_model
        results['random_forest'] = {
            'accuracy': float(rf_accuracy),
            'predictions': rf_pred.tolist(),
            'probabilities': rf_pred_proba.tolist(),
            'feature_importance': feature_importance_sorted
        }
        
        self.models = models
        self.model_results = results
        
        print(f"\n--- Model Comparison ---")
        print(f"Logistic Regression Accuracy: {lr_accuracy:.4f}")
        print(f"Random Forest Accuracy: {rf_accuracy:.4f}")
        print(f"Best Model: {'Random Forest' if rf_accuracy > lr_accuracy else 'Logistic Regression'}")
        
        return models, results
    
    def get_model_prediction_example(self, model_name='random_forest', sample_size=10):
        """Get example predictions with probabilities"""
        print(f"\n=== EXAMPLE PREDICTIONS ({model_name.upper()}) ===")
        
        model = self.models[model_name]
        probabilities = self.model_results[model_name]['probabilities']
        predictions = self.model_results[model_name]['predictions']
        
        # Select sample indices
        sample_indices = np.random.choice(len(self.y_test), min(sample_size, len(self.y_test)), replace=False)
        
        examples = []
        for idx in sample_indices:
            test_idx = self.y_test.index[idx] if hasattr(self.y_test, 'index') else idx
            example = {
                'patient_id': self.df.loc[test_idx, 'Patient_ID'] if test_idx < len(self.df) else None,
                'actual_risk': int(self.y_test.iloc[idx]),
                'predicted_risk': int(predictions[idx]),
                'risk_probability': float(probabilities[idx]),
                'correct_prediction': predictions[idx] == self.y_test.iloc[idx]
            }
            examples.append(example)
        
        return examples
    
    def prepare_ml_dataset(self):
        """Execute full ML preparation pipeline"""
        print("="*60)
        print("HEALTHCARE ML DATA PREPARATION")
        print("="*60)
        
        self.load_data()
        self.prepare_features_and_target()
        self.handle_class_imbalance()
        self.split_data()
        self.scale_features()
        self.train_baseline_models()
        
        print("\n" + "="*60)
        print("ML PREPARATION COMPLETE")
        print("="*60)
        
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def save_preparation_report(self, output_path):
        """Save ML preparation report"""
        report = {
            'dataset_info': {
                'total_samples': len(self.df),
                'feature_count': len(self.X.columns),
                'target_variable': 'High Risk (1) vs Low Risk (0)'
            },
            'train_test_split': {
                'train_size': len(self.X_train),
                'test_size': len(self.X_test),
                'train_positive_class': int(self.y_train.sum()),
                'test_positive_class': int(self.y_test.sum())
            },
            'class_weights': self.class_weights,
            'model_results': self.model_results,
            'features_used': list(self.X.columns)
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nML preparation report saved to: {output_path}")
        return output_path
    
    def save_training_data(self, output_dir):
        """Save training data in different formats"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save scaled training data
        train_data = pd.DataFrame(
            self.X_train_scaled,
            columns=self.X_train.columns
        )
        train_data['target'] = self.y_train.values
        train_data.to_csv(output_path / "train_scaled.csv", index=False)
        
        # Save scaled test data
        test_data = pd.DataFrame(
            self.X_test_scaled,
            columns=self.X_test.columns
        )
        test_data['target'] = self.y_test.values
        test_data.to_csv(output_path / "test_scaled.csv", index=False)
        
        print(f"\nTraining data saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    # Initialize ML preparation
    data_path = Path(__file__).parent.parent / "data" / "healthcare_data_engineered.csv"
    ml_prep = HealthcareMLPreparation(str(data_path))
    
    # Prepare data and train models
    ml_prep.prepare_ml_dataset()
    
    # Save reports
    report_path = Path(__file__).parent.parent / "data" / "ml_preparation_report.json"
    ml_prep.save_preparation_report(str(report_path))
    
    # Save training data
    train_data_dir = Path(__file__).parent.parent / "data" / "ml_training_data"
    ml_prep.save_training_data(str(train_data_dir))
    
    # Get example predictions
    examples = ml_prep.get_model_prediction_example('random_forest', sample_size=5)
    print("\n=== Example Predictions ===")
    for ex in examples:
        print(f"Actual: {ex['actual_risk']}, Predicted: {ex['predicted_risk']}, "
              f"Probability: {ex['risk_probability']:.4f}")
