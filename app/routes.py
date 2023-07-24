from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import SignUpForm, LoginForm, SearchForm, AddForm
import requests, json
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product, Cart, db
from werkzeug.security import check_password_hash


@app.route('/', methods=["GET", "POST"])
def home_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    print("Error: Username or password invalid")
            else:
                print(f"Could not find user {user}")

    return render_template('index.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    print("Error: Username or password invalid")
            else:
                print(f"Could not find user {user}")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    print(request)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            email = form.email.data

            user = User(username,password,email)

            db.session.add(user)
            db.session.commit()
            print(f"Successfully created user: {username, email, password}")
        else:
            print('Form invalid')

    return render_template('signup.html', form = form)

@app.route('/lookup', methods=["GET", "POST"])
def lookup_page():
    form = SearchForm()

    if request.method == "POST":  
        search_query = (form.query.data).lower()
        output = requests.get(f"https://fakestoreapi.com/products/{search_query}").json()
        print(output)
        return render_template('lookup.html', form=form, output=output)
    
    return render_template('lookup.html', form=form)

@app.route('/products', methods=["GET", "POST"])
@login_required
def products_page():

    ids = []
    titles = []
    images = []
    prices = []
    descriptions = []
    categories = []
    ratings = []

    products = requests.get("https://fakestoreapi.com/products").json()

    print(products[0]['title'])
    
    for product in products:
        titles.append(product['title'])
        prices.append(product['price'])
        descriptions.append(product['description'])
        categories.append(product['category'])
        images.append(product['image'])
        ratings.append(product['rating'])
        ids.append(product['id'])
        prices.append(product['price'])
    print(Product.query.all())

    print(current_user.id)
    if Product.query.all() == []: 
        for i in range(len(ids)):  
            Product.id = ids[i]
            Product.name = titles[i]
            Product.description = descriptions[i]
            Product.category = categories[i]
            Product.image = images[i]
            Product.rating = ratings[i]['rate']
            Product.price = prices[i]
            product = Product(Product.id,Product.name,Product.description,Product.category,Product.image,Product.rating,Product.price)
            db.session.add(product)
            db.session.commit()
        
    return render_template('products.html', products=products)




@app.route('/add_product/<new_product_id>')
def add_product(new_product_id):

    product = Cart(current_user.id, new_product_id)

    db.session.add(product)
    db.session.commit()
    return redirect(url_for('products_page'))



@app.route('/cart/', methods={"GET","POST"})
@login_required
def cart_page():
    cart = current_user.get_cart()
    return render_template('cart.html', cart=cart)

@app.route('/remove_product/<id>')
@login_required
def remove_product(id):
    product = Cart.query.filter_by(product_id=id).first()

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('cart_page'))




    


    