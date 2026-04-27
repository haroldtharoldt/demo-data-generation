# Notebook from Canvas Template

Generate a customized Jupyter notebook from a Slack Canvas template with customer context variables.

## Instructions

You are helping the user generate a Jupyter notebook from a Slack Canvas template and customize it with customer-specific information.

### Step 1: Prompt for Industry Selection

1. Use the AskUserQuestion tool to ask the user which industry they want to generate a notebook for:
   - question: "Which industry would you like to generate a notebook for?"
   - header: "Industry"
   - options:
     - label: "Education"
       description: "Use existing Higher Education templates or create new education-focused notebook"
     - label: "Financial Services"
       description: "Use existing Financial Services templates or create new FINS-focused notebook"
     - label: "New Industry"
       description: "Import canvas content from Slack to create a new industry template"
2. Store the selected industry for use in later steps

### Step 2: Select Existing Template or Create New

**For "Education" or "Financial Services" industries:**

1. Check for existing canvas_content.md files in the templates/ directory:
   - For Education: Look in `templates/higher-education/`, `templates/student-success/`, `templates/advancement/`, etc.
   - For Financial Services: Look in `templates/financial-services/`, `templates/fraud-operations/`, etc.
   
2. Build a list of available templates by checking which directories contain `canvas_content.md` files

3. Use the AskUserQuestion tool to present existing templates plus a "Create New" option:
   - question: "Which template would you like to use?"
   - header: "Template"
   - For each found canvas_content.md file, create an option with:
     - label: The directory name (formatted nicely, e.g., "Higher Education", "Financial Services")
     - description: "Use existing canvas_content.md from templates/{directory-name}/"
   - Add a final option:
     - label: "Create New from Slack Canvas"
     - description: "Import new canvas content from Slack (requires canvas URL)"
   
4. Store the user's selection:
   - If they select an existing template: Note the directory path and SKIP to Step 4
   - If they select "Create New from Slack Canvas": Continue to Step 3

**For "New Industry":**

- Skip directly to Step 3 (no existing templates to offer)

### Step 3: Import Canvas Content from Slack (Only for New Templates)

**This step is only executed if:**
- User selected "New Industry" in Step 1, OR
- User selected "Create New from Slack Canvas" in Step 2

1. Use the AskUserQuestion tool to collect:
   - question: "What is the Slack Canvas ID or URL?"
   - header: "Canvas ID"
   - (Allow free text input)

2. Parse the canvas ID from the input (handle both full URLs and direct IDs)

3. Prompt for a template name:
   - question: "What should we name this template? (will create templates/{name}/ directory)"
   - header: "Template Name"
   - (Suggest lowercase-with-hyphens format like "wealth-management" or "healthcare")

4. Create the template directory: `templates/{template-name}/`

5. Inform the user they need to manually export the canvas content:
   - Tell them to open the canvas URL: `https://salesforce.enterprise.slack.com/docs/T026QPGMQ/{canvas_id}`
   - Tell them to copy ALL content (⌘+A, ⌘+C)
   - Tell them to save it to: `templates/{template-name}/canvas_content.md`
   - Tell them to confirm when ready

6. Once confirmed, verify the file exists at `templates/{template-name}/canvas_content.md`

7. Execute the notebook generation script:
   - Determine which script to use based on Step 1 industry selection:
     - "Education" → `python3 scripts/generate_notebook.py --template {template-name}`
     - "Financial Services" → `python3 scripts/generate_notebook.py --template {template-name}`
     - "New Industry" → `python3 scripts/generate_notebook.py --template {template-name}`
   
8. Check the output to see where the notebook was saved (in `notebooks/{template-name}/` directory)

### Step 4: Generate Notebook and Collect Customer Context

**If user selected an existing template in Step 2 (skipped Step 3):**

1. Execute the notebook generation script using the existing canvas_content.md:
   ```bash
   python3 scripts/generate_notebook.py --template {template-directory-name}
   ```
2. Check the output to see where the notebook was saved

**If user created a new template in Step 3:**

- The notebook was already generated in Step 3, proceed to customization

#### 4.1 Customer Identification

1. Use AskUserQuestion to collect the customer/institution name:
   - question: "What is the name of the customer or institution for this demo?"
   - header: "Customer Name"
   - options:
     - Provide 2-3 generic examples based on industry:
       - Education: "State University", "Metro College", "Tech Institute"
       - Financial Services: "First National Bank", "Metro Credit Union", "Invest Partners"
     - User can select "Other" for custom input

2. Store the customer name for use in notebook customization

#### 4.2 Business Unit and Context Variables

3. Use AskUserQuestion to gather industry-specific customer context values:
   
   **For Education Industry:**
   - BUSINESS_UNIT (e.g., "Recruitment & Admissions", "Advancement", "Student Success")
   - INSTITUTION_TYPE (e.g., "Public 4-Year", "Private 4-Year", "Community College")
   - INSTITUTION_SIZE (e.g., "Small (<5,000)", "Medium (5,000-15,000)", "Large (>15,000)")
   - ACADEMIC_YEAR (e.g., "2024-2025", "2025-2026", "2026-2027")
   - DEMO_SCENARIO (e.g., "Enrollment decline and recovery", "Record growth", "Improving yield rates")

   **For Financial Services Industry:**
   - BUSINESS_UNIT (e.g., "Retail Banking", "Wealth Management", "Fraud Operations")
   - INSTITUTION_TYPE (e.g., "Regional Bank", "Credit Union", "Investment Firm")
   - INSTITUTION_SIZE (e.g., "Small (<$1B AUM)", "Medium ($1B-$10B AUM)", "Large (>$10B AUM)")
   - FISCAL_YEAR (e.g., "FY2024", "FY2025", "FY2026")
   - DEMO_SCENARIO (e.g., "Reducing fraud losses", "Improving customer retention", "Cross-sell growth")

4. Create multi-question prompts (up to 4 variables at a time) with sensible default options

#### 4.3 Customer Context File Setup

1. Inform the user about the context.md file purpose:
   - Contains additional customer background from NotebookLM or research
   - Helps generate more realistic, customer-specific demo data
   - Optional but recommended for high-quality demos

2. Use AskUserQuestion to ask if they have customer context to provide:
   - question: "Would you like to add customer context for more realistic demo data?"
   - header: "Context"
   - options:
     - label: "Yes, I'll paste my research"
       description: "Paste customer background, NotebookLM export, or meeting notes"
     - label: "No, skip for now"
       description: "Generate notebook without additional context (can add later)"

3. Based on response:
   - **If "Yes, I'll paste my research"**:
     - Use AskUserQuestion with free text input to ask:
       - question: "Paste your customer context below (NotebookLM export, meeting notes, research findings, etc.):"
       - header: "Context Content"
     - Create directory: `notebooks/customers/{customer-name-slug}/`
     - Create `context.md` file at `notebooks/customers/{customer-name-slug}/context.md`
     - Write the user's pasted content to the context.md file
     - Confirm: "✅ Created context file at notebooks/customers/{customer-name-slug}/context.md"
   - **If "No, skip for now"**:
     - Set CONTEXT_FILE to the default path `notebooks/customers/{customer-name-slug}/context.md` but note it doesn't exist yet
     - Inform user they can add context later by creating this file

4. Store the CONTEXT_FILE path for use in notebook customization

#### 4.4 Customize Notebook with Customer Data

1. Read the customer context file (if it exists) to understand customer background

2. **Update Section 1.2 (cell-3)** with all collected customer context variables:
   - Use NotebookEdit to replace the placeholder values in the generated notebook
   - Update: CUSTOMER_NAME, BUSINESS_UNIT, DEMO_SCENARIO, CONTEXT_FILE, INSTITUTION_TYPE, INSTITUTION_SIZE, ACADEMIC_YEAR (or equivalent for other industries)

3. **Generate Custom Data Generation Code for Section 2.1 (cell-7)**:
   - Based on collected information (CUSTOMER_NAME, BUSINESS_UNIT, DEMO_SCENARIO, context content), generate Python code that:
     - Creates realistic data specific to the customer
     - Uses the BUSINESS_UNIT to determine appropriate data schemas
     - Incorporates the DEMO_SCENARIO to build in the right "drama" pattern
     - References the customer_context variable loaded from context.md
     - Generates appropriate column names, realistic values, and relationships

   **Write custom Python code based on Business Unit:**

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

   **For Fraud Operations:**
   - Generate transaction/fraud detection data
   - Columns: transaction_id, transaction_date, amount, merchant, card_type, fraud_flag, risk_score
   - Apply drama pattern (e.g., fraud spike then mitigation)

4. Use NotebookEdit to replace the placeholder code in Section 2.1 (cell-7) with the generated custom code

5. **Move and rename the notebook to the customer directory**:
   - Determine customer slug from CUSTOMER_NAME (e.g., "Miami University of Ohio" → "miami-university-ohio")
   - The customer directory already exists from Step 4.3: `notebooks/customers/{customer-name-slug}/`
   - Use Bash to move and rename the generated timestamped notebook:
     - From: `notebooks/{template-name}/{template-name}_{timestamp}.ipynb`
     - To: `notebooks/customers/{customer-name-slug}/{customer-name-slug}.ipynb`
   - Example: `mv notebooks/higher-education/higher-education_20260427.ipynb notebooks/customers/miami-university-ohio/miami-university-ohio.ipynb`

6. Verify the notebook was moved successfully and confirm the new path

### Step 5: Prompt for Data Output Location

After customizing the notebook with customer context variables, determine where the generated data should be output.

1. Use the AskUserQuestion tool to ask the user where they want to output the generated data:
   - question: "Where would you like to output the generated data?"
   - header: "Output Destination"
   - options:
     - label: "PostgreSQL"
       description: "Store data in a PostgreSQL database table"
     - label: "Salesforce"
       description: "Load data directly into a Salesforce org"
     - label: "CSV (Default)"
       description: "Save data to a CSV file as backup or default option"

### Step 6: Collect Output-Specific Parameters

Based on the user's selection, collect the necessary parameters:

#### 6.1: PostgreSQL Output

If the user selects PostgreSQL:
1. Use AskUserQuestion to collect:
   - question: "What is the target PostgreSQL table name?"
   - header: "Table Name"
   - (Allow free text input or provide common options like "students", "contacts", "applications")
2. Use AskUserQuestion to collect:
   - question: "What email should be associated with this data load?"
   - header: "Email"
   - (Allow free text input)
3. Read section 9.1 of the notebook to identify the PostgreSQL data loading cell
4. Use NotebookEdit or Edit tool to update the cell with:
   - Replace `TABLE_NAME` with the provided table name
   - Replace `EMAIL` with the provided email
5. Verify the replacements were successful by reading the updated section

#### 6.2: Salesforce Output

If the user selects Salesforce:
1. Use AskUserQuestion to collect Salesforce connection information:
   - question: "What is your Salesforce org alias or username?"
   - header: "Salesforce Org"
   - (Provide common options like "dev", "staging", "production", or allow free text)
2. Use AskUserQuestion to collect:
   - question: "What is your Salesforce username?"
   - header: "Username"
   - (Allow free text input)
3. Use AskUserQuestion to collect:
   - question: "What is your Salesforce password (or security token)?"
   - header: "Password/Token"
   - (Allow free text input - note security considerations)
4. **Query the Salesforce org for schema information:**
   - Use the Bash tool to run: `sf sobject list --target-org {TARGET_ORG} --sobject all`
   - Or use Python script to query via simple-salesforce:
     ```python
     from simple_salesforce import Salesforce
     sf = Salesforce(username='...', password='...', security_token='...')
     # Get list of all objects
     objects = sf.describe()['sobjects']
     # Filter to custom and common standard objects
     relevant_objects = [obj['name'] for obj in objects if obj['createable']]
     ```
5. Parse the schema results and present common/relevant objects to the user:
   - Use AskUserQuestion to present object options:
   - question: "Which Salesforce object should we load data into?"
   - header: "Target Object"
   - options: Include objects like:
     - Contact
     - Account
     - Lead
     - Custom objects ending in `__c`
     - Education Cloud objects (if detected): `hed__Course__c`, `hed__Application__c`, etc.
6. Read section 9.2 of the notebook to identify the Salesforce data loading cell
7. Use NotebookEdit or Edit tool to update the cell with:
   - Replace `TARGET_ORG` with the provided org alias
   - Replace `USERNAME` with the provided username
   - Replace `PASSWORD` with the provided password/token
   - Replace `SALESFORCE_OBJECT` with the selected object name
8. Verify the replacements were successful by reading the updated section

#### 6.3: CSV Output (Default/Backup)

For CSV output (always offer as backup):
1. Use AskUserQuestion to collect:
   - question: "What is the desired output path for the CSV file?"
   - header: "Output Path"
   - options:
     - label: "./output/data.csv"
       description: "Default output directory"
     - label: "./exports/data_{timestamp}.csv"
       description: "Timestamped export"
     - label: "Custom path"
       description: "Specify your own path"
2. Read section 9.3 of the notebook (if it exists) to identify the CSV export cell
3. Use NotebookEdit or Edit tool to update the cell with the provided output path
4. Verify the replacements were successful

### Step 7: Verify Output Configuration

1. Read the updated notebook sections (9.1, 9.2, and/or 9.3) to verify the parameters were correctly inserted
2. Inform the user that the output configuration is complete
3. Provide a summary of the output settings configured:
   - For PostgreSQL: "Data will be loaded to table '{TABLE_NAME}' with email '{EMAIL}'"
   - For Salesforce: "Data will be loaded to '{SALESFORCE_OBJECT}' in org '{TARGET_ORG}'"
   - For CSV: "Data will be exported to '{output_path}'"

### Step 8: Completion

1. Inform the user that the notebook has been fully generated and customized

2. **Summarize what was created:**
   - "✅ Created customer-specific notebook: `{customer-name-slug}.ipynb`"
   - "Section 1.2: All customer context variables populated ({BUSINESS_UNIT}, {INSTITUTION_TYPE}, etc.)"
   - "Section 2.1: Custom Python code to generate {BUSINESS_UNIT} demo data for {CUSTOMER_NAME}"
   - "Section 9: Output destination configured ({PostgreSQL/Salesforce/CSV})"
   - "Context file: notebooks/customers/{customer-name-slug}/context.md" (if created)

3. Provide the full path to the customer-named notebook

4. **Explain how to use the notebook:**
   - "The notebook is ready to run - all code is customer-specific"
   - "Run all cells to generate your demo data for {CUSTOMER_NAME}"
   - "The data will include the '{DEMO_SCENARIO}' pattern you specified"
   - "Section 2.1 generates realistic data based on {CUSTOMER_NAME} and context.md"
   - "Section 9 exports to your configured destination"

5. Remind them:
   - The notebook is named after the customer for easy identification
   - Data will be tailored to the customer context provided
   - Review Section 2.1 code to understand the data schema before running
   - If they need to modify the data generation logic, Section 2.1 contains the custom code

6. **Automatically open the notebook in VS Code:**
   - Run: `code notebooks/customers/{customer-name-slug}/{customer-name-slug}.ipynb`
   - Inform user: "Opening {customer-name-slug}.ipynb in VS Code..."
   - The notebook will open in their editor ready to review and execute

## Important Notes

- **Existing Templates:** Check for existing canvas_content.md files in notebooks/ subdirectories before prompting to create new ones
- **Template Discovery:** Use Bash to list directories in templates/ and check for canvas_content.md files: `find templates -name "canvas_content.md" -type f`
- The generate_notebook.py script requires manual canvas export for now (future versions may support API integration)
- Be patient with the user during the manual canvas export step (only applies to new template creation)
- When replacing variables in the notebook, be careful to only replace actual placeholder variables, not arbitrary uses of those words in text
- After editing the notebook, always verify the changes were applied correctly
- **Security Consideration:** When collecting Salesforce passwords/tokens, remind the user that these will be embedded in the notebook. Suggest using environment variables or `.env` files for production use
- The Salesforce org query step requires either the Salesforce CLI (`sf`) or the `simple-salesforce` Python package
- If the notebook doesn't have sections 9.1, 9.2, or 9.3 for output configuration, the canvas template may need to be updated
- **Skip Logic:** If user selects an existing template in Step 2, skip Step 3 entirely and proceed directly to Step 4

## File Structure

Templates are stored in:
- **templates/{template-name}/**
  - **canvas_content.md** - Raw Slack canvas content (template for notebook generation)

Customer-specific files are stored together in:
- **notebooks/customers/{customer-name-slug}/**
  - **{customer-name-slug}.ipynb** - The customer-specific Jupyter notebook
  - **context.md** - Customer background from NotebookLM/research (optional)

## Notebook Sections

The generated notebooks should follow this structure:
- **Sections 1-8:** Customer context, data generation logic, and transformations
- **Section 9.1:** PostgreSQL data loading (uses TABLE_NAME, EMAIL parameters)
- **Section 9.2:** Salesforce data loading (uses TARGET_ORG, USERNAME, PASSWORD, SALESFORCE_OBJECT parameters)
- **Section 9.3:** CSV export (uses output_path parameter)

## Example Workflows

### Example 1: Using Existing Template (Education)

1. User invokes: `/notebook-from-canvas` or asks to "Generate a notebook from canvas"
2. You ask user to select industry: "Education", "Financial Services", or "New Industry"
3. User selects "Education"
4. You check templates/ directory and find existing templates with canvas_content.md files:
   - `templates/higher-education/canvas_content.md` exists
   - `templates/financial-services/canvas_content.md` exists
5. You present options: "Higher Education", "Financial Services", or "Create New from Slack Canvas"
6. User selects "Higher Education"
7. You run: `python3 scripts/generate_notebook.py --template higher-education`
8. The script generates: `notebooks/higher-education/higher-education_20260427.ipynb`
9. You identify education-specific variables: BUSINESS_UNIT, CUSTOMER_NAME, INSTITUTION_TYPE, INSTITUTION_SIZE, ACADEMIC_YEAR
10. You ask user for customer name: "State University"
11. You ask for business unit and other context: "Student Success", "Public 4-Year", "Large (>15,000)", "2025-2026", "At-risk student intervention"
12. You ask if they want to add customer context content
13. User pastes NotebookLM research about State University's retention challenges
14. You create `notebooks/customers/state-university/context.md` with their pasted content
15. You use NotebookEdit to update cell-3 with customer context variables
16. You use NotebookEdit to update cell-7 with custom Student Success data generation code
17. You move and rename the notebook: `mv notebooks/higher-education/higher-education_20260427.ipynb notebooks/customers/state-university/state-university.ipynb`
18. You ask where to output data: "PostgreSQL", "Salesforce", or "CSV"
19. User selects "Salesforce"
20. You collect: org, username, password, object name
21. You update section 9.2 of the notebook with Salesforce parameters
22. You automatically open `notebooks/customers/state-university/state-university.ipynb` in VS Code
23. You confirm success with summary showing both context.md and the customer notebook are co-located

### Example 2: Creating New Template from Slack Canvas

1. User invokes the skill
2. You ask user to select industry: "Education", "Financial Services", or "New Industry"
3. User selects "New Industry"
4. You ask for Slack Canvas ID or URL
5. User provides: "F0BXC9KK2WY"
6. You ask for template name
7. User provides: "wealth-management"
8. You create directory: `templates/wealth-management/`
9. You instruct user to export canvas content to `templates/wealth-management/canvas_content.md`
10. User confirms completion
11. You run: `python3 scripts/generate_notebook.py --template wealth-management`
12. The script generates temporary notebook: `notebooks/wealth-management/wealth-management_20260427.ipynb`
13. You identify variables in the notebook and collect values from user
14. You customize the notebook with user-provided values
15. You configure output destination and complete the workflow

## Error Handling

- If no industry is selected, prompt the user to select an industry first
- If no existing templates are found in notebooks/ directory for the selected industry, inform the user and offer to create a new template
- If the notebook generation script (generate_notebook.py) is not found, inform the user
- If the notebook generation fails, show the error and help the user troubleshoot
- If the manual canvas export file (canvas_content.md) is not found in the template directory (for new templates), remind the user of the steps and wait for confirmation
- If an existing template's canvas_content.md file is missing or corrupted, inform the user and suggest recreating it
- If Salesforce connection fails during schema query, inform the user and ask them to verify credentials
- If the Salesforce CLI (`sf`) is not installed or not working, fall back to asking user to manually specify the target object
- If section 9.1, 9.2, or 9.3 is not found in the notebook, inform the user that the notebook may not support that output method
- If notebook cell updates fail, show the error and verify the cell structure matches expectations
- If user provides an invalid Slack Canvas URL/ID format, parse it gracefully and extract the canvas ID portion

