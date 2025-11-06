"""
Constants related to SQLite database.
"""

# Connection settings
DB_POOL_SIZE = 5
DB_CONNECT_TIMEOUT = 10  # seconds
DB_MAX_OVERFLOW = 10

# Query execution settings
QUERY_TIMEOUT = 30  # seconds

# Database file path - this could be moved to settings/config.py instead
SQLITE_DB_FILE = "project_management.db"
