from flask import Blueprint, render_template, redirect, url_for, request
from extensions import mongo
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/add_item', methods=['POST','GET'])
def add_item():
    items_collection = mongo.db.items
    item = request.form['item']
    items_collection.insert_one({'text': item, 'complete': False})
    return redirect(url_for('main.index'))

@main.route('/')
def index():
    items_collection = mongo.db.items
    todo = items_collection.find({'complete': False})
    finished = items_collection.find({'complete': True})
    return render_template('index.html', items_collection=todo, done=finished)

@main.route('/complete/<oid>')
def complete(oid):
    items_collection = mongo.db.items
    todo_item = items_collection.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    items_collection.save(todo_item)
    return redirect(url_for('main.index'))

@main.route('/incomplete/<oid>')
def incomplete(oid):
    items_collection = mongo.db.items
    todo_item = items_collection.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = False
    items_collection.save(todo_item)
    return redirect(url_for('main.index'))

@main.route('/delete_completed')
def delete_completed():
    items_collection = mongo.db.items
    items_collection.delete_many({'complete' : True})
    return redirect(url_for('main.index'))

@main.route('/delete_all')
def delete_all():
    items_collection = mongo.db.items
    items_collection.delete_many({})
    return redirect(url_for('main.index'))