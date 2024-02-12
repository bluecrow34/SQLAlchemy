from flask import Flask, redirect, request, render_template
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bio_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'itsasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)



@app.route('/')
def home():
    """Home Page"""
    return render_template('base.html')


@app.route('/app')
def users_list():
    """User List"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('app_list.html')


@app.route('/app/new', methods=[ "GET"])
def new_user_app():
    """New Applicant"""

    return render_template('new_app.html')


@app.route('/app/new', methods=["POST"])
def add_user():
        """New User"""
        new_user = User(
            first_name = request.form.get['first_name'],
            last_name = request.form.get['last_name'],
            image_url = request.form.get['image_url'] or None)

        db.session.add(new_user)
        db.session.commit()

        return redirect('base.html')
       

@app.route('/app/<int:user-id>/')
def user_details(user_id):
     """Users Details List"""
     user = User.query.get_or_404(user_id)
     return render_template('app_details.html', user=user)

@app.route('/app/<int:user-id>/edit')
def edit_user(user_id):
     """Edit Users"""
     user = User.query.get_or_404(user_id)
     return render_template('edit_users.html', user=user)

@app.route('/app/<int:user-id>/edit', methods=["POST"])
def edit_user(user_id):
     """Edit Users"""
     user = User.query.get_or_404(user_id)
     return render_template('edit_users.html', user=user)

@app.route('/app/<int:user-id>/delete', methods=["POST"])
def delete_user(user_id):
     """Delete Users"""
     return redirect('base.html')




if __name__ == "__main__":
    app.run(debug=True)
