from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Post, Tag

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

@app.route("/404")
def four_0four(e):

    return render_template('404.html'), 404

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
    flash("User Added!")

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
     flash("User Edited!")

     return redirect('/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
     """Delete Users"""
    
     user = User.query.get_or_404(user_id)
     db.session.delete(user)
     db.session.commit()
     flash("User Deleted!")

     return redirect('/users')



#### POSTS

@app.route("/users/<int:user_id>/new/post")
def posts_form(user_id):

    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/new/post", methods=["POST"])
def new_posts(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post =Post(title=request.form['title'],
        content=request.form['content'],
        user=user,
        tags=tags
       )
    
    db.session.add(new_post)
    db.session.commit()
    flash("Post Added!")

    return redirect(f'/users/{user_id}')



@app.route("/post/<int:post_id>/")
def post_view(post_id):
    user = User.query.order_by(User.last_name, User.first_name).all()
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_details.html', post=post, user=user, tags=tags)


@app.route("/post/<int:post_id>/edit")
def edit_post_view(post_id):
    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title =request.form['title']
    post.content =request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash("Post Edited!")
    
    return redirect(f'/users/{post.user_id}')

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted!")

    return redirect(f'/users/{post.user_id}')


##### Tags

@app.route("/new/tags")
def new_tag():
    posts = Post.query.all()
    return render_template('new_tag.html', posts=posts)

@app.route("/tags/list")
def tags_list():
    user = User.query.order_by(User.last_name, User.first_name).all()
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags, user=user)


@app.route("/new/tags", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash("Tag Addded")

    return redirect("/tags/list")

@app.route('/tags/<int:tag_id>')
def tags_view(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_details.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit')
def edit_tags_view(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tags.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash("Tag Edited!")
    return redirect("/tags/list")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash("Tag Deleted!")

    return redirect("/tags/list")