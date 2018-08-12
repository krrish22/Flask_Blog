# !/usr/bin/python3.6
# from datetime import datetime
# from flask import Flask, render_template, url_for, flash, redirect
#
# from forms import RegistrationForm, LoginForm
#
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
# # Will protect from modifying cookies and cross site request forgery attcks etc...
#
# app.config['SECRET_KEY']='19070baa900be67562d7960c3a276c4e'
#
# # Setting location for database i.e configuration
#
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db' #is a relative path should create site.db file along project file
#
# # Crating db insatnce
#
# db = SQLAlchemy(app)
#
# # We have SQLAlchemy DB insatnce. We can represnrt DB structyre as classes and behaving those classes called MOdels
#
# # we could put in separate forms lite files
#
# class User(db.Model):
#
#     # Adding columns to the Table
#
#     id=db.Column(db.Integer,primary_key=True)
#
#     username= db.Column(db.String(20), unique=True, nullable=False)
#
#     email= db.Column(db.String(120), unique=True, nullable=False)
#
#     image_file =db.Column(db.String(20), nullable= False, default='default.jpeg')
#
#     password =db.Column(db.String(60), nullable= False)
#
#     posts=db.relationship('Post', backref='author', lazy=True)
#
#     # Here Post attribute has a relationship to the post model
#
#     #backref --- similar to adding another column to Post model, allow us to do when we have a post we can simply use
#
#     # this author attribute to get user who created the post.
#
#     #Lazy---- argument will define when SQLAlchemy loasds the date from Database. True means SQLALCHEMY will load the data as necessay in one go.
#
#     # How our object is printed, whenever we printed out
#
#     def __repr__(self):
#
#         return f"User('{self.username}', {self.email},{self.image_file})"
#
#
# class Post(db.Model):
#
#     id= db.Column(db.Integer, primary_key=True)
#
#     title= db.Column(db.String,(100), nullble=False)
#
#     date_posted = db.Column(db.DateTime, nullble=False,default=datetime.utcnow)# we are passing that utc now as argument not as function
#
#     content =db.Column(db.Text, nullable=False)
#
#     # sepcifying user in post model as below
#
#     user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#
#         return f"Post('{self.title}','{self.date_posted}',)"



from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# __name is a sepcial varbale in python is a name of a module

# DB CALL

posts =[

    {

    'author': 'krishnakanth',

    'title': 'Blog post',

    'content':'first post content',

        'date_posted':'July 26, 2018'


    },

    {

        'author': 'New auth',

        'title': 'Blog post2',

        'content': 'second post content',

        'date_posted': 'July 27, 2018'

    },

]



#Decorator use to additional funcitnaly to existing function.

@app.route("/")

@app.route("/home")
def Home():
    return render_template('Home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register",methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        flash(f'Account created for {form.username.data}!', 'success')

        return  redirect(url_for('Home'))

    return render_template('register.html', title='Register',form=form)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)
#



@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
            if form.email.data == 'admin@blog.com' and form.password.data =='password1':
                flash('You have been logged in!', 'success')
                return redirect(url_for('Home'))

            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='LogIn', form=form)



# this will run our app directly with python but not with envirmonetal var(flask run)

if __name__ == "__main__":
    app.run(debug=True)