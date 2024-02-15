from flask import Flask, redirect, request, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_form'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'itsasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
toolbar = DebugToolbarExtension(app)





@app.route("/")
def home():
    """Pets Page"""
    pets = Pet.query.all()
    return render_template('base.html', pets=pets)

@app.route("/404")
def four_0four(e):

    return render_template('404.html'), 404

@app.route("/new")
def new_pet():
    """New User"""
    return render_template('new_pet.html')


@app.route("/new", methods=["POST"])
def new_pet_form(): 
  
    form = AddPetForm()

    if form.validate_on_submit():
        new_pet =Pet(
            pet_name=request.form['pet_name'],
            species=request.form['species'],
            image_url=request.form['image_url'],
            age=request.form['age'],
            note=request.form['note'],
            availability=request.form['available'])
        db.session.add(new_pet)
        db.session.commit()
        flash("Pet Added!")

    else:

        return redirect('/')
       
@app.route("/pet/<int:pet_id>/", methods=["GET", "POST"])
def pet_edit(pet_id):
    """Users Details List"""
    pet= Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.note = request.form['note']
        pet.available = request.form['available']
        pet.photo_url = request.form['image_url']
        db.session.commit()
        flash(f"{pet.name} updated!")
        return redirect('/')
    else:
        return render_template('pet_edit.html', pet=pet, form=form)


@app.route("/pet/<int:user_id>/info", methods=["GET"])
def pet_info(pet_id):
    """Edit Users Action"""
    pet = Pet.query.get_or_404(pet_id)
    info ={"name": pet.name, "age": pet.age}
    return jsonify(info)
