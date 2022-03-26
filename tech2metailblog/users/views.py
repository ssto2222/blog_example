#users/views.py

from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tech2metailblog import db
from tech2metailblog.models import User, BlogPost
from tech2metailblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from tech2metailblog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

#register
@users.route("/signup",methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user =User(email=form.email.data,
                   username=form.username.data,
                   password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("ご登録ありがとうございました。")
        return redirect(url_for('users.login'))
    
    return render_template('signup.html',form=form)
    
#Login
@users.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('ログインしました。')
                
                next = request.args.get('next')
                
                if next == None or not next[0]=='/':
                    next = url_for('core.index')
                
                return redirect(next)
            else:
                flash('emailアドレスまたはパスワードが間違っています。')
                return redirect(url_for('users.login'))
            
        else:
            flash('ユーザー名が見つかりません。サインアップを行なってください。')
            return redirect(url_for('users.signup'))
        
    return render_template('login.html',form=form)

#Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


#account(update Userform)
@users.route('/account/<username>', methods=['GET','POST'])
@login_required
#
def account(username):
    flash(f'ユーザー: {current_user.username} でログイン中')
    form = UpdateUserForm()
    if form.validate_on_submit():
        username = current_user.username
        if form.picture.data:
            flash(f'new_file: {form.picture.data}')
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic
        if form.username.data != username:
            current_user.username = form.username.data
        if form.email.data != current_user.email:
            current_user.email = form.email.data
        db.session.commit()
        flash('ユーザーアカウントを更新しました。')
        return redirect(url_for('users.account',username=username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

#user's list if Blog posts
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)

