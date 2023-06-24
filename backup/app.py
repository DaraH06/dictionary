from flask import request,Flask,render_template,jsonify,redirect,url_for,jsonify
import requests
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:<test>@cluster00.aw629as.mongodb.net/?retryWrites=true&w=majority')
db = client.DbNextGen

app = Flask(__name__)
@app.route('/')
def main():
    
    words = list(db.dictionary.find({},{'_id':False}))

    return render_template('index.html',words=words)

@app.route('/detail/<keyword>')
def detail(keyword):
    print (keyword)
    return render_template('detail.html',word=keyword)

@app.route('/api/save_word',methods=['POST'])
def save_word():
    return jsonify({'msg':'word saved successfully','status':'success'})

@app.route('/api/del_word',methods=['POST'])
def del_word():
    return jsonify({'msg':'word deleted successfully','status':'success'})

 #@app.route('/practice')
 #def practice():
    #return render_template('practice.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)