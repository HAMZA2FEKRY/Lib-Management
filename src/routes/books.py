import json
from flask import Blueprint, jsonify, request

books_bp = Blueprint('books', __name__, url_prefix='/api/books')
dataset = 'src/models/books.json'


def load_books():
    with open(dataset, 'r') as file:
        return json.load(file)

def save_books(books):
    with open(dataset, 'w') as file:
        json.dump(books, file, indent=4)


@books_bp.route('', methods=['GET'])
def list_books():
    return jsonify(load_books()), 200

@books_bp.route('/search', methods=['GET'])
def search_books():
    books = load_books()
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')
    filtered_books = [
        book for book in books
        if (not author or book['author'] == author) and
           (not published_year or str(book['published_year']) == published_year) and
           (not genre or book['genre'] == genre)
    ]
    return jsonify(filtered_books), 200

@books_bp.route('', methods=['POST'])
def add_book():
    new_book = request.json
    required_fields = ['title', 'author', 'published_year', 'isbn']
    if not all(field in new_book for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    books = load_books()
    books.append(new_book)
    save_books(books)
    return jsonify({"message": "Book added successfully"}), 201

@books_bp.route('/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = load_books()
    updated_books = [book for book in books if book['isbn'] != isbn]
    if len(books) == len(updated_books):
        return jsonify({"message": "Book not found"}), 404
    save_books(updated_books)
    return jsonify({"message": "Book deleted successfully"}), 200

@books_bp.route('/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    updated_data = request.json
    books = load_books()
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_data)
            save_books(books)
            return jsonify({"message": "Book updated successfully"}), 200
    return jsonify({"message": "Book not found"}), 404
