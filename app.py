from flask import Flask, jsonify, request
from matplotlib.pyplot import title
from datos_dummy import books  #variable diccionario del otro script

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros

@app.route('/api/v0/resources/books/all', methods=['GET'])
def get_all():
    return jsonify(books)

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada

@app.route('/api/v0/resources/book', methods=['GET'])

def book_id():

    results = []
    if 'id' in request.args:
        id = int(request.args['id'])
        for book in books:
            if book['id']== id:
                results.append(book)
                
        if results == []:
            return 'Book not found'
        else:
            return jsonify(results)
    else: 
        return 'No id'



# 3.Ruta para obtener un libro concreto mediante su título como parámetro e
# n la llamada de otra forma

@app.route('/api/v0/resources/book/<string:title>', methods=['GET'])
def book_title(title):

    results = [] 

    for book in books: 
        if book['title']== title:
            results.append(book)
       
    if results != []:
        return jsonify(results)
    else:
        return 'Book title not found'

    
# 4.Ruta para obtener un libro concreto mediante su título dentro del cuerpo de la llamada

@app.route('/api/v0/resources/book', methods=['GET'])

def book_title_body():

    results = [] 
    title = request.get_json()['title']
    for book in books: 
        if book['title']== title:
            results.append(book)
    if results != []:
        return jsonify(results)
    else:
        return 'Book title not found'

# 5.Ruta para añadir un libro mediante parámetros en la llamada


@app.route('/api/v0/resources/book/add', methods=['POST'])

def post_book ():
    data = request.get_json()
    books.append(data)
    return jsonify(books)
    #request.post('http://127.0.0.1:5000/api/v0/resources/book/add', data = {'id': 3,'title': 'El arte de la guerra','author': 'Sun Tzu ','first_sentence': 'to wound the autumnal city.','published': '1975'})
    
# 6.Ruta para añadir un libro de otra forma 1

@app.route('/api/v0/resources/book/add_parameters', methods=['POST'])
def post_book_parameters ():
    data= {}
    data['id']= request.args['id']
    data['title']= request.args['title']
    data['author']= request.args['author']
    data['first_sentence']= request.args['first_sentence']
    data['published']= request.args['published']
    books.append(data)


# 7.Modificar

@app.route('/api/v0/resources/book/update', methods=['PUT'])
def put_book ():
    year = request.args['year']
    title = request.args['title']

    for book in books:
        if book['title'] == title:
            book['published'] == year
        return jsonify(books)


# 8.Ruta para eliminar un libro

@app.route('/api/v0/resources/book/delete', methods=['DELETE'])

def delete_book ():
    if title in request.args:
        title = request.args['title']
        for book in books:
            if book['title'] == title:
                books.remove(book)
                return jsonify(books)
    else: 
        return 'talta un titulo del libro'

app.run()