from flask import Flask
from flask import request
import psycopg2
import sqlite3

app = Flask(__name__)
url = "postgresql://jelani:NRuQTD22a3wc42z1j_cLdw@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/ingredients?sslmode=verify-full&options=--cluster%3Dhunter-codfish-3992&sslrootcert=root.crt"
print('here1')
conn = psycopg2.connect(url)
print('here2')
c = conn.cursor()
print('here3')

def similar(full, typed):
    return typed in full 

def find_similar_name(name, value):
    # find all similar names of the ingredient to value
    ingredients = []
    all_names = []
    print('here4')
    c.execute('SELECT * from ingredients')
    print('here5')
    records = c.fetchall()
    print('here6')
    all_names = [r[0] for r in records]
    for n in all_names:
        if similar(n, value):
            ingredients.append(n)
    return {"ingredients" : ingredients}
    
@app.route("/nameEntry", methods=['GET'])
def name_entry():
    key = list(request.args.keys())[0]
    value = list(request.args.values())[0]
    return find_similar_name(key, value)

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

if __name__ == "__main__":
    app.run()