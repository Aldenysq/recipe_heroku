from flask import Flask
from flask import request
import psycopg2
import sqlite3
import json

app = Flask(__name__)
url = "postgresql://jelani:NRuQTD22a3wc42z1j_cLdw@free-tier4.aws-us-west-2.cockroachlabs.cloud:26257/ingredients?sslmode=verify-full&options=--cluster%3Dhunter-codfish-3992&sslrootcert=root.crt"
conn = psycopg2.connect(url)
c = conn.cursor()

def similar(full, typed):
    print(typed, full)
    return typed in full 

def find_similar_name(name, value):
    # find all similar names of the ingredient to value
    ingredients = []
    all_names = []
    c.execute('SELECT * from ingredients')
    records = c.fetchall()
    all_names = [r[0] for r in records]
    for n in all_names:
        if n and similar(n, value):
            ingredients.append(n)
    return {"ingredients" : ingredients}
    
@app.route("/nameEntry", methods=['GET'])
def name_entry():
    key = list(request.args.keys())[0]
    value = list(request.args.values())[0]
    return find_similar_name(key, value)

weights = {
    "ounce": 2,
    "cup": 2,
    "teaspoon" : 1,
    "tablespoon": 1,
    "pound": 3,
    "pinch": 1,
    "can": 3,
    "package": 3,
    "slice": 1,
    "pint": 1,
    "clove": 1,
    "stick": 1,
    "stalk": 1,
    "dash": 1,
    "piece": 1,
    "gram": 2,
    "head": 3,
    "quart": 3,
    "ear": 2,
    "strip": 1,
    "box": 3,
    "ml": 2,
    "sprig": 1,
    "bunch": 3,
    "dozen": 3,
    "bottle": 2,
    "handful": 3,
    "fillet": 1,
    "bag": 3,
    "gallon": 3,
    "loaf": 1,
    "bulb": 1,
    "none": 1
}

def same_ing(name1, name2):
    return name1 in name2 or name1[:-1] in name2 #account for plurals

def comp(to, have):
    cost = 0
    for not_us in to:
        left_to_buy = not_us[2] * weights[not_us[1]]
        name = not_us[0]
        for us in have:
            if same_ing(us["name"], name):
                left_to_buy -= int(us["quantity"]) * weights[us["unit"]]
        left_to_buy = max(left_to_buy, 0)
        cost += left_to_buy
    return cost

def find_closest(have):
    c.execute('SELECT * from parsed_ingredients')
    parsed_ingredients = c.fetchall()
    # collect with same id
    d = {}
    for p in parsed_ingredients:
        e = d.get(p[0], [])
        e.append(p[1:4])
        d[p[0]] = e
    all_entries = []
    for ing_id in d:
        all_entries.append([ing_id, d[ing_id]])
    all_entries = sorted(all_entries, key= lambda x: comp(x[1], have))
    # for e in all_entries:
    #     print(comp(e[1], have), e[1])
    c.execute('SELECT * from recipes')
    recipes = c.fetchall()
    recipes_d = {}
    for r in recipes:
        recipes_d[r[1]] = (r[0], r[2], r[3]) #name, url, instructions
    return_arr = {'ret' : []}
    for i in range(14):
        return_arr['ret'].append({
            'name': recipes_d[all_entries[i][0]][0],
            'url': recipes_d[all_entries[i][0]][1],
            'instructions': recipes_d[all_entries[i][0]][2],
            'ingredients': all_entries[i][1] #name, unit, quanitty
            })
    return return_arr

@app.post("/closest")
def closest_recipe():
    return find_closest(json.loads(request.data)['ingredients'])

@app.route("/")
def home_view():
    return "<h1>Welcome to our api :)</h1>"

if __name__ == "__main__":
    app.run()