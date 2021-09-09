from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
with open("config.json","r") as f:
    params=json.load(f)["params"]

app = Flask("blogapp") # app is defined here
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/blog' # connection is done with database
app.config.update(MAIL_SERVER="smtp.gmail.com",MAIL_PORT="465",MAIL_USE_SSL=True,MAIL_USERNAME=params['emailuser'],MAIL_PASSWORD=params['pass'])
mail=Mail(app)
db = SQLAlchemy(app)
class Contacts(db.Model):
    '''

    Here we have created connection with the table of hte database
    '''
    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False)
    email = db.Column(db.String(120), unique=False)
    phone = db.Column(db.String(120), unique=False)
    msg = db.Column(db.String(120), unique=False)
    time = db.Column(db.String(120), nullable=True,unique=True)
class Posts(db.Model):
    '''

    Here we have created connection with the table of hte database
    '''
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=False)
    tagline = db.Column(db.String(50), unique=False)
    slug = db.Column(db.String(20), unique=False)
    content = db.Column(db.String(150), unique=False)
    date = db.Column(db.String(120), nullable=True,unique=True)
@app.route("/post/<string:post_slug>")
def post(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",post=post,params=params)


@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template("index.html",params=params,posts=posts)
@app.route("/about")
def about():
    return render_template("about.html",params=params)
@app.route("/contact",methods=['POST','GET'])
def contact():
    if request.method=="POST": # if post request is done
        in_name=request.form.get('name')
        in_email=request.form.get('email')
        in_phone=request.form.get('phone')
        in_msg=request.form.get('msg')
        entry=Contacts(name=in_name,email=in_email,phone=in_phone,msg=in_msg,time=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(sender=params['emailuser'],subject=f"{in_msg}",recipients=[params['emailuser']],body="This is to inform you that there is a message from your blog sir")
    # the entry will be done here
    return render_template("contact.html",params=params)

@app.route("/login",methods=['POST','GET'])
def login():
    if "logged" in session and session["logged"]==params['username']: # if user is logged in
        posts=Posts.query.filter_by().all()
        return render_template("dashboard.html",params=params,posts=posts)
    if request.method=="POST": # if post request is done by the user
        user_name=request.form.get('name')
        pass_word=request.form.get('password')
        
        if user_name==params['username'] and pass_word==params['password']: # if user have entered a correct password and user name
            session["logged"]=params['username']
            posts=Posts.query.filter_by().all()
            return render_template("dashboard.html",params=params,posts=posts)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html") # in starting
@app.route("/addit",methods=['POST','GET'])
def addpost():
    if request.method=="POST":
        post_title=request.form.get('title')
        post_tagline=request.form.get('tagline')
        post_slug=request.form.get('slug')
        post_content=request.form.get('content')
        entry=Posts(title=post_title,tagline=post_tagline,slug=post_slug,content=post_content)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(sender=params['emailuser'],subject="The post is successfully added to your database Sir",recipients=[params['emailuser']],body="This is to inform you that the post has been added to your database")
        return render_template("addpost.html",params=params)
    else:
        return render_template("addpost.html",params=params)
@app.route("/delete/<string:post_slug>",methods=['POST','GET'])
def delete(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    db.session.delete(post) # delete that particular post
    db.session.commit()
    posts=Posts.query.filter_by().all()
    mail.send_message(sender=params['emailuser'],subject="The post is Deleted from your Blog and database",recipients=[params['emailuser']],body="This is to inform you that the post has been Deleted from you website")
    return render_template("dashboard.html",params=params,posts=posts)
@app.route("/logout")
def logout():
    session.pop("logged")
    return redirect("/")
@app.route("/searchpost",methods=['POST','GET'])
def search():
    if request.method=="POST": # if post request is done
        t=request.form.get('title')
        post=Posts.query.filter_by(title=t).first()
        return render_template("show.html",post=post,params=params)
    else:
        return render_template("search.html",params=params)




app.run(debug=True)