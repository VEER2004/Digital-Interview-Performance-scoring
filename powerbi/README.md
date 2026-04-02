# Power BI Dashboard Pack

Use `data/interview_powerbi_source.csv` as the main table.

## Suggested pages
### 1. Executive Overview
- Cards: Avg Performance Score, Avg Interviewer Rating, Avg Confidence Score, Offer Rate
- Bar chart: Performance Category by Position Applied
- Donut chart: Offer_Extended split
- KPI cards: Excellent / Good / Needs Improvement counts

### 2. Technical Performance
- Scatter: Coding Test Score vs Performance Score
- Bar: Technical Questions Answered by Position Applied
- Histogram: Coding Test Score distribution

### 3. Soft Skills
- Scatter: Confidence Score vs Interviewer Rating
- Scatter: Filler Words Used vs Performance Score
- Bar: Eye Contact and Body Language averages by Interview Round

### 4. Logistics & Interview Conditions
- Network Stability by Interview Mode
- Microphone Clarity vs Performance Score
- Background Noise Level vs Performance Score
- Duration Minutes vs Performance Score

## DAX
See `powerbi/measures.dax`.

## Theme
See `powerbi/theme.json`.