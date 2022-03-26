from flask import render_template,url_for,flash,request,redirect,Blueprint,abort
from flask_login import current_user,login_required
from tech2metailblog import db
from tech2metailblog.models import Contact
from tech2metailblog.contacts.forms import ContactUserForm

contacts= Blueprint('contacts',__name__)

@contacts.route("/contact",methods=['GET','POST'])
@login_required
def contact():
    form = ContactUserForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            if form.email.data == current_user.email:
                print('正常')   
                contact=Contact(
                    username = form.username.data,
                    email = form.email.data,
                    title = form.title.data,
                    text = form.text.data
                    )
                
                db.session.add(contact)
                db.session.commit()
                flash('お問合せメールを送信しました。')
                return redirect(url_for('core.index'))
            else:
                flash('ご登録済のemailアドレスを使用して下さい。')
    
    
    return render_template('contact.html',form=form)