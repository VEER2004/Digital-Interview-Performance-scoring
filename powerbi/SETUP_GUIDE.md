# 📊 Power BI Dashboard Setup Guide

## Complete Configuration & Formulas

### Data Source
- **File**: `data/interview_powerbi_source.csv`
- **Rows**: 2,000 interview records
- **Columns**: 32 data fields

---

## Step 1: Import Data into Power BI

1. Open **Power BI Desktop**
2. Click **Home** → **Get Data** → **Text/CSV**
3. Select: `interview_powerbi_source.csv`
4. Click **Load**
5. In the **Data** tab, verify all columns are loaded

---

## Step 2: Data Modeling

### Create Calculated Column: Performance Category

**Location**: Data tab → Right-click table → New Column

**Formula**:
```dax
Performance Category = 
IF([Performance_Score_Proxy] >= 20, "Excellent",
   IF([Performance_Score_Proxy] >= 12, "Good",
      "Needs Improvement"))
```

---

## Step 3: Dashboard Visualizations

### Page Layout
- Page Size: 16:9 Widescreen
- Theme: Dark
- Background: #1a1a1a

---

### Visual 1: KPI - Average Performance Score

**Type**: Card  
**Location**: Top-left  
**Size**: 300×150px

**Configuration**:
- Field: `Performance_Score_Proxy` (Sum)
- Then change to **Average**
- Format: Number, 2 decimal places
- Title Color: White
- Value Color: #00D7FF (Cyan)

**Display**:
- Title: "Avg Performance Score"
- Shows: 15.2 (example value)

---

### Visual 2: KPI - Average Confidence Score

**Type**: Card  
**Location**: Top-center  
**Size**: 300×150px

**Configuration**:
- Field: `Confidence_Score` (Average)
- Format: Number, 1 decimal place
- Title Color: White
- Value Color: #FFD700 (Gold)

**Display**:
- Title: "Avg Confidence"
- Shows: 5.3 (example value)

---

### Visual 3: KPI - Total Candidates Interviewed

**Type**: Card  
**Location**: Top-right  
**Size**: 300×150px

**Configuration**:
- Field: `Candidate_ID` (Count)
- Format: Number, whole number
- Title Color: White
- Value Color: #00FF7F (Spring Green)

**Display**:
- Title: "Total Candidates"
- Shows: 2,000

---

### Visual 4: Performance Distribution (Pie Chart)

**Type**: Pie Chart  
**Location**: Left side, below KPIs  
**Size**: 500×400px

**Configuration**:
- Legend: `Performance Category`
- Values: Count of `Candidate_ID` (or `Performance_Score_Proxy` Sum)
- Colors:
  - Excellent: #00FF7F (Green)
  - Good: #FFD700 (Gold)
  - Needs Improvement: #FF6B6B (Red)

**Features**:
- Show data labels with percentages
- Enable tooltips
- Title: "Performance Distribution"

**Expected Output**:
- Excellent: ~35%
- Good: ~45%
- Needs Improvement: ~20%

---

### Visual 5: Coding Score vs Final Performance (Scatter)

**Type**: Scatter Chart  
**Location**: Right side, below KPIs  
**Size**: 600×400px

**Configuration**:
- X-axis: `Coding_Test_Score` (Average)
- Y-axis: `Performance_Score_Proxy` (Average)
- Legend: `Performance Category`
- Size: `Interviewer_Rating` (optional)

**Features**:
- Color by Performance Category
- Show trend line (Analytics → Trend line)
- Enable tooltips
- Title: "Coding Score vs Final Performance"

**Interpretation**: Shows strong correlation between coding ability and final performance score

---

### Visual 6: Confidence vs Interviewer Rating (Scatter)

**Type**: Scatter Chart  
**Location**: Bottom-left  
**Size**: 600×350px

**Configuration**:
- X-axis: `Confidence_Score` (Average)
- Y-axis: `Interviewer_Rating` (Average)
- Legend: `Performance Category`
- Size: `Response_Relevance_Score`

**Features**:
- Color by Performance Category
- Show trend line with OLS regression
- Title: "Confidence vs Interviewer Rating"

**Interpretation**: Shows how candidate confidence influences interviewer perception

---

### Visual 7: Performance by Position (Bar Chart)

**Type**: Horizontal Bar Chart  
**Location**: Bottom-center  
**Size**: 450×350px

**Configuration**:
- Axis: `Position_Applied`
- Values: `Performance_Score_Proxy` (Average)
- Color: By `Performance Category`

**Features**:
- Sort by average score (descending)
- Show data labels
- Title: "Avg Performance by Position"

**Expected Output**:
- Shows which positions have highest/lowest performance scores
- Helps identify role-specific challenges

---

### Visual 8: Performance by Interview Mode (Column Chart)

**Type**: Column Chart  
**Location**: Bottom-right  
**Size**: 450×350px

**Configuration**:
- X-axis: `Interview_Mode` (Zoom, Skype, Google Meet, In-Person)
- Y-axis: `Performance_Score_Proxy` (Average)
- Color: `Performance Category`

**Features**:
- Show data labels
- Stacked column (by category)
- Title: "Performance by Interview Mode"

**Interpretation**: Compares how interview platform affects performance

---

### Visual 9: Offer Rate by Performance Category (KPI Matrix)

**Type**: Matrix Visual  
**Location**: Can be on separate page  
**Size**: 600×300px

**Configuration**:
- Rows: `Performance Category`
- Values: 
  - Count of Offers: `Offer_Extended` (Count WHERE TRUE)
  - Total: Count of `Candidate_ID`

**Features**:
- Show percentages
- Format as percentage bars

**Display Example**:
| Performance Category | Offers | Total | Offer Rate |
|---|---|---|---|
| Excellent | 630 | 700 | 90% |
| Good | 720 | 900 | 80% |
| Needs Improvement | 50 | 400 | 12% |

---

## Step 4: Formatting & Styling

### Color Scheme
```
Primary: #00D7FF (Cyan)
Success: #00FF7F (Green)
Warning: #FFD700 (Gold)
Danger: #FF6B6B (Red)
Background: #1a1a1a (Dark)
Text: #FFFFFF (White)
```

### Font
- Font Family: Segoe UI
- Title: Bold, 16pt
- Label: Regular, 12pt

### Interactions
- Enable cross-filtering between charts
- Tooltip background: #2a2a2a
- Tooltip text: White

---

## Step 5: Advanced Features (Optional)

### Slicers
Add interactive filters:
1. **Position Applied Slicer** - Dropdown
2. **Interview Mode Slicer** - Buttons
3. **Gender Slicer** - Dropdown
4. **Performance Category Slicer** - Buttons

### Bookmarks
Create dashboard views:
1. **Executive Summary** - KPIs + Distribution
2. **Detailed Analysis** - All charts
3. **Performance Deep Dive** - Scatter charts + Position analysis

### Report Pages
- **Page 1**: Dashboard (overview)
- **Page 2**: Detailed Analysis
- **Page 3**: Hiring Effectiveness

---

## Step 6: Publishing

1. **Save** the Power BI file: `Interview_Performance_Dashboard.pbix`
2. Go to: **File** → **Save as**
3. Location: `powerbi/Interview_Performance_Dashboard.pbix`

4. **Publish to Power BI Service** (Optional):
   - **Home** → **Publish**
   - Select workspace
   - Share link with stakeholders

---

## Key Metrics to Monitor

| Metric | Good Range | Benchmark |
|--------|-----------|-----------|
| Avg Performance Score | 14-16 | 15.2 |
| Avg Confidence | 5-6 | 5.3 |
| Offer Rate (Excellent) | >85% | 90% |
| Offer Rate (Good) | 70-85% | 80% |
| Coding Score Correlation | >0.7 | 0.75 |

---

## Troubleshooting

### Issue: "Performance Category column not found"
**Solution**: 
1. Go to Data tab
2. Create the calculated column using the DAX formula above
3. Refresh the data

### Issue: Charts showing no data
**Solution**:
1. Click chart
2. Check Fields pane
3. Verify correct field names
4. Refresh data (Ctrl+Shift+R)

### Issue: Trend line not appearing
**Solution**:
1. Click chart
2. Analytics pane (right side)
3. Enable "Trend line"
4. Select OLS or other option

---

## Dashboard Export

After completion:
1. **Export report**: File → Export
2. Format: PDF or PowerPoint
3. Share with stakeholders

---

## Performance Optimization

If dashboard is slow:
1. Close unused pages
2. Reduce size of date ranges in slicers
3. Disable unnecessary cross-filters
4. Use **Performance Analyzer**: View → Performance Analyzer

---

Generated: April 2, 2026
Version: 1.0
Status: Ready for Implementation
