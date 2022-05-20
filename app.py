from flask import Flask, render_template, flash, request,redirect, url_for, jsonify
from webform import LoginForm, PostForm, PasswordForm, UserForm, NamerForm, SearchForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_required, login_user, current_user, UserMixin, logout_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os
# Create Flask Instance
app = Flask(__name__)





# Add Ck Editor
ckeditor = CKEditor(app)
# Add DataBase
# Old SQLite Db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sarik1999@localhost/our_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# POstgress database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vrvxdoqjfgahvv:7b0b61d8ad08e9b4d302b06f8ca364308f8342baaacc4273dc28106eb9545b5a@ec2-52-71-69-66.compute-1.amazonaws.com:5432/d9jt62icvgfpo7'

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOde2AD_FOLDER'] = UPLOAD_FOLDER

# Secret Key!
app.config['SECRET_KEY'] = 'huytebe'

# Initialize The DAtaBase
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Json Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {}
    return {"DATE": date.today()}


# Pass Stuff Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Create Search Function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get Data From Submitted Form
        post.searched = form.searched.data
        # Query The Database
        posts = posts.filter(Posts.title.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

    return render_template("search.html", form=form, searched=post.searched, posts=posts)


# Update DateBase Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id )
        except:
            flash("Error! Looks like there was a problem ..., try again")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:

        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)






@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


# Add Post Page
@app.route('/add-post', methods=['POST','GET'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        form.title.data=''
        form.content.data = ''
        form.slug.data = ''


        # Add Post to DataBase
        db.session.add(post)
        db.session.commit()
        # Return a Message
        flash("Blog Post Submitted Successfully")
    # Return to the webpage
    return render_template('add_post.html', form=form)


@app.route('/posts/edit/i=<int:id>', methods=['POST','GET'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update DateBase
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You Aren't Authorized To Edit This Post")
        post = Posts.query.get_or_404(id)
        return render_template('post.html', post=post)

# Create Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")
    return render_template('login.html', form=form)


# Create Logout Page
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('login'))


@app.route('/verify_logout')
@login_required
def verify_logout():
    return render_template('verify_logout.html')

@app.route('/verify_delete/<int:id>')
@login_required
def verify_delete(id):
    return render_template('verify_delete.html', id=id)


# Create Dashboard
@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        name_to_update.profile_pic = request.files['profile_pic']
        name_to_update.about_author = request.form['about_author']


        # Grab Image name
        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        # Set UUID
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save That Image
        saver = request.files['profile_pic']

        # Change it to a string to save to db
        name_to_update.profile_pic = pic_name

        try:
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            db.session.commit()

            flash("User Updated Successfully!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
        except:
            flash("Error! Looks like there was a problem ..., try again")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:

        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)




@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()


    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')
        # our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, id=id)

    except:
        flash("Whoops! There was a problem deleting user, try again....")
        return render_template('add_user.html', form=form, name=name, id=id)


@app.route('/post/delete-post/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:


        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Return a message
            flash("Blog Post Was Deleted")
            posts = Posts.query.order_by(Posts.date_posted)
            return redirect(url_for('posts', posts=posts))

        except:
            flash("Whoops! There was a problem deleting post, try again....")
            return render_template('posts.html',  posts=posts)
    else:
        flash("You Aren't Autorized To Delete That Post")
        posts = Posts.query.order_by(Posts.date_posted)
        return redirect(url_for('posts', posts=posts))

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Create name page

@app.route('/name', methods=['GET', 'POST'])
@login_required
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")

    return render_template('name.html', name=name, form=form)

# Create Password TestPAge
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''

        pw_to_check = Users.query.filter_by(email=email).first()
    #     check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('test_pw.html', email=email, passed=passed, password=password, form=form, pw_to_check=pw_to_check)


# Create a route decorator
@app.route('/')
def index():
    first_name = "John"
    stuff = "This is bold text   "
    flash("Welcome to our WebSite!")

    favorite_pizza = ['Peppironi', 'Cheese', "Mashrooms", 41]
    return render_template('index.html', first_name=first_name, stuff=stuff,
                           favorite_pizza=favorite_pizza)


# Create Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 32:
     return render_template("admin.html")
    else:
        flash("Sorry You Must Be Admin To Access Admin Page")
        return redirect(url_for('dashboard'))

# localhost: 5000/user/john
@app.route('/user/<name>')
# def user(name):
#     return "<h1>Hello {}!!!</h1>".format(name)
def user(name):
    return render_template('user.html', user_name=name)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_nay_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_nay_found(e):
    return render_template("500.html"), 500

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))
    # Foreign Key To Link Users( refer to primary_key of The User)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # DO Some Password Stuff!
    password_hash = db.Column(db.String(128))
    # User Can Have Many Posts
    posts = db.relationship('Posts', backref='poster')
    profile_pic = db.Column(db.String(500), nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute! ')

    @password.setter
    def password(self, password):
        self.password_hash =generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
