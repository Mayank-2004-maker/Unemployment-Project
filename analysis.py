# Step 1: Library Load
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Data Loading and Cleaning
# Load from public URL
url = 'https://raw.githubusercontent.com/Ainakota/Datasets/main/Unemployment%20in%20India.csv'
df = pd.read_csv(url)

# Clean column names
df.columns = df.columns.str.strip()

# Calculate national average instead of filtering for 'India'
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df_india = df.groupby('Date')['Estimated Unemployment Rate (%)'].mean().reset_index()
df_india = df_india.sort_values('Date')
df_india = df_india.set_index('Date')
df_india = df_india.dropna()

print(f"Data cleaned Rows: {len(df_india)}")
print(df_india.head(3))


# Step 3: VISUALIZATION
plt.figure(figsize=(14, 6))
plt.plot(df_india.index, df_india['Estimated Unemployment Rate (%)'],color='crimson', linewidth=2)

# COvid Lockdown ka area highlight
plt.axvspan(pd.Timestamp('2020-03-25'), pd.Timestamp('2020-05-31'), color='grey', alpha=0.3, label='Lockdown')

plt.title('India Unemployment Rate (2019-2020)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Unemployment Rate (%)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('unemployment_trend.png')
print("\nSaved unemployment_trend.png")

# Step 4: COVID IMPACT
pre_covid = df_india[df_india.index < '2020-03-25']['Estimated Unemployment Rate (%)'].mean()
covid_peak = df_india[(df_india.index >= '2020-04-01') & (df_india.index <= '2020-05-31')]['Estimated Unemployment Rate (%)'].max()

print("\n--- COVID ANALYSIS ---")
print(f"Pre-COVID Average: {pre_covid:.2f}%")
print(f"Covid Peak April-May 2020: {covid_peak:.2f}%")
print(f"Jump: +{covid_peak - pre_covid:.2f}% points")


# Step 5: SEASONALITY
df_india['Month'] = df_india.index.month
monthly_avg = df_india.groupby('Month')['Estimated Unemployment Rate (%)'].mean()

plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_avg.index, y=monthly_avg.values, hue=monthly_avg.index, palette='coolwarm', legend=False)
plt.title('Seasonal Pattern: Avg Unemployment by Month', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Avg Rate %', fontsize=12)
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig('seasonal_pattern.png')
print("Saved seasonal_pattern.png")

# State Heatmap Code
pivot_tables = df.pivot_table(values='Estimated Unemployment Rate (%)', index='Region', columns=df['Date'].dt.strftime('%Y-%m'), aggfunc='mean')

plt.figure(figsize=(14, 8))
sns.heatmap(pivot_tables, cmap='Reds', linewidths=0.5)
plt.title('State-wise Unemployment Heatmap')
plt.tight_layout()
plt.savefig('Heatmap.png')
plt.show()