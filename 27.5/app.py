from flask import Flask, redirect, request, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import User, db, connect_db, Feedback
from forms import UserAddForm, LoginForm, FeedbackForm, DeleteFrom
import flask_wtf
#from flask_bcrypt import Bcrypt
#from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "itsasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
toolbar = DebugToolbarExtension(app)
app.debug = True


connect_db(app)


@app.route('/register', methods=["GET", "POST"])
def register_form():
    """Register Form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = UserAddForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        
        user = User.register(username,password, email, first_name, last_name)
        
        db.session.commit()
        session['username'] = user.username
        flash("User Added!")
        return redirect(f"/users/{user.username}")
    else:
        return render_template('register.html', form=form)
    

@app.route('/')
def home():
    """Base"""
    return redirect('/register')

@app.route('/secret')
def dashboard():
    """After Login Page"""

    return render_template('secret.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    """Login Page"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash("Login Successful")
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    """Logout Page"""
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def user_view(username):
    if "username" not in session or username != session['username']:
        raise Unathorized()
    user =User.query.get(username)
    form = DeleteFrom()
    return render_template("users_view.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if "username" not in session or username != session['username']:
        raise Unathorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET","POST"])
def new_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unathorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback_new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unathorized()
    
    form=FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect("/feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unathorized()
    
    form = DeleteFrom()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{feedback.username}")


if __name__=='__main__':
     app.run(debug=True)
