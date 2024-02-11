from flask import *
from flask_sqlalchemy import *
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#create book class with it's parameters
class book(db.model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

#default page
@app.route('/')
def index():
    return "hello"

#page with list of books
@app.route('/books')
def get_books():
    books = Books.query.all()

    output = []
    for book in books:
        book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)

    return {'books': output}

#page of specific book
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'name': book.name, 'author': book.author, 'publisher': book.publisher}

#add book to list
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

#remove book from list
@app.route('/books/<id>', methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)
    if book is None:
        return 'book not found'
    db.session.delete(book)
    db.session.commit()

