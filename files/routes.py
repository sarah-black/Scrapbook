#import all that fun jazz
import os
import secrets
from PIL import Image
from flask_sqlalchemy import sqlalchemy
from flask import render_template, url_for, flash, redirect, request, abort
from files import app, db, bcrypt
from files.models import User, Post, Comment, Relationship
from files.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PostUpdateForm, FamilyForm, FamilyUpdateForm
from flask_login import login_user, current_user, logout_user, login_required

from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')




#the below is from the 08-CRUD lab code
@app.route("/register", methods=['GET', 'POST'])
#creates an account and hashes their password
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#the below is from the 08-CRUD lab code
#this checks the users' credentials against the hashed password
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#the below is from the 08-CRUD lab code
#uh... pretty self-explanatory
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#the below is from the 08-CRUD lab code
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/posts', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/posts", methods=['GET', 'POST'])
@login_required
def posts():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/fam", methods=['GET', 'POST'])
@login_required
def fam():

    fam = User.query.join(Relationship, User.id==Relationship.userID_2) \
    .add_columns(Relationship.userID_1,Relationship.relation_id,Relationship.dtr,Relationship.userID_2, User.username)
    return render_template('familyUpdate.html', posts=fam)

@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    userID=current_user.id
    author=current_user.username
    image_file = None
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
        post = Post(user_id=userID ,title=form.title.data, content=form.content.data,author=author,image=image_file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route("/posts/<id>",methods=["GET","POST"])
@login_required
def changePost(id):
    post = Post.query.get_or_404([id])
    return render_template("update_post.html", title=str(post.title)+"_"+str(post.content),post=post,now=datetime.utcnow())


@app.route("/posts/<id>/update",methods=["GET","POST"])
@login_required
def update_posts(id):

    post = Post.query.get_or_404([id])
    currentTitle = post.title
    currentContent = post.content
    print("assign")
    form = PostUpdateForm()
    if form.validate_on_submit():
        print("Test")
        if currentTitle != form.title.data:
            post.title = form.title.data
        if currentContent != form.content.data:
            post.content = form.content.data
        db.session.commit()
        flash('The Assignment has been updated!', 'success')
        return redirect(url_for('posts'))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')
@app.route("/posts/<id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('The Post has been deleted!', 'success')
    return redirect(url_for('home'))



#the below is from the 08-CRUD lab code
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                         form=form)

@app.route("/family", methods=['GET', 'POST'])
@login_required
def family():
    users = User.query.all()
    userID1 = current_user.id
    relationship = Relationship.query.all()
    form = FamilyForm(request.form)
    if form.validate_on_submit():
        relation = Relationship(userID_1=userID1, userID_2=form.fam_members.data, dtr=form.dtr.data)
        db.session.add(relation)
        db.session.commit()
        flash('You are a family! Lol Cool', 'success')
        return redirect(url_for('family'))
    return render_template('my_family.html', title='My Family', form=form, posts=posts, relationship=relationship)

@app.route("/family/<relation_id>/update", methods=['GET', 'POST'])
@login_required
def update_fam(relation_id):
    fam = Relationship.query.get_or_404()
    currentRel = fam.relation_id

    form = FamilyUpdateForm(request.form)
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentRel !=form.relation_id.data:
            fam.relation_id=form.relation_id.data
        fam.dtr=form.dtr.data
        db.session.commit()
        flash('Your relationship has been updated!', 'success')
        return redirect(url_for('update_fam', relation_id=relation_id))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.relation_id.data = dept.relation_id
        form.userID_1.data = dept.userID_1
        form.userID_2.data = dept.userID_2
        form.dtr.data = dept.dtr
    return render_template('familyUpdate.html', title='Update Fam',
                           form=form, legend='Update Fam')
