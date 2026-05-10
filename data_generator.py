import pandas as pd
import numpy as np

def generate_mock_data(n_samples=500):
    np.random.seed(42)
    
    data = {
        'Age': np.random.randint(21, 45, n_samples),
        'Education Score': np.random.randint(1, 10, n_samples),
        'Technical Questions Answered': np.random.randint(0, 10, n_samples),
        'Coding Test Score': np.random.randint(0, 100, n_samples),
        'Behavioural Questions Answered': np.random.randint(0, 10, n_samples),
        'Eye Contact Score': np.random.uniform(1.0, 10.0, n_samples),
        'Confidence Score': np.random.uniform(1.0, 10.0, n_samples),
        'Speech Speed (WPM)': np.random.randint(80, 160, n_samples),
        'Filler Words Used': np.random.randint(0, 30, n_samples),
        'Interviewer Rating': np.random.uniform(1.0, 10.0, n_samples),
        'Time Management Score': np.random.uniform(1.0, 10.0, n_samples),
        'Round Score': np.random.uniform(1.0, 10.0, n_samples),
        'Duration': np.random.randint(15, 60, n_samples),
        'Network Stability': np.random.uniform(1.0, 10.0, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate Target Variable based on a linear combination with some noise
    df['Final Interview Performance Score'] = (
        0.5 * df['Coding Test Score'] / 10 + 
        0.3 * df['Confidence Score'] + 
        0.2 * df['Technical Questions Answered'] + 
        0.2 * df['Behavioural Questions Answered'] + 
        0.1 * df['Eye Contact Score'] - 
        0.05 * df['Filler Words Used'] + 
        0.4 * df['Interviewer Rating'] + 
        np.random.normal(0, 2, n_samples)
    )
    
    # Clip the scores to be somewhat realistic (e.g., max ~30 depending on the combination)
    df['Final Interview Performance Score'] = df['Final Interview Performance Score'].clip(lower=0, upper=30)
    
    df.to_csv('virtual_interview_with_target.csv', index=False)
    print("Mock dataset generated as 'virtual_interview_with_target.csv'")

if __name__ == "__main__":
    generate_mock_data()
