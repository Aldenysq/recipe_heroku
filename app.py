from flask import Flask
from flask import request
import psycopg2
import sqlite3
import os

app = Flask(__name__)
url = "postgresql://jelani:NRuQTD22a3wc42z1j_cLdw@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/ingredients?sslmode=verify-full&options=--cluster%3Dhunter-codfish-3992"
conn = psycopg2.connect(url)
c = conn.cursor()

def similar(full, typed):
    return typed in full 

def find_similar_name(name, value):
    # find all similar names of the ingredient to value
    ingredients = []
    all_names = []
    c.execute('SELECT * from ingredients')
    records = c.fetchall()
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