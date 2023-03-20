import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_security.decorators import roles_required
from project.models import Product
from werkzeug.utils import secure_filename
from . import db
from . import forms

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/admin')
@login_required
@roles_required('admin')
def admin():
    products= Product.query.all()
    return render_template('admin.html',products=products)


@main.route('/add', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def agregar():
    create_form=forms.ProductForm(request.form)
    if request.method=='POST':
        newProduct =Product(image=create_form.image.data, 
                     name=create_form.name.data, price=create_form.price.data, 
                     stock=create_form.stock.data)
        product = Product.query.filter_by(name=create_form.name.data).first()

        if product:
            flash('Ya existe el producto')
            return redirect(url_for('add'))
        
        db.session.add(newProduct)
        db.session.commit()
        return redirect(url_for('main.admin'))
    return render_template('add.html', form =create_form)


@main.route('/delete', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def delete():
    create_form=forms.ProductForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        productInfo=db.session.query(Product).filter(Product.id==id).first()
        create_form.id.data=id
        create_form.image.data=productInfo.image
        create_form.name.data=productInfo.name
        create_form.price.data=productInfo.price
        create_form.stock.data=productInfo.stock
        create_form.active.data=productInfo.active
    
    if request.method=='POST':
        id=create_form.id.data
        product=Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        flash('Producto eliminado correctamente')

        return redirect(url_for('main.admin'))
    return render_template('delete.html', form = create_form)

@main.route('/edit', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def update():
    create_form=forms.ProductForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        productInfo=db.session.query(Product).filter(Product.id==id).first()
        create_form.id.data=id
        create_form.image.data=productInfo.image
        create_form.name.data=productInfo.name
        create_form.price.data=productInfo.price
        create_form.stock.data=productInfo.stock
        create_form.active.data=productInfo.active
    
    if request.method=='POST':
        id=create_form.id.data
        newProduct=db.session.query(Product).filter(Product.id==id).first()
        newProduct.image=create_form.image.data
        newProduct.name=create_form.name.data
        newProduct.price=create_form.price.data
        newProduct.stock=create_form.stock.data
        newProduct.active=create_form.active.data

        db.session.add(newProduct)
        db.session.commit()

        return redirect(url_for('main.admin'))
    return render_template('edit.html', form = create_form)
   

@main.route('/products')
@login_required
@roles_required('customer')
def products():
    products= Product.query.all()
    return render_template('products.html',products=products)

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')
