"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash, url_for, jsonify
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'asdfasdfasdfasd'

app.app_context().push()
connect_db(app)
db.create_all()


toolbar = DebugToolbarExtension(app)

@app.route('/')
def list_pets():
    """List all pets."""

    pets = Pet.query.all()
    return render_template("pets.html", pets=pets)
    


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Add a pet."""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_pets'))

    else:
        # re-present form for editing
        return render_template("pet_add_form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet."""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    else:
        # failed; re-present form for editing
        return render_template("pet_edit_form.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)




# @app.route('/users')
# def users_index():
#     """Show a page with info on all users"""

#     users = User.query.order_by(User.last_name, User.first_name).all()
#     return render_template('users/index.html', users=users)


# @app.route('/users/new', methods=["GET"])
# def users_new_form():
#     """Show a form to create a new user"""

#     return render_template('users/new.html')


# @app.route("/users/new", methods=["POST"])
# def users_new():
#     """Handle form submission for creating a new user"""

#     new_user = User(
#         first_name=request.form['first_name'],
#         last_name=request.form['last_name'],
#         image_url=request.form['image_url'] or None)

#     db.session.add(new_user)
#     db.session.commit()
#     flash(f"User {new_user.full_name} added.")

#     return redirect("/users")



# @app.route('/users/<int:user_id>')
# def users_show(user_id):
#     """Show a page with info on a specific user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/show.html', user=user)



# @app.route('/users/<int:user_id>/edit')
# def users_edit(user_id):
#     """Show a form to edit an existing user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/edit.html', user=user)


# @app.route('/users/<int:user_id>/edit', methods=["POST"])
# def users_update(user_id):
#     """Handle form submission for updating an existing user"""

#     user = User.query.get_or_404(user_id)
#     user.first_name = request.form['first_name']
#     user.last_name = request.form['last_name']
#     user.image_url = request.form['image_url']

#     db.session.add(user)
#     db.session.commit()

#     return redirect("/users")



# @app.route('/users/<int:user_id>/delete', methods=["POST"])
# def users_destroy(user_id):
#     """Handle form submission for deleting an existing user"""

#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()

#     return redirect("/users")



