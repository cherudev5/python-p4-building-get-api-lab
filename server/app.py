#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries=[]
    for bakery in Bakery.query.all():
        bakery_dict={
            "id":bakery.id,
            "name":bakery.name,
            "created_at":bakery.created_at
            
        }
        bakeries.append(bakery_dict)
    
    return jsonify(bakeries),200


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at':bakery.created_at,
        'baked_goods':[good.name for good in bakery.baked_goods]
    }
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = []
    for good in baked_goods:
        good_data = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': good.created_at,
            'bakery_id': good.bakery_id
        }
        goods_list.append(good_data)
    return jsonify(goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_good:
        good_data = {
            'id': most_expensive_good.id,
            'name': most_expensive_good.name,
            'price': most_expensive_good.price,
            'created_at': most_expensive_good.created_at,
            'bakery_id': most_expensive_good.bakery_id
        }
        return jsonify(good_data)
    else:
        return jsonify({"error": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
