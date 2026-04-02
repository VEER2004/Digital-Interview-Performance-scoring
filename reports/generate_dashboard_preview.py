"""
Power BI Dashboard Preview Generator
Creates visualization preview of the interview performance dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set style
plt.style.use('dark_background')
sns.set_palette("husl")

# Load data
data_path = Path(__file__).parent.parent / "data" / "interview_powerbi_source.csv"
df = pd.read_csv(data_path)

# Convert data types
df['Offer_Extended'] = (df['Offer_Extended'] == 'Yes').astype(int)
df['Camera_On'] = (df['Camera_On'] == 'Yes').astype(int)

# Create Performance Category column
df['Performance_Category'] = pd.cut(
    df['Performance_Score_Proxy'],
    bins=[0, 12, 20, 30],
    labels=['Needs Improvement', 'Good', 'Excellent'],
    include_lowest=True
)

# Create dashboard figure with subplots
fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor('#1a1a1a')
fig.suptitle('📊 Interview Performance Analytics Dashboard', fontsize=28, fontweight='bold', y=0.98, color='white')

# Define colors
color_excellent = '#00FF7F'
color_good = '#FFD700'
color_needs_imp = '#FF6B6B'
colors_category = {
    'Excellent': color_excellent,
    'Good': color_good,
    'Needs Improvement': color_needs_imp
}

# Create GridSpec for better layout control
gs = GridSpec(4, 4, figure=fig, hspace=0.45, wspace=0.35, 
              left=0.08, right=0.95, top=0.94, bottom=0.08)

# ===== KPI SECTION (Top Row - Row 0) =====
ax_kpi1 = fig.add_subplot(gs[0, 0])
ax_kpi1.text(0.5, 0.6, f"{df['Performance_Score_Proxy'].mean():.1f}", 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#00D7FF')
ax_kpi1.text(0.5, 0.15, 'Avg Performance Score', 
             ha='center', va='center', fontsize=12, color='white')
ax_kpi1.set_xlim(0, 1)
ax_kpi1.set_ylim(0, 1)
ax_kpi1.axis('off')
ax_kpi1.set_facecolor('#1a1a1a')
ax_kpi1.spines['bottom'].set_color('white')
ax_kpi1.spines['bottom'].set_linewidth(3)

ax_kpi2 = fig.add_subplot(gs[0, 1])
ax_kpi2.text(0.5, 0.6, f"{df['Confidence_Score'].mean():.1f}", 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#FFD700')
ax_kpi2.text(0.5, 0.15, 'Avg Confidence Score', 
             ha='center', va='center', fontsize=12, color='white')
ax_kpi2.set_xlim(0, 1)
ax_kpi2.set_ylim(0, 1)
ax_kpi2.axis('off')
ax_kpi2.set_facecolor('#1a1a1a')
ax_kpi2.spines['bottom'].set_color('white')
ax_kpi2.spines['bottom'].set_linewidth(3)

ax_kpi3 = fig.add_subplot(gs[0, 2])
ax_kpi3.text(0.5, 0.6, f"{len(df)}", 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#00FF7F')
ax_kpi3.text(0.5, 0.15, 'Total Candidates', 
             ha='center', va='center', fontsize=12, color='white')
ax_kpi3.set_xlim(0, 1)
ax_kpi3.set_ylim(0, 1)
ax_kpi3.axis('off')
ax_kpi3.set_facecolor('#1a1a1a')
ax_kpi3.spines['bottom'].set_color('white')
ax_kpi3.spines['bottom'].set_linewidth(3)

ax_kpi4 = fig.add_subplot(gs[0, 3])
offer_rate = (df['Offer_Extended'].sum() / len(df)) * 100
ax_kpi4.text(0.5, 0.6, f"{offer_rate:.1f}%", 
             ha='center', va='center', fontsize=40, fontweight='bold', color='#FF69B4')
ax_kpi4.text(0.5, 0.15, 'Offer Rate', 
             ha='center', va='center', fontsize=12, color='white')
ax_kpi4.set_xlim(0, 1)
ax_kpi4.set_ylim(0, 1)
ax_kpi4.axis('off')
ax_kpi4.set_facecolor('#1a1a1a')
ax_kpi4.spines['bottom'].set_color('white')
ax_kpi4.spines['bottom'].set_linewidth(3)

# ===== SECOND ROW (Row 1) =====
ax1 = fig.add_subplot(gs[1, 0])
category_counts = df['Performance_Category'].value_counts()
colors_pie = [colors_category[cat] for cat in category_counts.index]
wedges, texts, autotexts = ax1.pie(
    category_counts.values,
    labels=category_counts.index,
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'}
)
ax1.set_title('Performance Distribution', fontsize=12, fontweight='bold', color='white', pad=15)

# ===== CODING vs FINAL SCORE SCATTER =====
ax2 = fig.add_subplot(gs[1, 1:3])
for category in ['Excellent', 'Good', 'Needs Improvement']:
    mask = df['Performance_Category'] == category
    ax2.scatter(
        df[mask]['Coding_Test_Score'],
        df[mask]['Performance_Score_Proxy'],
        alpha=0.6,
        s=50,
        label=category,
        color=colors_category[category]
    )
ax2.set_xlabel('Coding Test Score', fontsize=10, color='white')
ax2.set_ylabel('Performance Score', fontsize=10, color='white')
ax2.set_title('Coding Score vs Final Performance', fontsize=12, fontweight='bold', color='white', pad=15)
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.2)

# ===== CONFIDENCE vs INTERVIEWER RATING SCATTER =====
ax3 = fig.add_subplot(gs[1, 3])
for category in ['Excellent', 'Good', 'Needs Improvement']:
    mask = df['Performance_Category'] == category
    ax3.scatter(
        df[mask]['Confidence_Score'],
        df[mask]['Interviewer_Rating'],
        alpha=0.6,
        s=50,
        label=category,
        color=colors_category[category]
    )
ax3.set_xlabel('Confidence Score', fontsize=10, color='white')
ax3.set_ylabel('Interviewer Rating', fontsize=10, color='white')
ax3.set_title('Confidence vs Interviewer Rating', fontsize=12, fontweight='bold', color='white', pad=15)
ax3.legend(loc='upper left', fontsize=9)
ax3.grid(True, alpha=0.2)

# ===== THIRD ROW (Row 2) =====
ax4 = fig.add_subplot(gs[2, 0:2])
for category in ['Excellent', 'Good', 'Needs Improvement']:
    mask = df['Performance_Category'] == category
    ax4.hist(
        df[mask]['Duration_Minutes'],
        bins=20,
        alpha=0.6,
        label=category,
        color=colors_category[category]
    )
ax4.set_xlabel('Duration (Minutes)', fontsize=10, color='white')
ax4.set_ylabel('Frequency', fontsize=10, color='white')
ax4.set_title('Interview Duration Distribution', fontsize=12, fontweight='bold', color='white', pad=15)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.2, axis='y')

# ===== PERFORMANCE BY POSITION =====
ax5 = fig.add_subplot(gs[2, 2:4])
position_performance = df.groupby('Position_Applied')['Performance_Score_Proxy'].mean().sort_values(ascending=True)
bars = ax5.barh(position_performance.index, position_performance.values, color='#00D7FF')
ax5.set_xlabel('Avg Performance Score', fontsize=10, color='white')
ax5.set_title('Average Performance by Position', fontsize=12, fontweight='bold', color='white', pad=15)
ax5.grid(True, alpha=0.2, axis='x')
for i, v in enumerate(position_performance.values):
    ax5.text(v + 0.2, i, f'{v:.1f}', va='center', fontsize=9, color='white')

# ===== FOURTH ROW (Row 3) =====
ax6 = fig.add_subplot(gs[3, 0:2])
mode_performance = df.groupby('Interview_Mode')['Performance_Score_Proxy'].mean().sort_values(ascending=False)
bars = ax6.bar(mode_performance.index, mode_performance.values, color='#FFD700')
ax6.set_ylabel('Avg Performance Score', fontsize=10, color='white')
ax6.set_title('Performance by Interview Mode', fontsize=12, fontweight='bold', color='white', pad=15)
ax6.grid(True, alpha=0.2, axis='y')
for i, (idx, v) in enumerate(mode_performance.items()):
    ax6.text(i, v + 0.3, f'{v:.1f}', ha='center', fontsize=9, color='white')

# ===== TECHNICAL QUESTIONS vs PERFORMANCE =====
ax7 = fig.add_subplot(gs[3, 2])
tech_performance = df.groupby('Technical_Questions_Answered')['Performance_Score_Proxy'].mean()
ax7.plot(tech_performance.index, tech_performance.values, marker='o', linewidth=2.5, 
         markersize=8, color='#00FF7F')
ax7.fill_between(tech_performance.index, tech_performance.values, alpha=0.3, color='#00FF7F')
ax7.set_xlabel('Technical Questions Answered', fontsize=10, color='white')
ax7.set_ylabel('Avg Performance Score', fontsize=10, color='white')
ax7.set_title('Technical Questions Impact', fontsize=12, fontweight='bold', color='white', pad=15)
ax7.grid(True, alpha=0.2)

# ===== CAMERA STATUS IMPACT =====
ax8 = fig.add_subplot(gs[3, 3])
camera_data = df.groupby('Camera_On')['Performance_Score_Proxy'].agg(['mean', 'count'])
colors_camera = ['#FF6B6B', '#00FF7F']
bars = ax8.bar(camera_data.index, camera_data['mean'], color=colors_camera)
ax8.set_ylabel('Avg Performance Score', fontsize=10, color='white')
ax8.set_xlabel('Camera Status', fontsize=10, color='white')
ax8.set_title('Camera On Impact', fontsize=12, fontweight='bold', color='white', pad=15)
ax8.grid(True, alpha=0.2, axis='y')
for i, (idx, row) in enumerate(camera_data.iterrows()):
    ax8.text(i, row['mean'] + 0.3, f"{row['mean']:.1f}\n(n={int(row['count'])})", 
             ha='center', fontsize=9, color='white')

# Adjust layout
plt.tight_layout()

# Save figure
output_path = Path(__file__).parent.parent / "reports" / "figures" / "powerbi_dashboard_preview.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
print(f"✅ Dashboard preview saved to: {output_path}")

# Save as PDF as well
pdf_path = Path(__file__).parent.parent / "reports" / "figures" / "powerbi_dashboard_preview.pdf"
plt.savefig(pdf_path, bbox_inches='tight', facecolor='#1a1a1a')
print(f"✅ PDF version saved to: {pdf_path}")

# plt.show() - commented out for terminal execution
plt.close()

# Print summary statistics
print("\n" + "="*60)
print("📊 DASHBOARD SUMMARY STATISTICS")
print("="*60)
print(f"\nPerformance Metrics:")
print(f"  • Avg Performance Score: {df['Performance_Score_Proxy'].mean():.2f}")
print(f"  • Avg Confidence Score: {df['Confidence_Score'].mean():.2f}")
print(f"  • Avg Interviewer Rating: {df['Interviewer_Rating'].mean():.2f}")
print(f"\nCategory Breakdown:")
for cat in ['Excellent', 'Good', 'Needs Improvement']:
    count = len(df[df['Performance_Category'] == cat])
    pct = (count / len(df)) * 100
    offers = df[df['Performance_Category'] == cat]['Offer_Extended'].sum()
    offer_rate = (offers / count) * 100 if count > 0 else 0
    print(f"  • {cat}: {count} candidates ({pct:.1f}%), Offer Rate: {offer_rate:.1f}%")

print(f"\nInterview Modes:")
for mode in df['Interview_Mode'].unique():
    count = len(df[df['Interview_Mode'] == mode])
    avg_score = df[df['Interview_Mode'] == mode]['Performance_Score_Proxy'].mean()
    print(f"  • {mode}: {count} interviews, Avg Score: {avg_score:.2f}")

print(f"\nTop Positions by Performance:")
top_positions = df.groupby('Position_Applied')['Performance_Score_Proxy'].mean().nlargest(5)
for pos, score in top_positions.items():
    print(f"  • {pos}: {score:.2f}")

print("\n" + "="*60)
