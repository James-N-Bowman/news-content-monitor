import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_github_visuals(file_path):
    # Load data
    df = pd.read_csv(file_path)
    df['Date Published'] = pd.to_datetime(df['Date Published'])

    # --- Chart 1: Average Heading Length by Committee ---
    plt.figure(figsize=(10, 6))
    cttee_data = df.groupby('Committee Name')['Heading Word Count'].median().sort_values()
    
    cttee_data.plot(kind='barh', color='#2ea44f', edgecolor='#1b1f23') # GitHub-style green
    plt.title('Median Heading Word Count by Committee', fontweight='bold')
    plt.xlabel('Median Words')
    plt.ylabel('')
    plt.tight_layout()
    
    plt.savefig('docs/committee_avg.svg') 
    plt.close()

    # --- Chart 2: Monthly Heading Trend ---
    plt.figure(figsize=(10, 6))
    # 'MS' is Month Start frequency
    monthly_data = df.resample('MS', on='Date Published')['Heading Word Count'].median()
    # 2. Dynamically calculate the middle: (Start + End) / 2

    month_starts = monthly_data.index
    month_ends = monthly_data.index + pd.offsets.MonthEnd(0)

    plt.xlim(monthly_data.index.min(), monthly_data.index.max() + pd.offsets.MonthEnd(0))

    #monthly_data.index = month_starts + (month_ends - month_starts) / 2
    monthly_data.index = month_starts + pd.Timedelta(days=15)

    # Set the x-axis to start at your first month and end at your last month

    plt.bar(monthly_data.index, monthly_data.values, width=25, align='center', color='#0969da', edgecolor='#1b1f23') # GitHub-style blue
    plt.title('Median Average Heading Word Count', fontweight='bold')
    
    # Format the X-axis for dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
    plt.xticks(rotation=45)
    
    plt.ylabel('Median Words')
    plt.tight_layout()

    plt.savefig('docs/monthly_trend.svg')
    plt.close()

    print("Success! Generated SVG (for GitHub/HTML) and PDF (for reports).")

if __name__ == "__main__":
    generate_github_visuals('docs/committee_news.csv')