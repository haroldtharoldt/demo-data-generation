> # ⚠️ DEPRECATED — READ-ONLY ARCHIVE
>
> This repository is **no longer maintained** and has been **archived (read-only)** as of June 2026.
>
> The data-generation toolkit has moved to **Salesforce EMU GitHub** (`salesforce.ghe.com`), as company work must live in EMU rather than personal GitHub. The Financial Services edition was migrated there; this repository has been **scoped down to Higher Education only** and frozen for reference.
>
> **If you want to continue using this toolkit:** clone it and push your own copy to EMU (or your team's sanctioned location). You cannot push here — the repo is archived.
>
> ```bash
> git clone https://github.com/haroldtharoldt/demo-data-generation.git
> # then create your own EMU repo and push to it
> ```
>
> Questions: contact Harold Thomas.

---

# Demo Data Generation Scripts (Higher Education)

Synthetic data generation toolkit for creating realistic demo datasets for Salesforce demonstrations in **Higher Education**. Generates data with built-in "drama" (trends, inflections, YoY changes) that tells compelling stories for Tableau Next and Agentforce demos.

## Features

- **Industry Templates**: Pre-built notebooks for Higher Education business units
- **Business Unit Support**: Recruitment & Admissions, Student Success, Advancement, Registrar, Corporate Engagement
- **AI-Powered Customization**: Claude Code skill generates institution-specific data generation code
- **Multiple Export Options**: PostgreSQL, Salesforce, or CSV output
- **Built-in Drama Patterns**: Enrollment decline/recovery, at-risk intervention success, donor campaign surges
- **Quality Validation**: Data quality checks, statistical summaries, outlier detection
- **Tableau Integration**: Semantic layer preview and natural language query suggestions

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/haroldtharoldt/demo-data-generation.git
cd demo-data-generation
```

### 2. Set Up Python Environment

**Prerequisites**: Python 3.11 or higher

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux  (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

**Required credentials in `.env`:**

- **PostgreSQL** (if using database output): `PG_HOST`, `PG_PORT`, `PG_DATABASE`, `PG_USER`, `PG_PASSWORD`
- **Slack API** (if importing canvas templates): `SLACK_TOKEN`
- **Salesforce** (if using Salesforce output): `SF_USERNAME`, `SF_PASSWORD`, `SF_SECURITY_TOKEN`, `SF_DOMAIN` (`login` or `test`)

⚠️ **IMPORTANT**: Never commit your `.env` file to Git. It contains sensitive credentials.

### 4. Verify Installation

```bash
python3 -c "import pandas, numpy, faker, simple_salesforce; print('✅ All dependencies installed')"
python3 scripts/utils/config_loader.py
```

## Using the Notebook Generation Skill

This project includes a Claude Code skill for generating institution-specific Jupyter notebooks.

1. **Start Claude Code:** `claude`
2. **Invoke the skill:** `/notebook-from-canvas` (or ask "Generate a notebook from canvas")
3. **Follow the prompts:**
   - Choose existing template (Higher Education) or create new from a Slack Canvas
   - Provide institution name (e.g., "Miami University of Ohio")
   - Enter business unit context (e.g., "Student Success")
   - Paste institution research/context (optional but recommended)
   - Configure output destination (PostgreSQL/Salesforce/CSV)
4. **Result:** institution-specific notebook at `notebooks/customers/{customer-name}/` plus a `context.md`.

## Manual Notebook Usage

```bash
python3 scripts/generate_notebook.py --template higher-education
code notebooks/higher-education/higher-education_{timestamp}.ipynb
```

Edit **Section 1.2** variables:

```python
BUSINESS_UNIT = "Student Success"
CUSTOMER_NAME = "Your University Name"
DEMO_SCENARIO = "At-risk student intervention"
INSTITUTION_TYPE = "Public 4-Year"
INSTITUTION_SIZE = "Medium (5,000-15,000)"
ACADEMIC_YEAR = "2024-2025"
```

Run all cells, then export via Section 9.1 (PostgreSQL) / 9.2 (Salesforce) / 9.3 (CSV).

## Project Structure

```
.
├── .claude/skills/notebook-from-canvas.skill.md   # HE notebook-generation skill
├── config/                     # YAML configuration files
├── templates/
│   └── higher-education/canvas_content.md
├── notebooks/customers/        # Institution-specific notebooks
│   └── {customer-name}/{customer-name}.ipynb + context.md
├── scripts/
│   ├── generators/  loaders/  utils/
│   └── generate_notebook.py
├── output/csv/  output/logs/
├── .env.example                # safe template (.env is gitignored)
├── requirements.txt
└── README.md
```

## Available Templates

### Higher Education
- **Business Units**: Recruitment & Admissions, Student Success, Advancement
- **Scenarios**: Enrollment decline/recovery, at-risk intervention, donor campaigns
- **Data Types**: Applications, enrollments, student retention, donor gifts

## Common Tasks

- **Add a template:** create `templates/your-template/`, export a Slack Canvas to `canvas_content.md`, run `python3 scripts/generate_notebook.py --template your-template`
- **Update context:** edit `notebooks/customers/{customer-name}/context.md` with research / NotebookLM exports / discovery findings
- **Clean generated files:** `rm output/csv/*.csv output/logs/*.log`

## Troubleshooting

- **"Module not found"**: activate `.venv`, re-run `pip install -r requirements.txt`
- **PostgreSQL**: verify `PG_*` in `.env`; ensure your IP is whitelisted
- **Salesforce auth**: verify `SF_*` in `.env`; check `SF_DOMAIN` (`login`/`test`); ensure API access is enabled
- **Jupyter won't start**: `pip install jupyter`, then `python3 -m jupyter notebook`

## Security Best Practices

⚠️ **NEVER commit:** `.env` (live credentials), customer notebooks in `notebooks/customers/*/`, generated CSVs with real/sensitive data.
✅ **Safe to commit:** `.env.example`, template `canvas_content.md` files, `scripts/`, `config/`.

## License

Internal use only — Salesforce SE.
