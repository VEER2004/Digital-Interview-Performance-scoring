"""
Model Retraining Example
Demonstrates how to retrain the model with new data
"""

from pathlib import Path
import json
import subprocess
import pandas as pd
from datetime import datetime

def retrain_model(data_path=None):
    """
    Retrain the model with new data
    
    Args:
        data_path: Path to new training CSV (default: uses existing)
    
    Returns:
        dict: New model metrics
    """
    
    print("\n" + "="*60)
    print("🔄 MODEL RETRAINING PROCESS")
    print("="*60)
    
    # Step 1: Verify data
    print("\n📊 STEP 1: Verifying Data")
    print("-" * 60)
    
    if data_path is None:
        data_path = Path(__file__).parent / "data" / "interview_training_source.csv"
    
    data_path = Path(data_path)
    
    if not data_path.exists():
        print(f"❌ Error: Data file not found at {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"✅ Data loaded: {len(df)} records")
    print(f"✅ Columns: {len(df.columns)} features")
    
    # Required columns
    required_cols = [
        'Age', 'Gender', 'Education_Level', 'Position_Applied', 'Industry',
        'Interview_Round', 'Interview_Mode', 'Duration_Minutes', 'Camera_On',
        'Microphone_Clarity', 'Network_Stability_Score', 'Technical_Questions_Answered',
        'Behavioral_Questions_Answered', 'Coding_Test_Score', 'Eye_Contact_Score',
        'Body_Language_Score', 'Speech_Speed_WPM', 'Filler_Words_Used',
        'Confidence_Score', 'Response_Relevance_Score', 'Interviewer_Rating',
        'Background_Noise_Level', 'Follow_Up_Questions_Asked', 'Dressing_Appropriateness',
        'Time_Management_Score', 'Performance_Score_Proxy'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"❌ Error: Missing columns: {missing_cols}")
        return None
    
    print(f"✅ All {len(required_cols)} required features present")
    
    # Check for missing values
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"⚠️  Warning: {null_count} null values found")
    else:
        print("✅ No missing values")
    
    # Step 2: Show data statistics
    print("\n📈 STEP 2: Data Statistics")
    print("-" * 60)
    print(f"Performance Score Range: {df['Performance_Score_Proxy'].min():.1f} - {df['Performance_Score_Proxy'].max():.1f}")
    print(f"Average Performance: {df['Performance_Score_Proxy'].mean():.2f}")
    print(f"Confidence Range: {df['Confidence_Score'].min():.1f} - {df['Confidence_Score'].max():.1f}")
    print(f"Average Confidence: {df['Confidence_Score'].mean():.2f}")
    
    # Step 3: Train model
    print("\n🔨 STEP 3: Training Model")
    print("-" * 60)
    print("Running: python -m src.train")
    
    try:
        result = subprocess.run(
            ["python", "-m", "src.train"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ Training failed: {result.stderr}")
            return None
        
        print("✅ Training completed successfully")
        
    except subprocess.TimeoutExpired:
        print("❌ Training timed out (exceeded 5 minutes)")
        return None
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        return None
    
    # Step 4: Load new metrics
    print("\n📊 STEP 4: Loading New Metrics")
    print("-" * 60)
    
    metrics_path = Path(__file__).parent / "artifacts" / "model_metrics.json"
    
    if not metrics_path.exists():
        print("❌ Metrics file not found")
        return None
    
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    # Step 5: Display results
    print("\n✅ STEP 5: Results")
    print("-" * 60)
    
    best_model = metrics.get('best_model', 'Unknown')
    holdout_metrics = metrics.get('holdout', {})
    
    print(f"Best Model: {best_model}")
    print(f"R² Score: {holdout_metrics.get('r2', 'N/A'):.4f}")
    print(f"MAE: {holdout_metrics.get('mae', 'N/A'):.4f}")
    print(f"RMSE: {holdout_metrics.get('rmse', 'N/A'):.4f}")
    print(f"Train Size: {metrics.get('train_rows', 'N/A')} records")
    print(f"Test Size: {metrics.get('test_rows', 'N/A')} records")
    
    # Step 6: Log the result
    print("\n📝 STEP 6: Logging Result")
    print("-" * 60)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data_file": str(data_path),
        "records": len(df),
        "best_model": best_model,
        "r2": holdout_metrics.get('r2'),
        "mae": holdout_metrics.get('mae'),
        "rmse": holdout_metrics.get('rmse'),
        "status": "success"
    }
    
    log_file = Path(__file__).parent / "model_retraining_log.json"
    
    # Append to log
    logs = []
    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"✅ Logged to: {log_file}")
    
    # Step 7: Summary
    print("\n" + "="*60)
    print("🎉 RETRAINING COMPLETE")
    print("="*60)
    print(f"\n✅ Your model has been successfully retrained!")
    print(f"\n📂 Updated Files:")
    print(f"   • artifacts/best_interview_performance_model.joblib")
    print(f"   • artifacts/model_metrics.json")
    print(f"   • artifacts/model_metadata.json")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Refresh Streamlit app (http://localhost:8501)")
    print(f"   2. Check new predictions")
    print(f"   3. Monitor performance over time")
    
    return metrics


def compare_models(model_name_1="v1", metrics_1=None, model_name_2="v2", metrics_2=None):
    """
    Compare two model versions
    """
    print("\n" + "="*60)
    print("📊 MODEL COMPARISON")
    print("="*60)
    
    print(f"\n{'Metric':<20} {'Model 1':<15} {'Model 2':<15} {'Change':<10}")
    print("-" * 60)
    
    if metrics_1 and metrics_2:
        h1 = metrics_1.get('holdout', {})
        h2 = metrics_2.get('holdout', {})
        
        # R² Score
        r2_1 = h1.get('r2', 0)
        r2_2 = h2.get('r2', 0)
        change = ((r2_2 - r2_1) / r2_1 * 100) if r2_1 else 0
        print(f"{'R² Score':<20} {r2_1:<15.4f} {r2_2:<15.4f} {change:+.2f}%")
        
        # MAE
        mae_1 = h1.get('mae', 0)
        mae_2 = h2.get('mae', 0)
        change = ((mae_2 - mae_1) / mae_1 * 100) if mae_1 else 0
        print(f"{'MAE':<20} {mae_1:<15.4f} {mae_2:<15.4f} {change:+.2f}%")
        
        # RMSE
        rmse_1 = h1.get('rmse', 0)
        rmse_2 = h2.get('rmse', 0)
        change = ((rmse_2 - rmse_1) / rmse_1 * 100) if rmse_1 else 0
        print(f"{'RMSE':<20} {rmse_1:<15.4f} {rmse_2:<15.4f} {change:+.2f}%")
        
        print("\n✅ Recommendation:")
        if r2_2 > r2_1:
            print(f"   Model 2 is better (+{(r2_2-r2_1)*100:.2f}% improvement)")
        elif r2_2 < r2_1:
            print(f"   Model 1 is better (+{(r2_1-r2_2)*100:.2f}% improvement)")
        else:
            print("   Models are equivalent")


if __name__ == "__main__":
    # Example: Retrain with default data
    print("\n🚀 Starting Model Retraining Demo\n")
    
    # Option 1: Retrain with existing data
    metrics = retrain_model()
    
    # Option 2: Retrain with new data
    # metrics = retrain_model("data/interview_training_source_new.csv")
    
    # Option 3: Compare models (if you have both)
    # old_metrics = {...}  # Load old metrics
    # compare_models("Old Model", old_metrics, "New Model", metrics)
    
    print("\n✅ Demo complete!")
