from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from . models import User
from . import db, userDataStore
from . import forms

auth = Blueprint('auth', __name__)

@auth.route('/sesion', methods=['POST', 'GET'])
def login():
    create_form=forms.LoginForm(request.form)
    if request.method=='POST':
        email=create_form.email.data
        password=create_form.password.data
        remember = True if create_form.remember.data else False
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('El usuario y/o la contraseña son incorrectos')
            return redirect(url_for('auth.login', form = create_form)) 
        
        login_user(user, remember=remember)
        return redirect(url_for('main.products', current_user = current_user))
    return render_template('login.html', form = create_form)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        newUser=User(name=create_form.name.data,
                    password=generate_password_hash(create_form.password.data, method='sha256'),
                    email=create_form.email.data)
        user = User.query.filter_by(email=create_form.email.data).first()

        if user:
            flash('Ya existe un usuario con el mismo correo')
            return redirect(url_for('auth.signup', form = create_form)) 

        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('auth.login')) 
    
    return render_template('signup.html', form = create_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['POST', 'GET'])
def profile():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        userInfo=db.session.query(User).filter(User.id==id).first()
        create_form.id.data=userInfo.id
        create_form.name.data=userInfo.name
        create_form.email.data=userInfo.email
        create_form.password.data=userInfo.password

    if request.method=='POST':
        id=create_form.id.data
        newInfo=db.session.query(User).filter(User.id==id).first()
        newInfo.email=create_form.email.data
        newInfo.name=create_form.name.data
        newInfo.password=create_form.password.data
        db.session.add(newInfo)
        db.session.commit()
        flash('Cambios guardados')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html', form = create_form)

