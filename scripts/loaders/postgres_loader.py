"""
PostgreSQL Data Loader

Handles loading DataFrames to PostgreSQL tables with table registration
and metadata tracking.
"""

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from datetime import datetime


class PostgreSQLDataLoader:
    """Load data into PostgreSQL database"""

    def __init__(self, host, port, database, user, password):
        """
        Initialize PostgreSQL connection

        Args:
            host: PostgreSQL server hostname
            port: PostgreSQL server port (default: 5432)
            database: Database name
            user: Database username
            password: Database password
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()

    def register_table(self, table_name, email):
        """
        Register a table with metadata tracking

        Args:
            table_name: Name of the table to register
            email: Email of the user registering the table
        """
        self.connect()

        # Create metadata table if it doesn't exist
        create_metadata_table = """
        CREATE TABLE IF NOT EXISTS _table_registry (
            table_name VARCHAR(255) PRIMARY KEY,
            registered_by VARCHAR(255),
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(create_metadata_table)

        # Register or update table
        register_query = """
        INSERT INTO _table_registry (table_name, registered_by, registered_at, last_updated)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (table_name)
        DO UPDATE SET
            last_updated = EXCLUDED.last_updated,
            registered_by = EXCLUDED.registered_by
        """
        now = datetime.now()
        self.cursor.execute(register_query, (table_name, email, now, now))
        self.connection.commit()

    def load_data(self, df, table_name, if_exists='replace'):
        """
        Load DataFrame to PostgreSQL table

        Args:
            df: pandas DataFrame to load
            table_name: Target table name
            if_exists: How to behave if table exists ('replace', 'append', 'fail')
        """
        self.connect()

        if if_exists == 'replace':
            # Drop table if it exists
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.connection.commit()

        # Use pandas to_sql for easy table creation and data insertion
        from sqlalchemy import create_engine
        engine = create_engine(
            f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        )

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=1000
        )

        engine.dispose()

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
