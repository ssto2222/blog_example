import os, json
from flask import request, redirect, url_for, render_template, flash, session, abort
from flask_login import  login_required, current_user
from tech2metailblog import db
from tech2metailblog.models import Books, BooksPost
from tech2metailblog.books.forms import BooksPostForm
from flask import Blueprint
from tech2metailblog.books.spread_sheet import create_df
import pandas as pd


books = Blueprint('books', __name__)
bookspost = Blueprint('bookspost', __name__)

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

def add_books():
    if current_user.username == admin_user:
        form = BooksPostForm()
        if request.method == 'POST':
            books = Books(
                title = form.title.data,
                author = form.author.data,
                published_by = form.published_by.data,
                published_at = form.published_at.data,
                img_link = form.img_link.data,
                pur_link = form.ecsite_link.data
            )
            
            db.session.add(books)
            db.session.commit()
            flash('新しく本が登録されました')
            return redirect(url_for('books.show_books'))
        return render_template('books/new.html',form=form)

@books.route('/books/book_id=<int:book_id>', methods=['GET'])
def show_book(book_id):
    bookspost = BooksPost.query.get(book_id)
    book = Books.query.get_or_404(book_id)
    return render_template('books/show.html', book=book, bookspost=bookspost,admin_user=admin_user)

@books.route('/books/<int:id>/edit', methods=['GET'])
@login_required
def edit_books(id):
    book = Books.query.get(id)
    return render_template('books/edit.html', book=book)
 

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

################################################
#### Books details 
#################################

@bookspost.route('/books/<int:book_id>/create_post',methods=['GET','POST'])
@login_required
def create_post(book_id):
    if current_user.username == admin_user:
        form = BooksPostForm()
        book = Books().query.get_or_404(book_id)
        if request.method == 'POST': 
            bookspost = BooksPost(
                book_id=book.id,
                user_id=current_user.id,
                title=form.title.data,
                text=form.text.data
            )
            
            db.session.add(bookspost)
            db.session.commit()
            flash('本詳細説明が作成されました。')
            return redirect(url_for('books.show_book',id=book.id))
        
        return render_template('books/create_post.html',form=form, book=book)

@bookspost.route('/books/book_id=<int:book_id>/<int:bookspost_id>/update', methods=['GET','POST'])
@login_required

def update_post(book_id,bookspost_id):
     if current_user.username == admin_user:
        form = BooksPostForm()
        bookspost = BooksPost.query.get_or_404(bookspost_id)
        book= Books.query.get(book_id)
        if request.method == 'POST':
            bookspost.title = form.title.data
            bookspost.text = form.text.data

            db.session.commit()
            flash('本への投稿完了')

        form.title.data = bookspost.title
        form.text.data = bookspost.text

        return render_template('books/books_post.html', form=form, book_id=book.id,bookspost_id=bookspost.id)


#delete
@bookspost.route('/books/book_id=<int:book_id>/<int:bookspost_id>/delete',methods=['GET', 'POST'])
@login_required
def delete_post(book_id, bookspost_id):
    bookspost = BooksPost.query.get_or_404(bookspost_id)
    if current_user.username != admin_user:
        abort(403)
        
    db.session.delete(bookspost)
    db.session.commit()
    flash('本詳細を削除しました。')
    return redirect(url_for('books.show_shelf'))