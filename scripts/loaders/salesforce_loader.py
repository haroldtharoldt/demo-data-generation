"""
Salesforce Data Loader

Handles loading DataFrames to Salesforce objects via the Bulk API.
"""

from simple_salesforce import Salesforce
import pandas as pd
from typing import List, Dict, Any


class SalesforceLoader:
    """Load data into Salesforce objects"""

    def __init__(self, username, password, security_token=None, domain='login'):
        """
        Initialize Salesforce connection

        Args:
            username: Salesforce username
            password: Salesforce password
            security_token: Salesforce security token (optional if IP whitelisted)
            domain: 'login' for production, 'test' for sandbox
        """
        self.username = username
        self.password = password
        self.security_token = security_token
        self.domain = domain
        self.sf = None

    def connect(self):
        """Establish Salesforce connection"""
        if not self.sf:
            # Combine password and security token if provided
            password = self.password
            if self.security_token:
                password = f"{self.password}{self.security_token}"

            self.sf = Salesforce(
                username=self.username,
                password=password,
                domain=self.domain
            )

    def get_object_schema(self, object_name):
        """
        Get schema information for a Salesforce object

        Args:
            object_name: Name of the Salesforce object (e.g., 'Contact', 'Account')

        Returns:
            dict: Object schema information
        """
        self.connect()
        return self.sf.__getattr__(object_name).describe()

    def list_objects(self, createable_only=True):
        """
        List available Salesforce objects

        Args:
            createable_only: Only return objects that can be created

        Returns:
            list: List of object names
        """
        self.connect()
        objects = self.sf.describe()['sobjects']

        if createable_only:
            objects = [obj for obj in objects if obj['createable']]

        return [obj['name'] for obj in objects]

    def load_data(self, df, object_name, batch_size=200):
        """
        Load DataFrame to Salesforce object using Bulk API

        Args:
            df: pandas DataFrame to load
            object_name: Target Salesforce object (e.g., 'Contact', 'Account')
            batch_size: Number of records per batch (max 200 for Bulk API)

        Returns:
            dict: Summary of results with successes and errors
        """
        self.connect()

        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')

        # Clean up records (remove None values, convert types)
        cleaned_records = []
        for record in records:
            cleaned = {k: v for k, v in record.items() if pd.notna(v)}
            cleaned_records.append(cleaned)

        # Bulk insert using Salesforce Bulk API
        results = self.sf.bulk.__getattr__(object_name).insert(
            cleaned_records,
            batch_size=batch_size
        )

        # Analyze results
        successes = [r for r in results if r['success']]
        errors = [r for r in results if not r['success']]

        summary = {
            'total': len(results),
            'successes': len(successes),
            'errors': len(errors),
            'error_details': errors[:10]  # First 10 errors
        }

        return summary

    def update_data(self, df, object_name, batch_size=200):
        """
        Update existing Salesforce records

        Args:
            df: pandas DataFrame with 'Id' column for records to update
            object_name: Target Salesforce object
            batch_size: Number of records per batch

        Returns:
            dict: Summary of results
        """
        self.connect()

        if 'Id' not in df.columns:
            raise ValueError("DataFrame must contain 'Id' column for updates")

        records = df.to_dict('records')
        cleaned_records = []
        for record in records:
            cleaned = {k: v for k, v in record.items() if pd.notna(v)}
            cleaned_records.append(cleaned)

        results = self.sf.bulk.__getattr__(object_name).update(
            cleaned_records,
            batch_size=batch_size
        )

        successes = [r for r in results if r['success']]
        errors = [r for r in results if not r['success']]

        return {
            'total': len(results),
            'successes': len(successes),
            'errors': len(errors),
            'error_details': errors[:10]
        }

    def query(self, soql_query):
        """
        Execute a SOQL query

        Args:
            soql_query: SOQL query string

        Returns:
            pandas DataFrame with query results
        """
        self.connect()
        results = self.sf.query_all(soql_query)

        if results['totalSize'] == 0:
            return pd.DataFrame()

        return pd.DataFrame(results['records']).drop('attributes', axis=1)

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Salesforce connection doesn't need explicit close
        pass
