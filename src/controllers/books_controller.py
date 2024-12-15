import json
from flask import jsonify, request


database = 'src/models/books.json'

def load_books():
    with open(database, 'r') as file:
        return json.load(file)

def save_books(books):
    with open(database, 'w') as file:
        json.dump(books, file, indent=4)

def add_book():
    data = request.json
    required_fields = ['title', 'author', 'published_year', 'isbn']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    books = load_books()
    books.append(data)
    save_books(books)
    return jsonify({"message": "Book added successfully"}), 201

def list_books():
    return jsonify(load_books())

def search_books():
    books = load_books()
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')
    filtered = [
        book for book in books
        if (not author or book['author'] == author) and
           (not published_year or str(book['published_year']) == published_year) and
           (not genre or book.get('genre') == genre)
    ]
    return jsonify(filtered)

def delete_book(isbn):
    books = load_books()
    updated_books = [book for book in books if book['isbn'] != isbn]
    if len(books) == len(updated_books):
        return jsonify({"message": "Book not found"}), 404
    save_books(updated_books)
    return jsonify({"message": "Book deleted successfully"})

def update_book(isbn):
    data = request.json
    books = load_books()
    for book in books:
        if book['isbn'] == isbn:
            book.update(data)
            save_books(books)
            return jsonify({"message": "Book updated successfully"})
    return jsonify({"message": "Book not found"}), 404
