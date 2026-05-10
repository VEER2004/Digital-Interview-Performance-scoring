import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda():
    data_path = "virtual_interview_with_target.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return
        
    df = pd.read_csv(data_path)
    print("Running Exploratory Data Analysis (EDA)...")
    
    # Create directory for plots
    os.makedirs("eda_plots", exist_ok=True)
    
    # 1. Distribution plots
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Final Interview Performance Score'], bins=20, kde=True)
    plt.title("Distribution of Final Interview Performance Score")
    plt.savefig("eda_plots/distribution_final_score.png")
    plt.close()
    
    # 2. Correlation heatmap
    plt.figure(figsize=(14, 10))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap")
    plt.savefig("eda_plots/correlation_heatmap.png")
    plt.close()
    
    # 3. Feature importance insight (using correlation with target)
    plt.figure(figsize=(10, 6))
    feature_importance = corr['Final Interview Performance Score'].drop('Final Interview Performance Score').sort_values(ascending=False)
    sns.barplot(x=feature_importance.values, y=feature_importance.index, palette="viridis")
    plt.title("Feature Correlation with Final Performance (Feature Importance Insight)")
    plt.savefig("eda_plots/feature_importance.png")
    plt.close()
    
    # 4. Relationship between technical score & final performance
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Coding Test Score', y='Final Interview Performance Score', data=df)
    plt.title("Coding Test Score vs Final Performance")
    plt.savefig("eda_plots/coding_vs_final.png")
    plt.close()
    
    # 5. Impact of filler words on performance
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Filler Words Used', y='Confidence Score', data=df)
    plt.title("Filler Words vs Confidence Score")
    plt.savefig("eda_plots/filler_vs_confidence.png")
    plt.close()
    
    print("EDA completed! Plots saved in 'eda_plots' directory.")
    
if __name__ == "__main__":
    run_eda()
