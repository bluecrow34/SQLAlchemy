from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bio_user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'itsasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all

@app.route("/")
def home():
    """User Options"""
    return render_template('base.html')

@app.route("/new")
def new_user_app():
    """New User"""

    return render_template('new_user.html')

@app.route("/users", methods=["GET"])
def users_list():
    """User List"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users=users)


@app.route("/new", methods=["POST"])
def add_user(): 
    
    new_user =User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
       
@app.route("/users/<int:user_id>/")
def user_details(user_id):
     """Users Details List"""
     user = User.query.get_or_404(user_id)
     return render_template('user_details.html', user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_view(user_id):
     """Edit Users View"""

     user = User.query.get_or_404(user_id)
     return render_template('edit_users.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
     """Edit Users Action"""
     user = User.query.get_or_404(user_id)
     user.first_name = request.form['first_name']
     user.last_name = request.form['last_name']
     user.image_url = request.form['image_url']

     db.session.commit()

     return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
     """Delete Users"""
    
     user = User.query.get_or_404(user_id)
     db.session.delete(user)
     db.session.commit()
     #flash(f"User {user.full_name} deleted!")

     return redirect('/users')



#### POSTS

@app.route("/users/<int:user_id>/new/post")
def posts_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)

@app.route("/users/<int:user_id>/new/post", methods=["GET"])
def new_posts(user_id):
    user = User.query.get_or_404(user_id)
    new_post =Post(
        p_title=request.form['title'],
        p_content=request.form['content']
       )
    
    db.session.add(new_post)
    db.session.commit()

    return redirect('/users/{user.id}')

@app.route("/post/<int:post_id>/")
def post_view(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route("/post/<int:post_id>/edit")
def edit_post_view(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.p_title=request.form['title'],
    post.p_content=request.form['content']
    db.session.commit()
    
    return redirect('/users/{user.id}')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    #flash(f"User {user.full_name} deleted!")
    return redirect('/users/{user.id}')