from flask import Flask, request, jsonify

app = Flask(__name__)

class Book:
    def __init__(self, title, author, ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN
    
    def display_info(self):
        return {
            "title": self.title,
            "author": self.author,
            "ISBN": self.ISBN,
        }

class EBook(Book):
    def __init__(self, title, author, ISBN, file_format):
        super().__init__(title, author, ISBN)
        self.file_format = file_format
    
    def display_info(self):
        info = super().display_info()
        info["fileFormat"] = self.file_format
        return info

class Library:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
        print("Book added to library:", book.display_info())
    
    def display_books(self):
        return [book.display_info() for book in self.books]
    
    def delete_book(self, ISBN):
        self.books = [book for book in self.books if book.ISBN != ISBN]
    
    def search_by_title(self, title):
        return [book.display_info() for book in self.books if title in book.title]

library = Library()

@app.route("/addBook", methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    ISBN = data.get("ISBN")
    file_format = data.get("fileFormat")
    
    
    if not (title and author and ISBN):
        return jsonify({"status": 400, "message": "Sorry! Provide book details"}), 400
    
    book = EBook(title, author, ISBN, file_format)
    library.add_book(book)
    return jsonify({"status": 200, "message": "Book added successfully"}), 200

@app.route("/listBooks", methods=["GET"])
def list_books():
    print('listBooks')
    return jsonify({"status": 200, "message": "Success", "data": library.display_books()}), 200

@app.route("/deleteBook", methods=["DELETE"])
def delete_book():
    ISBN = request.json.get("ISBN")
    library.delete_book(ISBN)
    return jsonify({"status": 200, "message": "Book deleted successfully"}), 200

@app.route("/title", methods=["GET"])
def search_by_title():
    title = request.json.get("title")
    books = library.search_by_title(title)
    if not books:
        return jsonify({"status": 200, "message": "Book not found with the title", "data": books}), 200
    return jsonify({"status": 200, "message": "Success", "data": books}), 200

if __name__ == "__main__":
    app.run(debug=True)
