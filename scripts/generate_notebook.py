#!/usr/bin/env python3
"""
Generate Jupyter Notebook from Slack Canvas Template

This script reads a Slack Canvas and converts it to a Jupyter notebook,
allowing SEs to maintain templates in Slack and generate fresh notebooks locally.

Usage:
    python scripts/generate_notebook.py --template recruitment-admissions
    python scripts/generate_notebook.py --canvas-id F0AHX0JJ0SX
    python scripts/generate_notebook.py --list-templates
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print(":x: Missing required packages. Please run: pip install pyyaml")
    sys.exit(1)


def load_canvas_templates():
    """Load canvas template registry from config file"""
    config_path = Path(__file__).parent.parent / "config" / "canvas_templates.yaml"
    
    if not config_path.exists():
        print(f":x: Config file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config.get('templates', {})


def list_templates():
    """List all available canvas templates"""
    templates = load_canvas_templates()
    
    print("\n:books: Available Canvas Templates:\n")
    for key, template in templates.items():
        status = ":white_check_mark: Ready" if template['canvas_id'] != "TBD" else ":double_vertical_bar: Not yet created"
        print(f"  {key} ({status})")
        print(f"    Name: {template['name']}")
        print(f"    Business Unit: {template['business_unit']}")
        print(f"    Canvas ID: {template['canvas_id']}")
        print(f"    Description: {template['description']}")
        print()


def fetch_canvas_content_manual(canvas_id, canvas_file_path):
    """
    Fetch canvas content manually (user copies content)

    TODO: Future enhancement - integrate with Slack API to fetch automatically
    """
    print(f"\n:warning: Manual canvas export required")
    print(f":clipboard: Please follow these steps:")
    print(f"   1. Open canvas: https://salesforce.enterprise.slack.com/docs/T026QPGMQ/{canvas_id}")
    print(f"   2. Copy ALL content (⌘+A, ⌘+C)")
    print(f"   3. Save to: {canvas_file_path}")
    print(f"   4. Re-run this script\n")

    # Check if manual export exists
    canvas_path = Path(canvas_file_path)
    if canvas_path.exists():
        with open(canvas_path, 'r') as f:
            content = f.read()
        print(f":white_check_mark: Found canvas content at {canvas_path}")
        return content
    else:
        print(f":x: Canvas content not found at {canvas_path}")
        sys.exit(1)


def parse_canvas_markdown(content):
    """
    Parse canvas markdown content into notebook cells
    
    Returns list of cells with type (markdown/code) and content
    """
    cells = []
    lines = content.split('\n')
    current_cell = {"type": "markdown", "content": []}
    in_code_block = False
    
    for line in lines:
        # Detect code block boundaries (```)
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block - save it
                if current_cell["content"]:
                    cells.append({
                        "type": "code",
                        "content": '\n'.join(current_cell["content"])
                    })
                current_cell = {"type": "markdown", "content": []}
                in_code_block = False
            else:
                # Start of code block - save previous markdown
                if current_cell["content"]:
                    markdown_text = '\n'.join(current_cell["content"]).strip()
                    if markdown_text:
                        cells.append({
                            "type": "markdown",
                            "content": markdown_text
                        })
                current_cell = {"type": "code", "content": []}
                in_code_block = True
            continue
        
        # Add line to current cell
        if in_code_block:
            current_cell["content"].append(line)
        else:
            current_cell["content"].append(line)
    
    # Add final cell if it has content
    if current_cell["content"]:
        content_text = '\n'.join(current_cell["content"]).strip()
        if content_text:
            cells.append({
                "type": current_cell["type"],
                "content": content_text
            })
    
    return cells


def create_notebook(cells, metadata=None):
    """
    Create Jupyter notebook structure from parsed cells
    """
    if metadata is None:
        metadata = {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13.1"
            }
        }
    
    notebook = {
        "cells": [],
        "metadata": metadata,
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    for cell in cells:
        nb_cell = {
            "cell_type": cell["type"],
            "metadata": {},
            "source": cell["content"]
        }
        
        if cell["type"] == "code":
            nb_cell["execution_count"] = None
            nb_cell["outputs"] = []
        
        notebook["cells"].append(nb_cell)
    
    return notebook


def save_notebook(notebook, output_path):
    """Save notebook to file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    
    print(f":white_check_mark: Notebook saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Jupyter Notebook from Slack Canvas Template"
    )
    parser.add_argument(
        '--template', '-t',
        help='Template name from canvas_templates.yaml (e.g., recruitment-admissions)'
    )
    parser.add_argument(
        '--canvas-id', '-c',
        help='Direct canvas ID (e.g., F0AHX0JJ0SX)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output notebook path (default: notebooks/<template-name>-<date>.ipynb)'
    )
    parser.add_argument(
        '--list-templates', '-l',
        action='store_true',
        help='List all available canvas templates'
    )
    
    args = parser.parse_args()
    
    # List templates if requested
    if args.list_templates:
        list_templates()
        return
    
    # Validate arguments
    if not args.template and not args.canvas_id:
        print(":x: Error: Must provide either --template or --canvas-id")
        parser.print_help()
        sys.exit(1)
    
    # Get canvas ID
    canvas_id = args.canvas_id
    template_name = args.template
    
    if args.template:
        templates = load_canvas_templates()
        if args.template not in templates:
            print(f":x: Template '{args.template}' not found in registry")
            print("\nAvailable templates:")
            list_templates()
            sys.exit(1)
        
        canvas_id = templates[args.template]['canvas_id']
        template_name = args.template
        
        if canvas_id == "TBD":
            print(f":x: Template '{args.template}' doesn't have a canvas ID yet")
            print("   Please create the canvas and update canvas_templates.yaml")
            sys.exit(1)
    
    # Determine output directory and paths
    if args.output:
        output_path = Path(args.output)
        # If custom output, use same directory for canvas content
        canvas_file_path = output_path.parent / "canvas_content.md"
    else:
        # Create template-specific subdirectory
        template_dir = Path("notebooks") / (template_name or "notebook")
        template_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{template_name or 'notebook'}_{timestamp}.ipynb"
        output_path = template_dir / filename
        canvas_file_path = template_dir / "canvas_content.md"

    print(f"\n:art: Generating notebook from canvas: {canvas_id}")

    # Fetch canvas content
    content = fetch_canvas_content_manual(canvas_id, str(canvas_file_path))
    
    # Parse into cells
    print(":memo: Parsing canvas content...")
    cells = parse_canvas_markdown(content)
    print(f"   Found {len(cells)} cells ({sum(1 for c in cells if c['type'] == 'code')} code, {sum(1 for c in cells if c['type'] == 'markdown')} markdown)")
    
    # Create notebook
    print(":notebook: Creating Jupyter notebook...")
    notebook = create_notebook(cells)
    
    # Save notebook
    save_notebook(notebook, output_path)
    
    print(f"\n:tada: Success! Open your notebook:")
    print(f"   code {output_path}")
    print(f"\n   Or in Jupyter:")
    print(f"   jupyter notebook {output_path}")


if __name__ == "__main__":
    main()
    
print(":white_check_mark: File created: scripts/generate_notebook.py")