from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import certifi
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
import gridfs
import base64
import bcrypt
from werkzeug.utils import secure_filename
from io import BytesIO
import stripe
from bson import ObjectId

app = Flask(__name__)
app.secret_key = '0c6e69f08d231cee70b09b729e78efca'
client = pymongo.MongoClient("mongodb+srv://aishahussain13579:a9831122132@adainsta.tfexlrz.mongodb.net/", tlsCAFile=certifi.where())
db = client['FootPath']
user_collection = db['loginData']
product_collection = db['products']
fs = gridfs.GridFS(db)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get('username')
        user = user_collection.find_one({'email': email, 'password': password, 'name': name})
        if user:
            session['logged_in'] = True
            session['email'] = email
            session['username'] = name
            print("Login done")
            return redirect("/home")
        else:
            return "incorrect login information, please try again! <a href='/'>login</a>"

    return render_template('login.html')

@app.route("/sign-up", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('username')
        userinfo = {"email": email, "password": password, "name": name}  
        user_collection.insert_one(userinfo)
        return redirect('/')
    
    return render_template('sign.html')

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    wrap.__name__ = f.__name__
    return wrap

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
@login_required
def home():
    return render_template("home.html")


@app.route('/mens-collection')
@login_required
def mensAll():
    products = list(product_collection.find({"gender": "MEN"}))
    for product in products:
        image_id = product.get('image_id')
        if image_id:
            try:
                image_file = fs.get(image_id)
                img_data = image_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                product['image_data'] = img_base64
            except Exception as e:
                print(f"Error retrieving image: {e}")
                product['image_data'] = None
     
    return render_template('mens.html', products=products)


import base64

@app.route('/mens-shoes')
@login_required
def mensShoes():
    shoes = list(product_collection.find({"gender":"MEN", "tag":"SHOES"}))
    
    for shoe in shoes:
        image_id = shoe.get('image_id') 
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  
 
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                shoe['image_data'] = img_base64  
                
            except Exception as e:
                print(f"Error retrieving image: {e}")
                shoe['image_data'] = None  
    
    return render_template('menshoes.html', products=shoes)

@app.route('/mens-clothes')
@login_required
def mensclothes():
    clothes = list(product_collection.find({"gender":"MEN", "tag":"CLOTHING"}))
    
    for cloth in clothes:
        image_id = cloth.get('image_id')
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  # Read the image data
                
                # Convert the image data to Base64 for displaying in the template
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                cloth['image_data'] = img_base64  # Add the image data to the cloth dict
                
            except Exception as e:
                print(f"Error retrieving image: {e}")
                cloth['image_data'] = None  # If error occurs, set image_data to None
    
    return render_template('mensclothing.html', products=clothes)  # Pass the full clothes list to the template


@app.route('/mens-bags')
@login_required
def mensBags():
    bags = list(product_collection.find({"gender":"MEN", "tag":"BAGPACK"}))
    
    for bag in bags:
        image_id = bag.get('image_id') 
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                bag['image_data'] = img_base64  
            except Exception as e:
                print(f"Error retrieving image: {e}")
                bag['image_data'] = None  
    
    return render_template('mensbags.html', products=bags)


@app.route('/womens-collection')
@login_required
def womensCollection():
    women_clothes = list(product_collection.find({"gender":"WOMEN"}))
    
    for cloth in women_clothes:
        image_id = cloth.get('image_id') 
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                cloth['image_data'] = img_base64  
            except Exception as e:
                print(f"Error retrieving image: {e}")
                cloth['image_data'] = None  
    
    return render_template('womens.html', products=women_clothes)


@app.route('/womens-shoes')
@login_required
def womensShoes():
    womens_shoes = list(product_collection.find({"gender":"WOMEN", "tag":"SHOES"}))
    
    for shoe in womens_shoes:
        image_id = shoe.get('image_id') 
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                shoe['image_data'] = img_base64  
            except Exception as e:
                print(f"Error retrieving image: {e}")
                shoe['image_data'] = None  
    
    return render_template('womensshoes.html', products=womens_shoes)



@app.route('/womens-bags')
@login_required
def womensBags():
    womens_bags = list(product_collection.find({"gender": "WOMEN", "tag": "HANDBAG"}))
    
    for bag in womens_bags:
        image_id = bag.get('image_id') 
        if image_id:
            try:
                image_file = fs.get(image_id)  
                img_data = image_file.read()  
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                bag['image_data'] = img_base64  
            except Exception as e:
                print(f"Error retrieving image: {e}")
                bag['image_data'] = None  
    
    return render_template('womensbags.html', products=womens_bags)



@app.route('/upload', methods=["POST"])
def upload_image():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.files['image']
        tag = request.form['tag']
        gender = request.form['gender']
        quantity = request.form['quantity']
        file_id = fs.put(image, filename=secure_filename(image.filename))
        product_info = {
            "name": name,
            "description": description,
            "price": price,
            "image_id": file_id,
            "gender": gender,
            "quantity": quantity,
            "tag": tag 
        }
        product_collection.insert_one(product_info)
        return redirect('/admin67672/addproduct')

@app.route('/<productname>/desc')
@login_required
def product_desc(productname):
    product = product_collection.find_one({"name": productname})
    if not product:
        return "Product not found", 404

    # Retrieve image data
    image_data = None
    if 'image_id' in product:
        try:
            image_file = fs.get(product['image_id'])
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error retrieving image: {e}")

    # Pass the product data to the template
    return render_template('product_desc.html', product=product, image_data=image_data)


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')
stripe.api_key = "sk_test_51P4TSoSFPrVdKBVbmjp9LASNKS33nvJlYFF5lrve0DX2ld9rKePslNPDZZW21aH0MyFfeGpDv0WAuWRgMsMpeV9000LM8mZYSC"
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        line_items = [
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(float(item['price']) * 100),  # Convert to paisa
                },
                'quantity': 1,
            } for item in data['items']
        ]

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )

        return jsonify({'id': session.id})
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return jsonify({'error': str(e)}), 500


# Add an 'orders' collection
orders_collection = db['orders']

@app.route('/process-cod-order', methods=['POST'])
def process_cod_order():
    try:
        data = request.json
        username = session.get('username')
        phone = data.get('phone')
        address1 = data.get('address_line_one')
        address2 = data.get('address2_line_two')
        pincode = data.get('pincode')
        state = data.get('state')
        items = data.get('items')
        total_price = data.get('total')

        # Save the order in the 'orders' collection
        order = {
            "username": username,
            "phone": phone,
            "items": items,
            "address_line_one": address1,
            "address_line_two":address2,
            "pincode":pincode,
            "state":state,
            "total_price": total_price,
            "status": "Processing",
            "payment_method": "COD",
        }
        orders_collection.insert_one(order)

        # Redirect to success page
        return jsonify({'success': True, 'redirect_url': '/success-cod'})
    except Exception as e:
        print(f"Error processing COD order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/success-cod')
def success_cod():
    return "Your order has been placed successfully and is being processed. Thank you for shopping with us! <a href='/home'>Redirect to home</a>"



# ADMIN PANEL
hashed_password = bcrypt.hashpw(b"002777abb$$2ijjj98277sha77719bcrypt720adminpanelaccess78889923132", bcrypt.gensalt())

@app.route('/admin67672', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':
        password = request.form['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            session['admin_logged_in'] = True
            return redirect(url_for('addprod'))
        else:
            return "Invalid password, please try again."

    return render_template('adminlog.html')

def admin_login_required(f):
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('adminlog'))  
    wrap.__name__ = f.__name__
    return wrap

@app.route('/admin67672/addproduct')
@admin_login_required
def addprod():
    return render_template('addprod.html')


@app.route('/admin67672/orders')
@admin_login_required
def order():
    orders_collection = db["orders"]

    orders = list(orders_collection.find())  # Fetch all orders

    # Debugging: Print the structure of the orders
    for order in orders:
        print(order)

    return render_template("adminorder.html", orders=orders)


@app.route('/admin67672/all-products')
@admin_login_required
def view_products():
    products_collection = db['products']
    products = list(products_collection.find())
    for product in products:
        if isinstance(product.get('image_id'), bytes):  # Check if image_id is binary data
            product['image_id'] = base64.b64encode(product['image_id']).decode('utf-8')  # Encode binary to Base64
        else:
            print(f"No image data or wrong data type for product: {product['_id']}")
    return render_template("adminprod.html", product=products)


@app.route('/admin67672/logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Remove the admin session
    return redirect(url_for('adminlog'))  # Redirect to admin login page

@app.route('/admin67672/edit-product/<product_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_product(product_id):
    # Find the product by its ID
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        # Get updated product information from the form
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.files.get('image')
        tag = request.form['tag']
        gender = request.form['gender']
        quantity = request.form['quantity']

        # If a new image is uploaded, save it and update the product's image ID
        if image:
            file_id = fs.put(image, filename=secure_filename(image.filename))
            product['image_id'] = file_id

        # Update the product information in the database
        product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {
                "name": name,
                "description": description,
                "price": price,
                "tag": tag,
                "gender": gender,
                "quantity": quantity,
                "image_id": product.get('image_id', None)
            }}
        )

        return redirect('/admin67672/all-products')  # Redirect to the products page after updating

    return render_template('editprod.html', product=product)



if __name__ == "__main__":
    app.run(debug=True, port=6573)