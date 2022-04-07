import os, json
from flask import request, redirect, url_for, render_template, flash, session
from flask_login import  login_required, current_user
from tech2metailblog import db
from tech2metailblog.models import Books
from tech2metailblog.books.forms import BooksPostForm
from flask import Blueprint
from tech2metailblog.books.spread_sheet import create_df
import pandas as pd


books = Blueprint('books', __name__)

'''
basedir = os.getcwd()
print(basedir)
l = basedir.split('/')
del l[-1]
l_new = l[0]
for i in range(len(l)):
    l_new = os.path.join(l_new,l[i])
basedir = os.path.join("/",l_new)
dir = os.path.join(basedir,'secrets')
json_file = os.path.join(dir,"admin.json")
open_json = open(json_file,'r')
'''
admin_user = os.getenv('ADMIN_USER_NAME')

@books.route('/bookshelf')
def create_bookshelf():
    df=create_df()
    rows = df.shape[0]
    for i in range(1,rows+1):
        dict = df[:i:].to_dict()
        try:
            books= Books(
                title = dict['title'][i],
                author = dict['author_family'][i] + " " + dict['author_first'][i],
                published_by = dict['published_by'][i],
                published_at = dict['published_at'][i],
                img_link = dict['img_link'][i],
                pur_link = dict['pur_link'][i]
            )
            db.session.add(books)
            db.session.commit()
            flash('データ作成完了')
        except:
            continue
    return redirect(url_for('books.show_books'))

@books.route('/books/shelf')
def show_shelf():
    books = Books.query.all()
    return render_template('books/shelf.html', books=books)
   
@books.route('/books')
@login_required
def show_books():
    if current_user.username == admin_user:
        books = Books.query.all()
        return render_template('books/index.html', books=books)
    else:
        return render_template('error_pages/403.html')
        
    
@books.route('/books/new', methods=['GET','POST'])
@login_required

def new_book():
    form = BooksPostForm()
    return render_template('books/new.html', form=form)

@books.route('/books', methods=['POST'])
@login_required

def add_books():
    books = Books(
        title = request.form['title'],
        author = request.form['author'],
        published_by = request.form['published_by'],
        published_at = request.form['published_at'],
        img_link = request.form['img_link'],
        pur_link = request.form['pur_link'],
        text = request.form['text']  
    )
    
    db.session.add(books)
    db.session.commit()
    flash('新しく記事が作成されました')
    return redirect(url_for('books.show_books'))

@books.route('/books/<int:id>', methods=['GET'])
def show_book(id):
    book = Books.query.get(id)
    return render_template('books/show.html', book=book)

@books.route('/books/<int:id>/edit', methods=['GET'])
@login_required
def edit_books(id):
    book = Books.query.get(id)
    return render_template('books/edit.html', book=book)

@books.route('/books/<int:id>/post', methods=['GET','POST'])
@login_required
def post_books(id):
    user = current_user
    form = BooksPostForm()
    book = Books.query.get(id)
    if request.method == 'POST':
        return render_template('books/post.html', book=book, user=user)
    
    return render_template('create_post.html',form=form)
   

@books.route('/books/<int:id>/update', methods=['POST'])
@login_required
def update_books(id):
    books = Books.query.get(id)
    books.title = request.form.get('title')
    books.author = request.form.get('author')
    books.published_by = request.form.get('published_by')
    books.published_at = request.form.get('published_at')
    books.img_link = request.form.get('img_link')
    books.pur_link = request.form.get('pur_link')
    
    db.session.merge(books)
    db.session.commit()
    flash('タイトル : {} の記事を更新しました'.format(books.title))
    return redirect(url_for('books.show_books'))

@books.route('/books/<int:id>/delete', methods=['POST'])
@login_required
def delete_books(id):
    books = Books.query.get(id)
    
    db.session.delete(books)
    db.session.commit()
    flash('タイトル : {} の記事を削除しました'.format(books.title))
    return redirect(url_for('books.show_books'))