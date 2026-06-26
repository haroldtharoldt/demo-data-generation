# Notebook from Canvas Template (Higher Education)

Generate a customized Jupyter notebook from a Higher Education Slack Canvas template with customer context variables.

## Instructions

You are helping the user generate a Higher Education data-generation Jupyter notebook from a Slack Canvas template and customize it with institution-specific information.

### Step 1: Select Existing Template or Create New

1. Check for existing canvas_content.md files in the templates/ directory:
   - Look in `templates/higher-education/`, `templates/student-success/`, `templates/advancement/`, `templates/registrar/`, etc.

2. Build a list of available templates by checking which directories contain `canvas_content.md` files:
   `find templates -name "canvas_content.md" -type f`

3. Use the AskUserQuestion tool to present existing templates plus a "Create New" option:
   - question: "Which template would you like to use?"
   - header: "Template"
   - For each found canvas_content.md file, create an option with:
     - label: The directory name (formatted nicely, e.g., "Higher Education")
     - description: "Use existing canvas_content.md from templates/{directory-name}/"
   - Add a final option:
     - label: "Create New from Slack Canvas"
     - description: "Import new canvas content from Slack (requires canvas URL)"

4. Store the user's selection:
   - If they select an existing template: Note the directory path and SKIP to Step 3
   - If they select "Create New from Slack Canvas": Continue to Step 2

### Step 2: Import Canvas Content from Slack (Only for New Templates)

**This step is only executed if the user selected "Create New from Slack Canvas" in Step 1.**

1. Use the AskUserQuestion tool to collect:
   - question: "What is the Slack Canvas ID or URL?"
   - header: "Canvas ID"
   - (Allow free text input)

2. Parse the canvas ID from the input (handle both full URLs and direct IDs)

3. Prompt for a template name:
   - question: "What should we name this template? (will create templates/{name}/ directory)"
   - header: "Template Name"
   - (Suggest lowercase-with-hyphens format like "student-success" or "advancement")

4. Create the template directory: `templates/{template-name}/`

5. Inform the user they need to manually export the canvas content:
   - Tell them to open the canvas URL: `https://salesforce.enterprise.slack.com/docs/T026QPGMQ/{canvas_id}`
   - Tell them to copy ALL content (⌘+A, ⌘+C)
   - Tell them to save it to: `templates/{template-name}/canvas_content.md`
   - Tell them to confirm when ready

6. Once confirmed, verify the file exists at `templates/{template-name}/canvas_content.md`

7. Execute the notebook generation script:
   - `python3 scripts/generate_notebook.py --template {template-name}`

8. Check the output to see where the notebook was saved (in `notebooks/{template-name}/` directory)

### Step 3: Generate Notebook and Collect Customer Context

**If user selected an existing template in Step 1 (skipped Step 2):**

1. Execute the notebook generation script using the existing canvas_content.md:
   ```bash
   python3 scripts/generate_notebook.py --template {template-directory-name}
   ```
2. Check the output to see where the notebook was saved

**If user created a new template in Step 2:**

- The notebook was already generated in Step 2, proceed to customization

#### 3.1 Institution Identification

1. Use AskUserQuestion to collect the institution name:
   - question: "What is the name of the institution for this demo?"
   - header: "Institution Name"
   - options:
     - Provide 2-3 examples: "State University", "Metro College", "Tech Institute"
     - User can select "Other" for custom input

2. Store the institution name for use in notebook customization

#### 3.2 Business Unit and Context Variables

3. Use AskUserQuestion to gather education customer context values:
   - BUSINESS_UNIT (e.g., "Recruitment & Admissions", "Advancement", "Student Success")
   - INSTITUTION_TYPE (e.g., "Public 4-Year", "Private 4-Year", "Community College")
   - INSTITUTION_SIZE (e.g., "Small (<5,000)", "Medium (5,000-15,000)", "Large (>15,000)")
   - ACADEMIC_YEAR (e.g., "2024-2025", "2025-2026", "2026-2027")
   - DEMO_SCENARIO (e.g., "Enrollment decline and recovery", "Record growth", "Improving yield rates")

4. Create multi-question prompts (up to 4 variables at a time) with sensible default options

#### 3.3 Customer Context File Setup

1. Inform the user about the context.md file purpose:
   - Contains additional institution background from NotebookLM or research
   - Helps generate more realistic, institution-specific demo data
   - Optional but recommended for high-quality demos

2. Use AskUserQuestion to ask if they have context to provide:
   - question: "Would you like to add institution context for more realistic demo data?"
   - header: "Context"
   - options:
     - label: "Yes, I'll paste my research"
       description: "Paste institution background, NotebookLM export, or meeting notes"
     - label: "No, skip for now"
       description: "Generate notebook without additional context (can add later)"

3. Based on response:
   - **If "Yes, I'll paste my research"**:
     - Use AskUserQuestion with free text input to collect the content
     - Create directory: `notebooks/customers/{customer-name-slug}/`
     - Write the pasted content to `notebooks/customers/{customer-name-slug}/context.md`
     - Confirm: "✅ Created context file at notebooks/customers/{customer-name-slug}/context.md"
   - **If "No, skip for now"**:
     - Set CONTEXT_FILE to the default path but note it doesn't exist yet
     - Inform user they can add context later by creating this file

4. Store the CONTEXT_FILE path for use in notebook customization

#### 3.4 Customize Notebook with Institution Data

1. Read the context file (if it exists) to understand institution background

2. **Update Section 1.2 (cell-3)** with all collected context variables:
   - Use NotebookEdit to replace placeholder values
   - Update: CUSTOMER_NAME, BUSINESS_UNIT, DEMO_SCENARIO, CONTEXT_FILE, INSTITUTION_TYPE, INSTITUTION_SIZE, ACADEMIC_YEAR

3. **Generate Custom Data Generation Code for Section 2.1 (cell-7)** based on Business Unit:

   **For Recruitment & Admissions:**
   - Generate application/enrollment funnel data
   - Columns: applicant_id, application_date, decision_date, enrollment_date, pipeline_stage, source_type, gpa, test_scores
   - Apply drama pattern (e.g., enrollment decline then recovery around specific date)

   **For Student Success:**
   - Generate student retention/GPA tracking data
   - Columns: student_id, term, gpa, credits_earned, at_risk_flag, intervention_type, retention_status, engagement_score
   - Apply drama pattern (e.g., improving retention rates after intervention program)

   **For Advancement:**
   - Generate donor/campaign data
   - Columns: donor_id, gift_date, gift_amount, campaign, donor_type, cumulative_giving, pipeline_stage
   - Apply drama pattern (e.g., major gift campaign success, year-end surge)

4. Use NotebookEdit to replace the placeholder code in Section 2.1 (cell-7) with the generated custom code

5. **Move and rename the notebook to the customer directory**:
   - Determine customer slug from CUSTOMER_NAME (e.g., "Miami University of Ohio" → "miami-university-ohio")
   - From: `notebooks/{template-name}/{template-name}_{timestamp}.ipynb`
   - To: `notebooks/customers/{customer-name-slug}/{customer-name-slug}.ipynb`
   - Example: `mv notebooks/higher-education/higher-education_20260427.ipynb notebooks/customers/miami-university-ohio/miami-university-ohio.ipynb`

6. Verify the notebook was moved successfully and confirm the new path

### Step 4: Prompt for Data Output Location

After customizing the notebook, determine where the generated data should be output.

1. Use the AskUserQuestion tool:
   - question: "Where would you like to output the generated data?"
   - header: "Output Destination"
   - options:
     - label: "PostgreSQL"
       description: "Store data in a PostgreSQL database table"
     - label: "Salesforce"
       description: "Load data directly into a Salesforce org"
     - label: "CSV (Default)"
       description: "Save data to a CSV file as backup or default option"

### Step 5: Collect Output-Specific Parameters

Based on the user's selection, collect the necessary parameters:

#### 5.1: PostgreSQL Output

If the user selects PostgreSQL:
1. Collect target table name (common options: "students", "applications", "donors")
2. Collect the email associated with this data load
3. Read section 9.1 of the notebook to identify the PostgreSQL data loading cell
4. Use NotebookEdit/Edit to replace `TABLE_NAME` and `EMAIL`
5. Verify the replacements

#### 5.2: Salesforce Output

If the user selects Salesforce:
1. Collect Salesforce org alias/username, username, and password/security token
2. **Query the org for schema information:**
   - `sf sobject list --target-org {TARGET_ORG} --sobject all`
   - Or via simple-salesforce:
     ```python
     from simple_salesforce import Salesforce
     sf = Salesforce(username='...', password='...', security_token='...')
     objects = sf.describe()['sobjects']
     relevant_objects = [obj['name'] for obj in objects if obj['createable']]
     ```
3. Present common/relevant objects to the user:
   - question: "Which Salesforce object should we load data into?"
   - header: "Target Object"
   - options: Contact, Account, Lead, custom `__c` objects, and Education Cloud objects (if detected): `hed__Course__c`, `hed__Application__c`, etc.
4. Read section 9.2 and replace `TARGET_ORG`, `USERNAME`, `PASSWORD`, `SALESFORCE_OBJECT`
5. Verify the replacements

#### 5.3: CSV Output (Default/Backup)

For CSV output (always offer as backup):
1. Collect the desired output path (default `./output/data.csv`, or timestamped, or custom)
2. Read section 9.3 and update the CSV export cell with the provided output path
3. Verify the replacements

### Step 6: Verify Output Configuration

1. Read the updated notebook sections (9.1, 9.2, and/or 9.3) to verify parameters
2. Provide a summary of the output settings configured:
   - PostgreSQL: "Data will be loaded to table '{TABLE_NAME}' with email '{EMAIL}'"
   - Salesforce: "Data will be loaded to '{SALESFORCE_OBJECT}' in org '{TARGET_ORG}'"
   - CSV: "Data will be exported to '{output_path}'"

### Step 7: Completion

1. Inform the user the notebook has been fully generated and customized
2. **Summarize what was created:**
   - "✅ Created institution-specific notebook: `{customer-name-slug}.ipynb`"
   - "Section 1.2: All context variables populated ({BUSINESS_UNIT}, {INSTITUTION_TYPE}, etc.)"
   - "Section 2.1: Custom Python code to generate {BUSINESS_UNIT} demo data for {CUSTOMER_NAME}"
   - "Section 9: Output destination configured ({PostgreSQL/Salesforce/CSV})"
   - "Context file: notebooks/customers/{customer-name-slug}/context.md" (if created)
3. Provide the full path to the institution-named notebook
4. **Explain how to use the notebook** (run all cells to generate data; Section 2.1 holds the custom generation logic; Section 9 exports to the configured destination)
5. Remind them to review Section 2.1 code to understand the data schema before running
6. **Automatically open the notebook in VS Code:** `code notebooks/customers/{customer-name-slug}/{customer-name-slug}.ipynb`

## Important Notes

- **Existing Templates:** Check for existing canvas_content.md files before prompting to create new ones: `find templates -name "canvas_content.md" -type f`
- The generate_notebook.py script requires manual canvas export for now (future versions may support API integration)
- When replacing variables in the notebook, only replace actual placeholder variables, not arbitrary uses of those words in text
- After editing the notebook, always verify the changes were applied correctly
- **Security Consideration:** When collecting Salesforce passwords/tokens, remind the user these will be embedded in the notebook. Suggest using environment variables or `.env` files instead.
- The Salesforce org query step requires either the Salesforce CLI (`sf`) or the `simple-salesforce` Python package
- If the notebook doesn't have sections 9.1, 9.2, or 9.3, the canvas template may need to be updated

## File Structure

Templates are stored in:
- **templates/{template-name}/canvas_content.md** — Raw Slack canvas content

Customer-specific files are stored together in:
- **notebooks/customers/{customer-name-slug}/**
  - **{customer-name-slug}.ipynb** — The institution-specific Jupyter notebook
  - **context.md** — Institution background from NotebookLM/research (optional)

## Notebook Sections

- **Sections 1-8:** Context, data generation logic, and transformations
- **Section 9.1:** PostgreSQL data loading (TABLE_NAME, EMAIL)
- **Section 9.2:** Salesforce data loading (TARGET_ORG, USERNAME, PASSWORD, SALESFORCE_OBJECT)
- **Section 9.3:** CSV export (output_path)

## Example Workflow (Existing Higher Education Template)

1. User invokes the skill / asks to "Generate a notebook from canvas"
2. You check templates/ and find `templates/higher-education/canvas_content.md`
3. You present options: "Higher Education" or "Create New from Slack Canvas"
4. User selects "Higher Education"
5. You run: `python3 scripts/generate_notebook.py --template higher-education`
6. The script generates: `notebooks/higher-education/higher-education_{timestamp}.ipynb`
7. You collect variables: BUSINESS_UNIT="Student Success", CUSTOMER_NAME="State University", INSTITUTION_TYPE="Public 4-Year", INSTITUTION_SIZE="Large (>15,000)", ACADEMIC_YEAR="2025-2026", DEMO_SCENARIO="At-risk student intervention"
8. You ask if they want to add context; user pastes NotebookLM research about retention challenges
9. You create `notebooks/customers/state-university/context.md`
10. You update cell-3 with context variables, cell-7 with Student Success data generation code
11. You move/rename the notebook to `notebooks/customers/state-university/state-university.ipynb`
12. You configure output (PostgreSQL/Salesforce/CSV) and complete the workflow

## Error Handling

- If no templates are found for the selected template, inform the user and offer to create a new one
- If generate_notebook.py is not found, inform the user
- If notebook generation fails, show the error and help troubleshoot
- If a canvas_content.md file is missing/corrupted, suggest recreating it
- If Salesforce connection fails during schema query, ask them to verify credentials; if `sf` CLI is unavailable, fall back to manually specifying the target object
- If section 9.1/9.2/9.3 is not found, inform the user that output method isn't supported by the notebook
- If user provides an invalid Slack Canvas URL/ID, parse gracefully and extract the canvas ID portion
