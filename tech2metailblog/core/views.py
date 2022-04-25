# core/views.py

from flask import render_template, request, Blueprint
from tech2metailblog import db
from sqlalchemy import desc
from tech2metailblog.models import Books, BooksPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    booksposts = BooksPost.query.order_by(BooksPost.date.desc()).first()
    book = None
    if booksposts:
        book = Books.query.get_or_404(booksposts.book_id)
    return render_template('index.html',booksposts=booksposts,book=book)

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/blog')
def blog():
    return render_template('blog.html')