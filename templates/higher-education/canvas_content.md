# Higher Education Data Engineering Notebook Template
## Purpose
This template generates realistic synthetic data for Higher Education demonstrations across multiple business units: Recruitment & Admissions, Student Success, and Advancement. It creates business-unit-specific datasets with built-in "drama" (trends, inflections, YoY changes) that tell compelling stories for Tableau Next and Agentforce demos. The notebook validates data quality, tests story narratives, and exports to PostgreSQL, Salesforce, or CSV for downstream consumption in Data 360 pipelines.

## User Guide
Open Command Palette: ⌘+Shift+P
Type: Python: Select Interpreter
Select the .venv interpreter from your project directory
Open the terminal and enter the following commands: 
aws sso login opens a browser window to authenticate with AWS Embark
claude initiates a Claude Code session
Generate a notebook from canvas initiates the Data Generation Claude Skill
Provide inputs to all prompts

## Notebook Scripts
### 1. Setup & Configuration
#### 1.1 Import Libraries
```python
# This is code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sys
from pathlib import Path

#Add project root to path#
sys.path.append(str(Path.cwd().parent))

from scripts.utils.config_loader import load_config
from scripts.generators.higher_ed_patterns import *
from scripts.loaders.postgres_loader import PostgresLoader
from scripts.loaders.salesforce_loader import SalesforceLoader

#Configure plotting#
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
%matplotlib inline
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print('✅ Libraries imported successfully!')
```
#### 1.2 Load Configuration & Customer Context
```python
#=== USER INPUT PARAMETERS ===#
# Configure these values before running the notebook

#Business Unit Selection#
BUSINESS_UNIT = "Recruitment & Admissions"  # Options: Recruitment & Admissions, Student Success, Advancement, etc...

#Customer Context#
CUSTOMER_NAME = "Example University"
DEMO_SCENARIO = "Show enrollment decline and recovery story"
CONTEXT_FILE = "notebooks/customers/example-university/context.md"

#Data Generation Parameters#
DATE_RANGE_DAYS = 730  # Number of days of historical data to generate
DEFAULT_RECORD_COUNT = 5000  # Number of records to generate

#Load system config#
config = load_config()

#Load customer context from NotebookLM export#
try:
    with open(CONTEXT_FILE, 'r') as f:
        customer_context = f.read()
    print(f"✅ Loaded context for {CUSTOMER_NAME}")
except FileNotFoundError:
    customer_context = ""
    print("⚠️ No customer context file found")

#Display configuration#
print(f"\nBusiness Unit: {BUSINESS_UNIT}")
print(f"Customer: {CUSTOMER_NAME}")
print(f"Scenario: {DEMO_SCENARIO}")
print(f"Default Records: {config['data_generation']['default_record_count']:,}")
print(f"Date Range: {config['data_generation']['date_range_days']} days")
```
#### 1.3 Configure Business Unit Constituents
```python
#Define constituents and metrics by business unit#
BU_CONFIG = {
    "Recruitment & Admissions": {
        "constituents": ["Applicants", "Counselors", "High Schools"],
        "primary_metrics": ["Applications", "Acceptances", "Yield Rate"],
        "pipeline_stages": ["Inquiry", "Application Started", "Application Submitted", "Accepted", "Enrolled"]
    },
    "Student Success": {
        "constituents": ["Students", "Advisors", "Support Services"],
        "primary_metrics": ["Retention Rate", "Graduation Rate", "GPA"],
        "pipeline_stages": ["At Risk", "Improving", "On Track", "Excelling"]
    },
    "Advancement": {
        "constituents": ["Donors", "Gift Officers", "Campaigns"],
        "primary_metrics": ["Gift Amount", "Donor Count", "Pledge Amount"],
        "pipeline_stages": ["Prospect", "Cultivation", "Solicitation", "Stewardship", "Major Gift"]
    }
}

bu_config = BU_CONFIG[BUSINESS_UNIT]
print(f"\n📊 {BUSINESS_UNIT} Configuration:")
print(f"Constituents: {', '.join(bu_config['constituents'])}")
print(f"Primary Metrics: {', '.join(bu_config['primary_metrics'])}")
```
Horizontal Rule
### 2. Data Generation (Inline with Claude Code)
#### 2.1 Generate Synthetic Data
```python
#Claude Code Integration Point#
#Prompt Claude Code with customer context and business unit to generate appropriate data#

#Example: Generate enrollment data with drama (recent decline)#
from faker import Faker
fake = Faker()
Faker.seed(config['data_generation']['faker_seed'])

#TODO: Replace with Claude Code generated logic based on customer context#
#This is a placeholder showing the expected structure#

num_records = 5000  # Start with subset for validation
df = generate_enrollment_funnel_data(
    num_records=num_records,
    business_unit=BUSINESS_UNIT,
    date_range_days=730,
    drama_date="2026-02-15",  # Recent inflection point
    drama_type="decline_then_recovery"
)

print(f"✅ Generated {len(df):,} records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
df.head(10)
```
#### 2.2 Schema Preview
```python
#Display schema information#
print("=== DATA SCHEMA ===")
print(f"\nColumns ({len(df.columns)}): {df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nSample Records:")
df.head()
```
Horizontal Rule
### 3. Data Quality Checks
#### 3.1 Completeness & Integrity
```python
print("=== DATA QUALITY REPORT ===")
print(f"\n📊 Total Records: {len(df):,}")
print(f"\n🔍 Missing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("  ✅ No missing values")
else:
    print(missing[missing > 0])

print(f"\n🔍 Duplicate Records: {df.duplicated().sum()}")
if df.duplicated().sum() > 0:
    print("  ⚠️ Duplicates found - review recommended")
else:
    print("  ✅ No duplicates")

print(f"\n📅 Date Range Validation:")
if 'date' in df.columns:
    date_col = 'date'
    print(f"  Start: {df[date_col].min()}")
    print(f"  End: {df[date_col].max()}")
    print(f"  Span: {(df[date_col].max() - df[date_col].min()).days} days")
    
    #Check daily distribution#
    daily_counts = df[date_col].value_counts().sort_index()
    print(f"  Records per day - Min: {daily_counts.min()}, Max: {daily_counts.max()}, Avg: {daily_counts.mean():.1f}")

print(f"\n🔗 Referential Integrity:")
#Check for any relationship columns (customize based on schema)#
for col in df.columns:
    if col.endswith('_id') or col.endswith('_key'):
        unique_count = df[col].nunique()
        print(f"  {col}: {unique_count:,} unique values")
```
#### 3.2 Statistical Summary
```python
df.describe(include='all').T
```
Horizontal Rule
### 4. Story Validation ("Drama" Check)
#### 4.1 Identify Key Inflection Points
```python
print("=== STORY VALIDATION ===")

#Define drama date (usually recent)#
DRAMA_DATE = pd.to_datetime("2026-02-15")
LOOKBACK_DAYS = 30

#Calculate trend before and after drama date#
df_sorted = df.sort_values('date')
before_drama = df_sorted[df_sorted['date'] < DRAMA_DATE]
after_drama = df_sorted[df_sorted['date'] >= DRAMA_DATE]

print(f"\n📉 Inflection Point Analysis (Drama Date: {DRAMA_DATE.date()})")
print(f"Records before: {len(before_drama):,}")
print(f"Records after: {len(after_drama):,}")

#Analyze metric changes (customize based on your metrics)#
if 'metric_value' in df.columns:
    before_avg = before_drama['metric_value'].mean()
    after_avg = after_drama['metric_value'].mean()
    pct_change = ((after_avg - before_avg) / before_avg) * 100
    
    print(f"\nMetric Average:")
    print(f"  Before drama: {before_avg:,.2f}")
    print(f"  After drama: {after_avg:,.2f}")
    print(f"  Change: {pct_change:+.1f}%")
    
    if abs(pct_change) > 10:
        print(f"  ✅ Significant drama detected ({pct_change:+.1f}%)")
    else:
        print(f"  ⚠️ Drama may be too subtle ({pct_change:+.1f}%)")
```
#### 4.2 Golden Record Lookup
```python
#Find the "golden record" - the most dramatic example in the data#
GOLDEN_RECORD_ID = None  # Set to specific ID, or find automatically

if GOLDEN_RECORD_ID:
    golden_record = df[df['id'] == GOLDEN_RECORD_ID]
    print(f"\n⭐ Golden Record (ID: {GOLDEN_RECORD_ID}):")
    print(golden_record.T)
else:
    #Find record with most dramatic change#
    #Customize logic based on your drama criteria#
    print("\n⭐ Finding most dramatic record...")
    # Example: Find record with biggest change around drama date
```
#### 4.3 Cohort Performance Validation
```python
#Ensure different cohorts perform differently (adds realism)#
if 'cohort' in df.columns or 'category' in df.columns:
    cohort_col = 'cohort' if 'cohort' in df.columns else 'category'
    
    print(f"\n👥 Cohort Performance Variation:")
    cohort_stats = df.groupby(cohort_col)['metric_value'].agg(['mean', 'std', 'count'])
    print(cohort_stats)
    
    #Check for sufficient variation#
    coef_var = cohort_stats['mean'].std() / cohort_stats['mean'].mean()
    if coef_var > 0.2:
        print(f"  ✅ Good cohort variation (CV: {coef_var:.2f})")
    else:
        print(f"  ⚠️ Cohorts may be too similar (CV: {coef_var:.2f})")
```
Horizontal Rule
### 5. Time Series Analysis (YoY/YTD)
#### 5.1 Year-over-Year Comparison
```python
#Create YoY comparison at daily granularity#
df['year'] = df['date'].dt.year
df['day_of_year'] = df['date'].dt.dayofyear

#Aggregate by year and day of year#
yoy_data = df.groupby(['year', 'day_of_year'])['metric_value'].sum().reset_index()

fig, ax = plt.subplots(figsize=(16, 6))

for year in sorted(df['year'].unique()):
    year_data = yoy_data[yoy_data['year'] == year]
    ax.plot(year_data['day_of_year'], year_data['metric_value'],
            label=f'{year}', linewidth=2, marker='o', markersize=3, alpha=0.8)

ax.set_title('Year-over-Year Comparison (Daily)', fontsize=16, fontweight='bold')
ax.set_xlabel('Day of Year', fontsize=12)
ax.set_ylabel('Metric Value', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#Calculate YoY % change#
current_year = df['year'].max()
prior_year = current_year - 1

current_total = df[df['year'] == current_year]['metric_value'].sum()
prior_total = df[df['year'] == prior_year]['metric_value'].sum()
yoy_change = ((current_total - prior_total) / prior_total) * 100

print(f"\n📊 Year-over-Year Summary:")
print(f"{prior_year}: {prior_total:,.2f}")
print(f"{current_year}: {current_total:,.2f}")
print(f"Change: {yoy_change:+.1f}%")
```
#### 5.2 Year-to-Date Comparison
```python
#YTD comparison#
current_doy = pd.Timestamp.now().timetuple().tm_yday

ytd_current = df[(df['year'] == current_year) & (df['day_of_year'] <= current_doy)]['metric_value'].sum()
ytd_prior = df[(df['year'] == prior_year) & (df['day_of_year'] <= current_doy)]['metric_value'].sum()
ytd_change = ((ytd_current - ytd_prior) / ytd_prior) * 100

print(f"\n📊 Year-to-Date (through day {current_doy}):")
print(f"{prior_year} YTD: {ytd_prior:,.2f}")
print(f"{current_year} YTD: {ytd_current:,.2f}")
print(f"Change: {ytd_change:+.1f}%")

#Highlight if significant difference#
if abs(ytd_change) > 10:
    print(f"✅ Strong YTD story: {ytd_change:+.1f}% change")
```
#### 5.3 Seasonal Pattern Validation
```python
#Validate seasonal patterns (e.g., application spikes in fall)#
df['month'] = df['date'].dt.month
monthly_avg = df.groupby('month')['metric_value'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
monthly_avg.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Seasonal Pattern (Average by Month)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Average Metric Value')
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
plt.tight_layout()
plt.show()

print("\n📅 Seasonal Peaks:")
top_months = monthly_avg.nlargest(3)
for month, value in top_months.items():
    print(f"  Month {month}: {value:,.2f}")
```
Horizontal Rule
### 6. Distribution & Cohort Analysis
#### 6.1 Distribution by Category
```python
if 'category' in df.columns or 'stage' in df.columns:
    cat_col = 'category' if 'category' in df.columns else 'stage'
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    #Count distribution#
    df[cat_col].value_counts().plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title(f'Distribution by {cat_col.title()}', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Count')
    ax1.tick_params(axis='x', rotation=45)
    
    #Value distribution#
    df.groupby(cat_col)['metric_value'].sum().plot(kind='bar', ax=ax2, color='lightcoral')
    ax2.set_title(f'Total Value by {cat_col.title()}', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Total Value')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
```
#### 6.2 Pipeline/Funnel Progression
```python
#Visualize pipeline stages (if applicable)#
if 'pipeline_stage' in df.columns:
    pipeline_counts = df['pipeline_stage'].value_counts()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    pipeline_counts.plot(kind='barh', ax=ax, color='mediumseagreen')
    ax.set_title('Pipeline Funnel', fontsize=14, fontweight='bold')
    ax.set_xlabel('Count')
    plt.tight_layout()
    plt.show()
    
    #Calculate conversion rates#
    stages = bu_config['pipeline_stages']
    print("\n🔄 Pipeline Conversion Rates:")
    for i in range(len(stages) - 1):
        stage_from = stages[i]
        stage_to = stages[i + 1]
        count_from = len(df[df['pipeline_stage'] == stage_from])
        count_to = len(df[df['pipeline_stage'] == stage_to])
        if count_from > 0:
            conversion = (count_to / count_from) * 100
            print(f"  {stage_from} → {stage_to}: {conversion:.1f}%")
```
Horizontal Rule
### 7. Outlier Detection
#### 7.1 Statistical Outliers
```python
#Identify outliers using IQR method#
if 'metric_value' in df.columns:
    Q1 = df['metric_value'].quantile(0.25)
    Q3 = df['metric_value'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['metric_value'] < lower_bound) | (df['metric_value'] > upper_bound)]
    
    print(f"=== OUTLIER DETECTION ===")
    print(f"Lower bound: {lower_bound:,.2f}")
    print(f"Upper bound: {upper_bound:,.2f}")
    print(f"Outliers found: {len(outliers):,} ({len(outliers)/len(df)*100:.1f}%)")
    
    if len(outliers) > 0:
        print("\nTop 10 Outliers:")
        print(outliers.nlargest(10, 'metric_value')[['date', 'metric_value']])
        
        #Visualize outliers#
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.scatter(df.index, df['metric_value'], alpha=0.5, s=10, label='Normal')
        ax.scatter(outliers.index, outliers['metric_value'], color='red', s=30, label='Outliers', zorder=5)
        ax.set_title('Outlier Detection', fontsize=14, fontweight='bold')
        ax.set_ylabel('Metric Value')
        ax.legend()
        plt.tight_layout()
        plt.show()
```
#### 7.2 Explainability Check
```python
#Validate that outliers are realistic and explainable#
print("\n🔍 Outlier Explainability:")
if len(outliers) > 0:
    print("Review these outliers to ensure they align with your demo story:")
    for idx, row in outliers.head(5).iterrows():
        print(f"  Date: {row['date']}, Value: {row['metric_value']:,.2f}")
    print("\n✅ Are these outliers realistic for your Higher Ed scenario?")
else:
    print("  ℹ️ No significant outliers detected")
```
Horizontal Rule
### 8. Tableau Next Preview
#### 8.1 Semantic Layer Preview
```python
print("=== TABLEAU NEXT SEMANTIC LAYER PREVIEW ===")

#Define dimensions and measures based on generated data#
dimensions = [col for col in df.columns if df[col].dtype == 'object' or col in ['date', 'year', 'month']]
measures = [col for col in df.columns if df[col].dtype in ['int64', 'float64'] and col not in ['year', 'month', 'day_of_year']]

print(f"\n📐 Dimensions ({len(dimensions)}):")
for dim in dimensions:
    print(f"  - {dim} ({df[dim].nunique()} unique values)")

print(f"\n📊 Measures ({len(measures)}):")
for measure in measures:
    print(f"  - {measure} (min: {df[measure].min():.2f}, max: {df[measure].max():.2f}, avg: {df[measure].mean():.2f})")

print(f"\n🔗 Potential Relationships:")
#Identify potential join keys#
for col in df.columns:
    if col.endswith('_id') or col.endswith('_key'):
        print(f"  - {col} (foreign key)")
```
#### 8.2 Example Metric Definitions
```python
print("\n=== SUGGESTED TABLEAU NEXT METRICS ===")

#Generate metric suggestions based on business unit#
metrics = bu_config['primary_metrics']

for metric in metrics:
    print(f"\n📈 {metric}:")
    print(f"  Formula: [Customize based on your data]")
    print(f"  Dimensions: Date, {', '.join(dimensions[:3])}")
    print(f"  Filters: [Optional business logic]")
```
#### 8.3 Natural Language Query Suggestions
```python
print("\n=== NATURAL LANGUAGE QUERY SUGGESTIONS ===")
print("Test these queries in Tableau Next with Agentforce:\n")

nl_queries = [
    f"What is the trend in {metrics[0]} over the last 2 years?",
    f"Compare {metrics[1]} year over year",
    f"Show me {metrics[2]} by {dimensions[1] if len(dimensions) > 1 else 'category'}",
    f"What caused the change in {metrics[0]} around {DRAMA_DATE.date()}?",
    f"Which {dimensions[2] if len(dimensions) > 2 else 'segment'} has the highest {metrics[0]}?",
    f"Show seasonal patterns in {metrics[1]}"
]

for i, query in enumerate(nl_queries, 1):
    print(f"{i}. \"{query}\"")
```
Horizontal Rule
### 9. Export Decision
#### 9.1 Export to PostgreSQL
```python
# Section 9.1: PostgreSQL Data Loading

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration parameters (will be populated by notebook generation)
TABLE_NAMES = ["students", "applications", "enrollments"]
EMAIL = "user@example.com"

# Initialize PostgreSQL loader with credentials from .env
pg_loader = PostgreSQLDataLoader(
    host=os.getenv('PG_HOST'),
    port=int(os.getenv('PG_PORT', 5432)),
    database=os.getenv('PG_DATABASE'),
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PASSWORD')
)

print(f"📊 Loading data to PostgreSQL...")
print(f"🔗 Host: {os.getenv('PG_HOST')}")
print(f"🗄️  Database: {os.getenv('PG_DATABASE')}")
print(f"📧 Email: {EMAIL}\n")

# Load data for each constituent table
for table_name in TABLE_NAMES:
    # Register table
    pg_loader.register_table(table_name, EMAIL)
    
    # Load corresponding dataframe (assumes df_students, df_applications, df_enrollments exist)
    df_name = f"df_{table_name}"
    if df_name in locals():
        df = locals()[df_name]
        pg_loader.load_data(df, table_name)
        print(f"✅ Loaded {len(df):,} records to table: {table_name}")
    else:
        print(f"⚠️  Dataframe {df_name} not found - skipping {table_name}")

print(f"\n✅ PostgreSQL data load complete!")
print(f"📧 Contact: {EMAIL}")
```
#### 9.2 Export to Salesforce
```python
# Section 9.2: Salesforce Data Loading

# Configuration parameters (will be populated by notebook generation)
TARGET_ORG = "your-org-alias"           # e.g., "dev", "staging", "production"
USERNAME = "user@example.com"            # Salesforce username
PASSWORD = "your-password-here"          # Salesforce password + security token
SALESFORCE_OBJECT = "Contact"            # e.g., "Contact", "Account", "hed__Application__c"

# Initialize Salesforce connection
from simple_salesforce import Salesforce

sf = Salesforce(
    username=USERNAME,
    password=PASSWORD,
    domain='test' if 'sandbox' in TARGET_ORG.lower() else 'login'
)

# Prepare data for Salesforce bulk insert
records = df.to_dict('records')

# Bulk insert data into Salesforce object
try:
    result = sf.bulk.__getattr__(SALESFORCE_OBJECT).insert(records)
    
    # Check for errors
    errors = [r for r in result if not r['success']]
    successes = [r for r in result if r['success']]
    
    print(f"✅ Successfully loaded {len(successes)} records to {SALESFORCE_OBJECT}")
    print(f"🔗 Org: {TARGET_ORG}")
    print(f"👤 User: {USERNAME}")
    
    if errors:
        print(f"⚠️  {len(errors)} records failed:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"   - {error.get('errors', 'Unknown error')}")
            
except Exception as e:
    print(f"❌ Error loading data to Salesforce: {e}")
    print(f"   Please verify credentials and object permissions")
```
#### 9.3 Export to CSV (Manual Upload)
```python
#Export to CSV for manual review or upload#
output_path = Path('../output/csv')
output_path.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'{BUSINESS_UNIT.lower().replace(" ", "_")}_{CUSTOMER_NAME.lower().replace(" ", "_")}_{timestamp}.csv'
filepath = output_path / filename

df.to_csv(filepath, index=False)
print(f"✅ Data exported to: {filepath}")
print(f"Total records: {len(df):,}")
```
Horizontal Rule
### 10. Summary & Next Steps
#### 10.1 Validation Summary
```python
print("=== VALIDATION SUMMARY ===")
print(f"\n✅ Data Quality: {'PASS' if df.isnull().sum().sum() == 0 and df.duplicated().sum() == 0 else 'REVIEW NEEDED'}")
print(f"✅ Story Drama: {'PASS' if abs(pct_change) > 10 else 'NEEDS ENHANCEMENT'}")
print(f"✅ Date Range: {(df['date'].max() - df['date'].min()).days} days of data")
print(f"✅ Record Count: {len(df):,} records")
print(f"✅ YoY Change: {yoy_change:+.1f}%")
print(f"✅ Outliers: {len(outliers):,} detected")
```
#### 10.2 Next Steps Checklist
```python
print("\n=== NEXT STEPS ===")
print("- [ ] Data looks good? Proceed with upload")
print("- [ ] Build Data 360 pipeline (Data Stream → DMO → Semantic Model)")
print("- [ ] Create Tableau Next metrics and dashboards")
print("- [ ] Test natural language queries with Agentforce")
print("- [ ] Build demo script with click path and talk track")
```
