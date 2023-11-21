from django.db import connection


def test_database_connection():
    with connection.cursor() as cursor:

        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    if result:
        print("Database connection successful!")
    else:
        print("Failed to connect to the database.")