# Power BI Dashboard Specification

## Dataset
Use `data/interview_powerbi_source.csv`.

## Page 1 — Executive Overview
Visuals:
- Card: Avg Performance Score
- Card: Avg Confidence Score
- Card: Avg Interviewer Rating
- Card: Offer Rate
- Clustered bar chart: Performance Category by Position Applied
- Donut chart: Offer_Extended split

Fields:
- `Performance_Score_Proxy`
- `Confidence_Score`
- `Interviewer_Rating`
- `Offer_Extended`
- `Position_Applied`
- `Performance_Category`

## Page 2 — Technical Performance
Visuals:
- Scatter: Coding_Test_Score vs Performance_Score_Proxy
- Bar: Technical_Questions_Answered by Position Applied
- Histogram: Coding_Test_Score

## Page 3 — Soft Skills
Visuals:
- Scatter: Confidence_Score vs Interviewer_Rating
- Scatter: Filler_Words_Used vs Performance_Score_Proxy
- Bar: Eye_Contact_Score and Body_Language_Score by Interview_Round

## Page 4 — Interview Logistics
Visuals:
- Bar: Network_Stability_Score by Interview_Mode
- Bar: Microphone_Clarity by Performance_Category
- Bar: Background_Noise_Level by Performance_Category
- Scatter: Duration_Minutes vs Performance_Score_Proxy

## Recommended slicers
- Position_Applied
- Industry
- Interview_Round
- Interview_Mode
- Gender
- Education_Level

## DAX
See `powerbi/measures.dax`.
