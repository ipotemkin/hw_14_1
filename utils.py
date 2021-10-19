import sqlite3
from errors import ValidationError
from __init__ import app


def run_sql(sql: str):
    conn = sqlite3.connect(app.config['DB_FILE'])
    cursor = conn.cursor()
    results = cursor.execute(sql).fetchall()
    conn.close()
    return results


def make_results(*fields, data: list):
    if len(fields) != len(data[0]):
        raise ValidationError
    results = []
    for line in data:
        results_line = {}
        for i, field in enumerate(fields):
            results_line[field] = line[i]
        results.append(results_line)
    return results
