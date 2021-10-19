from flask import Flask

app = Flask(__name__)
app.config['MAX_ITEMS'] = 100
app.config['DB_FILE'] = 'netflix.db'
app.config['CATEGORIES'] = {'children': ['G'], 'family': ['PG', 'PG-13'], 'adult': ['R', 'NC-17']}
