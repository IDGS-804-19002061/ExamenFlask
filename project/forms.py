from wtforms import Form, StringField, IntegerField, EmailField, validators, RadioField, FloatField

class UserForm(Form):
    style2={'class': 'input is-large', 'placeholder': 'Nombre'}
    style4={'class': 'input is-large', 'placeholder': 'Email'}
    style3={'class': 'input is-large', 'placeholder': 'Password'}
    style1={'class': 'input is-large', 'placeholder': 'Id'}
    id=IntegerField('id', [validators.number_range(min=1, max=20, message='valor no valido')], render_kw=style1)
    name=StringField('name', [validators.DataRequired(message='valor no valido')], render_kw=style2)
    password=StringField('password', [validators.DataRequired(message='valor no valido')], render_kw=style3)
    email=EmailField('correo', [validators.DataRequired(message='valor no valido'), validators.Email(message='Ingresa un corroe valido')], render_kw=style4)

class LoginForm(Form):
    style4={'class': 'input is-large', 'placeholder': 'Email'}
    style3={'class': 'input is-large', 'placeholder': 'Password'}

    password=StringField('password',  render_kw=style3)
    email=EmailField('correo', render_kw=style4)
    remember = RadioField('', choices=[('remember', 'Recuérdame')])

class ProductForm(Form):
    style2={'class': 'input is-large', 'placeholder': 'Nombre'}
    style4={'class': 'input is-large', 'placeholder': 'Cantidad', 'min':0}
    style3={'class': 'input is-large', 'placeholder': 'Precio', 'min':0}
    style1={'class': 'input is-large', 'placeholder': 'Id'}
    style5={'class': 'input is-large', 'placeholder': 'Imagen'}
    
    id=IntegerField('id', [validators.number_range(min=1, max=20, message='valor no valido')], render_kw=style1)
    name=StringField('name', [validators.DataRequired(message='valor no valido')], render_kw=style2)
    image=StringField('image', [validators.DataRequired(message='valor no valido')], render_kw=style5)
    price=FloatField('price', [validators.DataRequired(message='valor no valido')], render_kw=style3)
    stock=IntegerField('stock', [validators.DataRequired(message='valor no valido')], render_kw=style4)
    active = RadioField('Estatus', [validators.DataRequired(message='valor no valido')], choices=[(1, 'Activo'), (0, 'Inactivo')])