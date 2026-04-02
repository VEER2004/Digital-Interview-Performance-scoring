# 📋 Sample New Training Data Template

To retrain your model, create a CSV file with this structure:

## Column Definitions & Sample Values

```csv
Candidate_ID,Age,Gender,Education_Level,Position_Applied,Industry,Interview_Round,Interview_Mode,Duration_Minutes,Camera_On,Microphone_Clarity,Network_Stability_Score,Technical_Questions_Answered,Behavioral_Questions_Answered,Coding_Test_Score,Eye_Contact_Score,Body_Language_Score,Speech_Speed_WPM,Filler_Words_Used,Confidence_Score,Response_Relevance_Score,Interviewer_Rating,Background_Noise_Level,Follow_Up_Questions_Asked,Dressing_Appropriateness,Time_Management_Score,Performance_Score_Proxy

C3001,29,Male,Bachelors,Software Engineer,Tech,HR,Zoom,52,Yes,Good,8.2,8,3,92,6,7,115,1,8,9,4.1,Low,2,Business Casual,8,19.2
C3002,35,Female,Masters,Data Analyst,Finance,Managerial,Teams,48,Yes,Good,9.1,9,4,88,5,6,108,0,7,8,3.8,Low,3,Formal,7,18.7
C3003,26,Male,Bachelors,UI/UX Designer,Tech,HR,Google Meet,42,No,Moderate,6.5,5,2,65,3,4,125,8,5,6,2.9,Medium,1,Casual,5,16.3
C3004,31,Non-binary,PhD,Data Scientist,Healthcare,Managerial,Skype,55,Yes,Excellent,9.5,10,5,98,7,8,105,1,9,9,4.5,Low,4,Formal,9,20.0
C3005,24,Female,Bachelors,Product Manager,Consulting,HR,Zoom,40,Yes,Good,7.8,6,3,78,4,5,110,3,6,7,3.2,Medium,2,Business Casual,6,17.1
```

## Column Explanations

| Column                        | Type    | Range                                  | Notes                                             |
| ----------------------------- | ------- | -------------------------------------- | ------------------------------------------------- |
| Candidate_ID                  | String  | -                                      | Unique identifier (e.g., C3001)                   |
| Age                           | Integer | 21-65                                  | Years old                                         |
| Gender                        | String  | Male/Female/Non-binary                 | Self-reported                                     |
| Education_Level               | String  | Bachelors/Masters/PhD/High School      | Highest achieved                                  |
| Position_Applied              | String  | Various roles                          | Software Engineer, Data Analyst, etc.             |
| Industry                      | String  | Tech/Finance/Healthcare/Consulting     | Business sector                                   |
| Interview_Round               | String  | HR/Managerial/Final                    | Round of interview                                |
| Interview_Mode                | String  | Zoom/Skype/Teams/Google Meet/In-Person | Meeting platform                                  |
| Duration_Minutes              | Integer | 25-120                                 | Interview length                                  |
| Camera_On                     | String  | Yes/No                                 | Video enabled                                     |
| Microphone_Clarity            | String  | Poor/Moderate/Good                     | Audio quality                                     |
| Network_Stability_Score       | Float   | 0-10                                   | Connection quality (0=worst, 10=best)             |
| Technical_Questions_Answered  | Integer | 0-10                                   | Count of questions answered correctly             |
| Behavioral_Questions_Answered | Integer | 0-10                                   | Count of behavioral Qs answered                   |
| Coding_Test_Score             | Integer | 0-100                                  | Test score percentage                             |
| Eye_Contact_Score             | Integer | 0-10                                   | Interviewer assessment                            |
| Body_Language_Score           | Integer | 0-10                                   | Interviewer assessment                            |
| Speech_Speed_WPM              | Integer | 80-160                                 | Words per minute                                  |
| Filler_Words_Used             | Integer | 0-50                                   | Count (um, uh, like, etc.)                        |
| Confidence_Score              | Integer | 1-10                                   | Interviewer assessment                            |
| Response_Relevance_Score      | Integer | 0-10                                   | Relevance to questions (0=irrelevant, 10=perfect) |
| Interviewer_Rating            | Float   | 1-5                                    | Overall rating                                    |
| Background_Noise_Level        | String  | Low/Medium/High                        | Environment quality                               |
| Follow_Up_Questions_Asked     | Integer | 0-10                                   | Questions candidate asked                         |
| Dressing_Appropriateness      | String  | Casual/Business Casual/Formal          | Dress code match                                  |
| Time_Management_Score         | Integer | 0-10                                   | Punctuality & pacing                              |
| Performance_Score_Proxy       | Float   | 0-20                                   | Target variable (calculated value)                |

## How to Calculate Performance_Score_Proxy

This is your target variable. It's a weighted score based on interview performance:

```python
# Formula to calculate Performance_Score_Proxy
Performance_Score_Proxy = (
    (Coding_Test_Score / 100 * 5) +           # 0-5 points
    (Confidence_Score / 10 * 3) +              # 0-3 points
    (Interviewer_Rating / 5 * 4) +             # 0-4 points
    (Technical_Questions_Answered / 10 * 3) + # 0-3 points
    (Response_Relevance_Score / 10 * 3) +     # 0-3 points
    (Time_Management_Score / 10 * 2) +        # 0-2 points
    (1 if Camera_On == 'Yes' else 0) +        # 0-1 point
    (0.5 if Microphone_Clarity == 'Good' else 0)  # 0-0.5 points
)
```

## Preparation Steps

### 1. **Create your data**

- Collect interview data from your HR system
- Ensure all 27 columns are present
- No blank cells (use 0 or appropriate defaults)

### 2. **Save as CSV**

- File: `data/interview_training_source_new.csv`
- Format: UTF-8 encoding
- Delimiter: Comma (,)

### 3. **Validate**

- Minimum 1,000 rows recommended
- Check data types match examples
- Verify ranges

### 4. **Backup existing**

```powershell
Copy-Item data/interview_training_source.csv data/interview_training_source_backup.csv
```

### 5. **Retrain**

```powershell
python -m src.train
```

## Example Python Code to Generate Sample Data

```python
import pandas as pd
import numpy as np
from pathlib import Path

# Create sample training data
np.random.seed(42)
n_records = 2000

data = {
    'Candidate_ID': [f'C{3001+i}' for i in range(n_records)],
    'Age': np.random.randint(22, 60, n_records),
    'Gender': np.random.choice(['Male', 'Female', 'Non-binary'], n_records, p=[0.5, 0.4, 0.1]),
    'Education_Level': np.random.choice(['Bachelors', 'Masters', 'PhD', 'High School'], n_records, p=[0.5, 0.35, 0.1, 0.05]),
    'Position_Applied': np.random.choice(['Software Engineer', 'Data Analyst', 'UI/UX Designer', 'Product Manager'], n_records),
    'Industry': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Consulting'], n_records),
    'Interview_Round': np.random.choice(['HR', 'Managerial', 'Final'], n_records),
    'Interview_Mode': np.random.choice(['Zoom', 'Teams', 'Skype', 'Google Meet'], n_records),
    'Duration_Minutes': np.random.randint(25, 121, n_records),
    'Camera_On': np.random.choice(['Yes', 'No'], n_records, p=[0.85, 0.15]),
    'Microphone_Clarity': np.random.choice(['Poor', 'Moderate', 'Good'], n_records, p=[0.15, 0.35, 0.5]),
    'Network_Stability_Score': np.random.uniform(3, 10, n_records),
    'Technical_Questions_Answered': np.random.randint(0, 11, n_records),
    'Behavioral_Questions_Answered': np.random.randint(0, 6, n_records),
    'Coding_Test_Score': np.random.randint(30, 101, n_records),
    'Eye_Contact_Score': np.random.randint(1, 11, n_records),
    'Body_Language_Score': np.random.randint(1, 11, n_records),
    'Speech_Speed_WPM': np.random.randint(80, 161, n_records),
    'Filler_Words_Used': np.random.randint(0, 31, n_records),
    'Confidence_Score': np.random.randint(1, 11, n_records),
    'Response_Relevance_Score': np.random.randint(1, 11, n_records),
    'Interviewer_Rating': np.random.uniform(1, 5, n_records),
    'Background_Noise_Level': np.random.choice(['Low', 'Medium', 'High'], n_records, p=[0.6, 0.3, 0.1]),
    'Follow_Up_Questions_Asked': np.random.randint(0, 6, n_records),
    'Dressing_Appropriateness': np.random.choice(['Casual', 'Business Casual', 'Formal'], n_records, p=[0.2, 0.5, 0.3]),
    'Time_Management_Score': np.random.randint(1, 11, n_records),
}

# Calculate Performance Score
df = pd.DataFrame(data)
df['Performance_Score_Proxy'] = (
    (df['Coding_Test_Score'] / 100 * 5) +
    (df['Confidence_Score'] / 10 * 3) +
    (df['Interviewer_Rating'] / 5 * 4) +
    (df['Technical_Questions_Answered'] / 10 * 3) +
    (df['Response_Relevance_Score'] / 10 * 3) +
    (df['Time_Management_Score'] / 10 * 2) +
    ((df['Camera_On'] == 'Yes').astype(int)) +
    ((df['Microphone_Clarity'] == 'Good').astype(float) * 0.5)
)

# Save
df.to_csv('data/interview_training_source_new.csv', index=False)
print(f"✅ Created {len(df)} sample records")
print(f"Avg Performance Score: {df['Performance_Score_Proxy'].mean():.2f}")
```

## Validation Checklist

Before retraining, verify:

- [ ] 27 columns present
- [ ] No empty cells
- [ ] Candidate_ID is unique
- [ ] Age: 22-65 range
- [ ] Performance_Score_Proxy: 0-20 range
- [ ] Yes/No values consistent
- [ ] At least 1,000 rows
- [ ] File saved as CSV

## Questions?

See: MODEL_RETRAINING_GUIDE.md for complete instructions
