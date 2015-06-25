#!flask/bin/python
from flask import Flask, jsonify
import food_parser

app = Flask(__name__)

entrees, nutrition_facts = food_parser.get_dining_info()


@app.route('/caldining/api/v1.0/entrees', methods=['GET'])
def get_tasks():
    return jsonify({'entrees': entrees})

@app.route('/caldining/api/v1.0/nutrition_facts', methods=['GET'])
def get_nutrition_facts():
    return jsonify({'nutrition_facts': nutrition_facts})

if __name__ == '__main__':
    app.run(debug=True)

