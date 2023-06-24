from flask import request,Flask,render_template,jsonify,redirect,url_for,jsonify
import requests
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://test:test@cluster00.aw629as.mongodb.net/?retryWrites=true&w=majority')
db = client.DbNextGen

app = Flask(__name__)
@app.route('/')
def index():
    bunch_of_words = list(db.words.find({},{'_id':False}))
    words = []
    for word in bunch_of_words:
        definition = word['definitions'][0]['shortdef']
        # Jadi kadang kadang data definisi dapat hanya berupa string, jadi untuk memastikan ditambahlah if argument
        if type(definition) is str:
            definition = definition  
        else:
            definition[0]
        words.append({
            'word': word['word'], # Mengakses judul atau kata saja
            'definition': definition,
        })
    msg = request.args.get('msg')
    return render_template('index.html',saved=words,msg=msg)

@app.route('/detail/<keyword>')
def detail(keyword):
    status = request.args.get('status_give','new')
    api_key = '0a6c2cae-533a-427b-b36a-9f21b331da9d'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()
    if not definitions:
        # return redirect(url_for('index',msg=f'Could not find the word, you looking for. "{keyword}" does not exist'))
        return redirect(url_for('erno',word=keyword))
    if type(definitions[0]) is str:
        suggestions = ','.join(definitions)
        # return redirect(url_for('index',msg=f'Could not find the word, you looking for. Did you mean {suggestions}'))
        return redirect(url_for('erno',word=keyword,suggests=suggestions))
    return render_template('detail.html',word=keyword,definitions=definitions,status=status)

@app.route('/api/save_word',methods=['POST'])
def save_word():
    today = datetime.now().strftime('%A_%d_%m_%Y %H:%M:%S')
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    doc = {
        'word': word,
        'definitions': definitions,
        'date': today,
    }
    db.words.insert_one(doc)

    return jsonify({'msg':f'the word, {word}, was saved','status':'success'})

@app.route('/api/del_word',methods=['POST'])
def del_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word':word})
    return jsonify({'msg':f'the word, {word}, was deleted successfully','status':'success'})

@app.route('/error')
def erno():
    word = request.args.get('word')
    if 'suggests' not in request.args:
        return render_template('error.html',word=word)
    else:
        suggestions = request.args.get('suggests')
        suggests = suggestions.split(',')
        return render_template('error.html',word=word,suggests=suggests)
    
    
# @app.route('/practice')
# def practice():
#     return render_template('practice.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=8080,debug=True)