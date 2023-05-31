import psycopg2
from django.conf import settings


class SchemaDatabase:
    def __init__(self, schema_name):
        db = settings.DATABASES
        db = db["default"]
        self.dbname = db.get("NAME")
        self.user = db.get("USER")
        self.password = db.get("PASSWORD")
        self.host = db.get("HOST")
        self.port = db.get("PORT}")
        self.schema_name = schema_name

    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            options=f"-c search_path={self.schema_name}",
        )
        self.coursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return self.coursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


# Usage
# with DatabaseConnection("your_database", "your_username", "your_password", "your_host", "5432") as conn:
#     # You can use the 'conn' object for database operations here
#     pass
