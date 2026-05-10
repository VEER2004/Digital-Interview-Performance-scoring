import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def main():
    print("--- Digital Interview Performance Scoring Workflow ---")
    
    # 1. Data Collection
    data_path = "virtual_interview_with_target.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run data_generator.py first.")
        return
    
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully.")
    
    # 2. Data Preprocessing
    # Check missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Feature & Target Selection
    target_col = 'Final Interview Performance Score'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature Scaling (Optional Enhancements as per document)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for Streamlit app
    joblib.dump(scaler, "scaler.pkl")
    
    # 3. Model Selection & Training
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(random_state=42),
        "Ada Boost Regressor": AdaBoostRegressor(random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
        "Ensemble (Voting)": VotingRegressor(estimators=[
            ('lr', LinearRegression()),
            ('rf', RandomForestRegressor(random_state=42)),
            ('gb', GradientBoostingRegressor(random_state=42))
        ])
    }
    
    best_model_name = None
    best_model = None
    best_r2 = -float('inf')
    
    print("\nEvaluating Models:")
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        
        print(f"[{name}] MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model = model
            
    print(f"\nBest Model Selected: {best_model_name} with R2: {best_r2:.2f}")
            
    # 4. Model Saving
    if best_model is not None:
        joblib.dump(best_model, "best_interview_performance_model.pkl")
        print("\nModel saved as best_interview_performance_model.pkl")
        
        # Save feature columns to ensure consistency in web app
        joblib.dump(X.columns.tolist(), "feature_columns.pkl")
    
    print("Training pipeline completed successfully.")

if __name__ == "__main__":
    main()
