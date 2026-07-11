# Simple test to show the analysis results
import pandas as pd

url = 'https://raw.githubusercontent.com/Ainakota/Datasets/main/Unemployment%20in%20India.csv'
df = pd.read_csv(url)
df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df_india = df.groupby('Date')['Estimated Unemployment Rate (%)'].mean().reset_index()
df_india = df_india.set_index('Date')

print(f"Data cleaned Rows: {len(df_india)}")
print(df_india.head(3))

pre_covid = df_india[df_india.index < '2020-03-25']['Estimated Unemployment Rate (%)'].mean()
covid_peak = df_india[(df_india.index >= '2020-04-01') & (df_india.index <= '2020-05-31')]['Estimated Unemployment Rate (%)'].max()

print("\n--- COVID ANALYSIS ---")
print(f"Pre-COVID Average: {pre_covid:.2f}%")
print(f"Covid Peak April-May 2020: {covid_peak:.2f}%")
print(f"Jump: +{covid_peak - pre_covid:.2f}% points")
