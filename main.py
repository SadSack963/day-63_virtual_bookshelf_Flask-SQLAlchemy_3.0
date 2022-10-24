from flask import Flask, render_template, request, redirect, url_for
# pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os

# See https://docs.sqlalchemy.org/en/14/core/engines.html#sqlite
# SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.
#   As SQLite connects to local files, the URL format is slightly different.
#   The “file” portion of the URL is the filename of the database.
#   For a relative file path, this requires three slashes.
DB_URI = 'sqlite:///new-books-collection.db'

# Create the Flask application
app = Flask(__name__)
# See https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI  # configure the SQLite database, relative to the app instance folder
# app.config['SQLALCHEMY_ECHO'] = True  # Echo log to console
db = SQLAlchemy(app)  # create the SQLAlchemy object, passing the application to it
# print(app.config)

# Alternative (recommended) code
# # create the extension
# db = SQLAlchemy()
# # create the app
# app = Flask(__name__)
# # configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
# # initialize the app with the extension
# db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Book: {self.title}>'


# Create the database file and tables
# This code must come _after_ the class definition
if not os.path.isfile(DB_URI):
    with app.app_context():
        db.create_all()


# ROUTES
# ======

@app.route('/')
def home():
    # Get a list of all books in the database
    all_books = db.session.query(Books).all()
    # all_books = Books.query.all()
    print(all_books)
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        # Get data from the "name" parameters in the form <input> fields
        # Create a new book object and store it in the database file
        db.session.add(
            Books(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating']
            )
        )
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == 'POST':
        # Get data from the "name" parameters in the form <input> fields and update the rating
        Books.query.get(request.form['book_id']).rating = request.form['new_rating']
        db.session.commit()  # Write to database file
        return redirect(url_for('home'))
    # Get book_id from the argument in the <a> tag and find the book in the database
    book = Books.query.get(request.args.get('book_id'))
    return render_template('edit_rating.html', book=book)


@app.route("/delete")
def delete_book():
    # Get book_id from the argument in the <a> tag, find the book in the database and delete it
    db.session.delete(Books.query.get(request.args.get('book_id')))
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit_title", methods=["GET", "POST"])
def edit_title():
    if request.method == 'POST':
        # Get data from the "name" parameters in the form <input> fields and update the rating
        Books.query.get(request.form['book_id']).title = request.form['new_title']
        db.session.commit()  # Write to database file
        return redirect(url_for('home'))
    # Get book_id from the argument in the <a> tag and find the book in the database
    book = Books.query.get(request.args.get('book_id'))
    return render_template('edit_title.html', book=book)


@app.route("/test", methods=["GET", "POST"])
def test():
    print("Running test()")
    all_books = db.session.query(Books).all()
    print(f'{all_books = }')
    book = Books.query.filter_by(title="Harry Potter").first()
    print(f'{book = }')
    book_to_update = Books.query.filter_by(title="Harry Potter").first()
    book_to_update.title = "Harry Potter - Prisoner of Azkaban"
    db.session.commit()
    all_books = db.session.query(Books).all()
    print(f'{all_books = }')
    print("Finished test()")

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='localhost', port=5004, debug=False)
    pass
