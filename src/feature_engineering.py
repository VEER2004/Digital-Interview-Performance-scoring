from __future__ import annotations
import numpy as np
import pandas as pd

EDU_MAP = {"Bachelors": 0.55, "Masters": 0.75, "PhD": 0.90}
ROUND_MAP = {"HR": 0.55, "Technical": 0.80, "Managerial": 0.70, "Final": 1.00}
MIC_MAP = {"Poor": 0.30, "Moderate": 0.65, "Clear": 1.00}
NOISE_MAP = {"High": 0.20, "Medium": 0.60, "Low": 1.00}
DRESS_MAP = {"Casual": 0.55, "Semi-Formal": 0.80, "Formal": 1.00}
CAM_MAP = {"No": 0.00, "Yes": 1.00}

def minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    denom = (s.max() - s.min())
    if denom == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / denom

def build_performance_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    score = (
        0.12 * minmax(out["Technical_Questions_Answered"]) +
        0.08 * minmax(out["Behavioral_Questions_Answered"]) +
        0.14 * minmax(out["Coding_Test_Score"]) +
        0.08 * minmax(out["Eye_Contact_Score"]) +
        0.08 * minmax(out["Body_Language_Score"]) +
        0.12 * minmax(out["Confidence_Score"]) +
        0.12 * minmax(out["Response_Relevance_Score"]) +
        0.10 * minmax(out["Interviewer_Rating"]) +
        0.07 * minmax(out["Time_Management_Score"]) +
        0.06 * minmax(out["Network_Stability_Score"]) +
        0.03 * minmax(out["Follow_Up_Questions_Asked"]) +
        0.02 * out["Camera_On"].map(CAM_MAP).astype(float) +
        0.03 * out["Microphone_Clarity"].map(MIC_MAP).astype(float) +
        0.01 * out["Dressing_Appropriateness"].map(DRESS_MAP).astype(float) +
        0.02 * out["Education_Level"].map(EDU_MAP).astype(float) +
        0.02 * out["Interview_Round"].map(ROUND_MAP).astype(float) +
        0.02 * (1 - np.abs(out["Duration_Minutes"] - 40) / 20).clip(0, 1) +
        0.02 * (1 - np.abs(out["Speech_Speed_WPM"] - 120) / 30).clip(0, 1) +
        0.01 * (1 - np.abs(out["Age"] - 27.5) / 12).clip(0, 1)
    ) - (
        0.07 * minmax(out["Filler_Words_Used"]) +
        0.03 * out["Background_Noise_Level"].map(NOISE_MAP).astype(float)
    )
    out["Performance_Score_Proxy"] = (score.clip(0, 1) * 30).round(2)
    out["Performance_Category"] = pd.cut(
        out["Performance_Score_Proxy"],
        bins=[-np.inf, 12, 20, np.inf],
        labels=["Needs Improvement", "Good", "Excellent"]
    ).astype(str)
    return out

def get_feature_columns(df: pd.DataFrame) -> list[str]:
    ignore = {"Candidate_ID", "Start_Time", "End_Time", "Final_Recommendation", "Offer_Extended", "Performance_Score_Proxy", "Performance_Category"}
    return [c for c in df.columns if c not in ignore]

def get_model_inputs(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "Age", "Gender", "Education_Level", "Position_Applied", "Industry", "Interview_Round", "Interview_Mode",
        "Duration_Minutes", "Camera_On", "Microphone_Clarity", "Network_Stability_Score",
        "Technical_Questions_Answered", "Behavioral_Questions_Answered", "Coding_Test_Score",
        "Eye_Contact_Score", "Body_Language_Score", "Speech_Speed_WPM", "Filler_Words_Used",
        "Confidence_Score", "Response_Relevance_Score", "Interviewer_Rating",
        "Background_Noise_Level", "Follow_Up_Questions_Asked", "Dressing_Appropriateness",
        "Time_Management_Score"
    ]
    return df[cols].copy()