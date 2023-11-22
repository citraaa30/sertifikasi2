from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # Ganti URL MongoDB sesuai kebutuhan
db = client['mydatabase']  # Ganti nama database sesuai kebutuhan
collection = db['mycollection']  # Ganti nama collection sesuai kebutuhan

# Halaman utama
@app.route('/')
def index():
    data = collection.find()
    return render_template('index.html', data=data)

# Halaman tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        collection.insert_one({'name': name, 'age': age})
        return redirect(url_for('index'))
    return render_template('add.html')

# Halaman update data
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    data = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        new_name = request.form['name']
        new_age = request.form['age']
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'name': new_name, 'age': new_age}})
        return redirect(url_for('index'))
    return render_template('update.html', data=data)

# Halaman hapus data
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
