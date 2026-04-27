# Demo Data Generation Scripts

Synthetic data generation toolkit for creating realistic demo datasets for Salesforce demonstrations across Education, Financial Services, and other industries. Generates data with built-in "drama" (trends, inflections, YoY changes) that tells compelling stories for Tableau Next and Agentforce demos.

## Features

- **Industry Templates**: Pre-built notebooks for Higher Education, Financial Services, and more
- **Business Unit Support**: Recruitment & Admissions, Student Success, Advancement, Fraud Operations
- **AI-Powered Customization**: Claude Code skill generates customer-specific data generation code
- **Multiple Export Options**: PostgreSQL, Salesforce, or CSV output
- **Built-in Drama Patterns**: Enrollment decline/recovery, fraud spikes, intervention success stories
- **Quality Validation**: Data quality checks, statistical summaries, outlier detection
- **Tableau Integration**: Semantic layer preview and natural language query suggestions

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "Python Data Generation Scripts"
```

### 2. Set Up Python Environment

**Prerequisites**: Python 3.11 or higher

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# Use your favorite text editor (nano, vim, VS Code, etc.)
nano .env
```

**Required credentials in `.env`:**

- **PostgreSQL** (if using database output):
  ```env
  PG_HOST=your_postgres_host
  PG_PORT=5432
  PG_DATABASE=your_database_name
  PG_USER=your_database_username
  PG_PASSWORD=your_database_password
  ```

- **Slack API** (if importing canvas templates):
  ```env
  SLACK_TOKEN=xoxb-your-slack-bot-token-here
  ```

- **Salesforce** (if using Salesforce output):
  ```env
  SF_USERNAME=your_salesforce_username
  SF_PASSWORD=your_salesforce_password
  SF_SECURITY_TOKEN=your_salesforce_security_token
  SF_DOMAIN=login  # or 'test' for sandbox
  ```

⚠️ **IMPORTANT**: Never commit your `.env` file to Git. It contains sensitive credentials.

### 4. Verify Installation

```bash
# Test that all dependencies are installed
python3 -c "import pandas, numpy, faker, simple_salesforce; print('✅ All dependencies installed')"

# Run a simple test
python3 scripts/utils/config_loader.py
```

## Using the Notebook Generation Skill

This project includes a Claude Code skill for generating customer-specific Jupyter notebooks.

### Prerequisites

- Claude Code CLI or VS Code extension installed
- Active Claude Code session

### Generate a Customer Notebook

1. **Start Claude Code:**
   ```bash
   claude
   ```

2. **Invoke the skill:**
   ```
   /notebook-from-canvas
   ```
   Or simply ask:
   ```
   Generate a notebook from canvas for Higher Education
   ```

3. **Follow the prompts:**
   - Select industry (Education, Financial Services, etc.)
   - Choose existing template or create new
   - Provide customer name (e.g., "Miami University of Ohio")
   - Enter business unit context (e.g., "Student Success")
   - Paste customer research/context (optional but recommended)
   - Configure output destination (PostgreSQL/Salesforce/CSV)

4. **Result:**
   - Customer-specific notebook created at: `notebooks/customers/{customer-name}/`
   - Context file: `notebooks/customers/{customer-name}/context.md`
   - Ready-to-run Jupyter notebook with custom data generation code

### Skill Features

- ✅ **Customer-specific data generation** tailored to business unit and scenario
- ✅ **Built-in drama patterns** (enrollment decline/recovery, fraud spikes, etc.)
- ✅ **Automatic code customization** based on your inputs
- ✅ **Multiple output formats** (PostgreSQL, Salesforce, CSV)
- ✅ **Context-aware** - uses NotebookLM exports or research notes

## Manual Notebook Usage

If you prefer to work without the skill:

### 1. Generate a Notebook from Template

```bash
# For Higher Education
python3 scripts/generate_notebook.py --template higher-education

# For Financial Services
python3 scripts/generate_notebook.py --template fraud-operations
```

### 2. Customize the Notebook

Open the generated notebook in Jupyter:

```bash
jupyter notebook notebooks/higher-education/higher-education_20260427.ipynb
```

Or in VS Code:
```bash
code notebooks/higher-education/higher-education_20260427.ipynb
```

### 3. Update Configuration Variables

Edit **Section 1.2** in the notebook:

```python
BUSINESS_UNIT = "Student Success"
CUSTOMER_NAME = "Your University Name"
DEMO_SCENARIO = "At-risk student intervention"
INSTITUTION_TYPE = "Public 4-Year"
INSTITUTION_SIZE = "Medium (5,000-15,000)"
ACADEMIC_YEAR = "2024-2025"
```

### 4. Run the Notebook

- Execute all cells: `Cell → Run All`
- Or run sequentially: `Shift + Enter` on each cell

### 5. Export Data

The notebook will guide you through exporting to:
- **PostgreSQL**: Section 9.1
- **Salesforce**: Section 9.2
- **CSV**: Section 9.3

## Project Structure

```
.
├── .claude/                    # Claude Code configuration and skills
│   └── skills/
│       └── notebook-from-canvas.skill.md
├── config/                     # YAML configuration files
├── notebooks/
│   ├── higher-education/       # Higher Ed templates
│   │   └── canvas_content.md
│   ├── fraud-operations/       # Financial Services templates
│   └── customers/              # Customer-specific notebooks
│       └── {customer-name}/
│           ├── {customer-name}.ipynb
│           └── context.md
├── scripts/
│   ├── generators/             # Data generation modules
│   ├── loaders/                # Data loaders (PostgreSQL, Salesforce)
│   └── utils/                  # Utilities (config loader, etc.)
├── output/
│   ├── csv/                    # Generated CSV files
│   └── logs/                   # Log files
├── .env                        # Environment variables (DO NOT COMMIT)
├── .env.example                # Example environment file (safe to commit)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Available Templates

### Higher Education
- **Business Units**: Recruitment & Admissions, Student Success, Advancement
- **Scenarios**: Enrollment decline/recovery, at-risk intervention, donor campaigns
- **Data Types**: Applications, enrollments, student retention, donor gifts

### Financial Services
- **Business Units**: Fraud Operations, Retail Banking, Wealth Management
- **Scenarios**: Fraud spike/mitigation, customer retention, cross-sell growth
- **Data Types**: Transactions, fraud flags, account data

## Common Tasks

### Add a New Template

1. Create directory: `notebooks/your-template/`
2. Export Slack Canvas to `notebooks/your-template/canvas_content.md`
3. Generate notebook: `python3 scripts/generate_notebook.py --template your-template`

### Update Customer Context

Edit the context file at `notebooks/customers/{customer-name}/context.md` with:
- Customer background research
- NotebookLM exports
- Meeting notes or discovery findings
- Institutional priorities

The data generation code will reference this context for more realistic data.

### Clean Generated Files

```bash
# Remove CSV output files
rm output/csv/*.csv

# Remove log files
rm output/logs/*.log

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
```

## Troubleshooting

### "Module not found" errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### PostgreSQL connection issues

- Verify credentials in `.env` file
- Check `PG_HOST`, `PG_PORT`, `PG_DATABASE` are correct
- Ensure your IP is whitelisted on the database server

### Salesforce authentication errors

- Verify `SF_USERNAME`, `SF_PASSWORD`, `SF_SECURITY_TOKEN` in `.env`
- Check `SF_DOMAIN` is set correctly (`login` or `test`)
- Ensure API access is enabled for your Salesforce user

### Jupyter notebook won't start

```bash
# Ensure jupyter is installed
pip install jupyter

# Launch with explicit Python interpreter
python3 -m jupyter notebook
```

## Getting Help

- **Internal Issues**: Contact the SE Resources team
- **Claude Code Skill Issues**: Check `.claude/skills/notebook-from-canvas.skill.md`
- **Python Errors**: Verify all dependencies in `requirements.txt` are installed

## Security Best Practices

⚠️ **NEVER commit these files:**
- `.env` (contains live credentials)
- Customer-specific notebooks in `notebooks/customers/*/`
- Generated CSV files with real or sensitive data

✅ **Safe to commit:**
- `.env.example` (template only)
- Template files: `notebooks/*/canvas_content.md`
- Script files in `scripts/`
- Configuration files in `config/`

## Contributing

When adding new features:
1. Update this README with usage instructions
2. Add new dependencies to `requirements.txt`
3. Update `.env.example` if new credentials are needed
4. Test with a clean virtual environment before committing

## License

Internal use only - Salesforce SE Resources team.
