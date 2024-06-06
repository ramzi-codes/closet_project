from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname
from flask_login import (LoginManager, UserMixin,
    login_user, logout_user, login_required, current_user)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
    )


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("add_user.html")
    if request.method == "POST":
        password=request.form.get("password")

        user = Users(username=request.form.get("username"),
                     password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login_user.html")
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()

        password = request.form.get("password")
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('You were successfully logged in')
            return redirect("/closet")
        else:
            flash('Your username or password were incorrect')
            return redirect("/login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You were successfully logged out')
    return redirect("/login")



class Closet(db.Model):
    __tablename__ = "closet"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(4096))
    author_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    author = db.relationship("Users", back_populates="closet")


class tops(db.Model):
    __tablename__ = "tops"
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(4096))
    type_top = db.Column(db.String(4096))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    author = db.relationship("Users", back_populates="tops")
    image_t = db.Column(db.Integer, db.ForeignKey("images.id"))
    image_tt = db.relationship("Images", back_populates="tops")


class bottoms(db.Model):
    __tablename__ = "bottoms"
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(4096))
    shorts_or_pants = db.Column(db.String(4096))
    type_bottoms = db.Column(db.String(4096))
    text = db.Column(db.String(4096))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    author = db.relationship("Users", back_populates="bottoms")
    image_b = db.Column(db.Integer, db.ForeignKey("images.id"))
    image_bb = db.relationship("Images", back_populates="bottoms")


class shoes(db.Model):
    __tablename__ = "shoes"
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(4096))
    brand = db.Column(db.String(4096))
    purpose = db.Column(db.String(4096))
    text = db.Column(db.String(4096))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    author = db.relationship("Users", back_populates="shoes")
    image_s = db.Column(db.Integer, db.ForeignKey("images.id"))
    image_ss = db.relationship("Images", back_populates="shoes")

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    closet = db.relationship("Closet", back_populates="author")
    tops = db.relationship("tops", back_populates="author")
    bottoms = db.relationship("bottoms", back_populates="author")
    shoes = db.relationship("shoes", back_populates="author")
    images = db.relationship("Images", back_populates="author")

class Images(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("Users", back_populates="images")
    tops = db.relationship("tops", back_populates="image_tt")
    bottoms = db.relationship("bottoms", back_populates="image_bb")
    shoes = db.relationship("shoes", back_populates="image_ss")


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/closet')
@login_required
def view_closet():
    Top = tops.query.all()
    Bottom = bottoms.query.all()
    Shoe = shoes.query.all()
    return render_template('closet.html', Top=Top, Bottom=Bottom, Shoe=Shoe)


@app.route('/add_top', methods=['POST', 'GET'])
@login_required
def add_top():
    if request.method == 'GET':
        return render_template('add_top.html')
    if request.method == 'POST':
        Type = request.form['type']
        color = request.form['color']
        f = request.files['file']
        filename = "mysite/static/images/" + f.filename
        f.save(filename)
        image_t = Images(filename=f.filename, author=current_user)
        db.session.add(image_t)
        db.session.commit()
        newTop = tops(type_top=Type, color=color, author = current_user, image_tt = image_t)
        db.session.add(newTop)
        db.session.commit()
        return redirect("/closet")


@app.route('/add_bottom', methods=['POST', 'GET'])
@login_required
def add_bottoms():
    if request.method == 'GET':
        return render_template('add_bottoms.html')
    if request.method == 'POST':
        shorts_or_pants = request.form['shorts_or_pants']
        color = request.form['color']
        type_bottoms = request.form['type_bottoms']
        f = request.files['file']
        filename = "mysite/static/images/" + f.filename
        f.save(filename)
        image_b = Images(filename=f.filename, author=current_user)
        db.session.add(image_b)
        db.session.commit()
        newBottoms = bottoms(shorts_or_pants=shorts_or_pants, color=color, type_bottoms=type_bottoms, author = current_user, image_bb = image_b)
        db.session.add(newBottoms)
        db.session.commit()
        return redirect("/closet")


@app.route('/add_shoes', methods=['POST', 'GET'])
@login_required
def add_shoes():
    if request.method == 'GET':
        return render_template('add_shoes.html')
    if request.method == 'POST':
        purpose = request.form['purpose']
        color = request.form['color']
        brand = request.form['brand']
        f = request.files['file']
        filename = "mysite/static/images/" + f.filename
        f.save(filename)
        image_s = Images(filename=f.filename, author=current_user)
        db.session.add(image_s)
        db.session.commit()
        newShoes = shoes(purpose=purpose, color=color, brand=brand, author = current_user, image_ss = image_s)
        db.session.add(newShoes)
        db.session.commit()
        return redirect("/closet")


@app.route('/delete_tops/<id>')
@login_required
def delete_tops(id):
    toDelete = tops.query.get(id)
    if(toDelete.author != current_user):
            flash("You are not the author of this comment, so you can't delete it!")
            return redirect("/closet")
    db.session.delete(toDelete)
    db.session.commit()
    return redirect("/closet")

@app.route('/delete_bottoms/<id>')
@login_required
def delete_bottoms(id):
    toDelete = bottoms.query.get(id)
    if(toDelete.author != current_user):
            flash("You are not the author of this comment, so you can't delete it!")
            return redirect("/closet")
    db.session.delete(toDelete)
    db.session.commit()
    return redirect("/closet")

@app.route('/delete_shoes/<id>')
@login_required
def delete_shoes(id):
    toDelete = shoes.query.get(id)
    if(toDelete.author != current_user):
            flash("You are not the author of this comment, so you can't delete it!")
            return redirect("/closet")
    db.session.delete(toDelete)
    db.session.commit()
    return redirect("/closet")


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        me = Users(username='admin',password=generate_password_hash("admin"))
        myCloset = Closet(text='''This is a sample item''',author=me)
        db.session.add(me)

        db.session.commit()
    if 'liveconsole' not in gethostname():
        app.run()






