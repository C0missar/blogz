from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)

class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Entry", backref = "user")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user


@app.route("/login", methods=['GET', 'POST'])
def login():
    incorrect_info=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        incorrect_info=""
        q_user = User.query.filter_by(username=username).first()
        error_bool=False
        if q_user:
            if password != q_user.password:
                incorrect_info = "Incorrect username or password"
                error_bool=True
        else:
            incorrect_info = "Incorrect username or password"
            error_bool=True    
        if error_bool == False:
            session['user'] = username 
            return redirect('/newpost?username='+username)
        else:
            return render_template("login.html", incorrect_info=incorrect_info)    
    return render_template("login.html")
    
@app.route('/logout')
def logout():
    if "user" in session:
        del session['user']
    return redirect('/blog')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    mismatch=""
    bad_password=""
    bad_username=""
    other_username=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        taken_username=User.query.filter_by(username=username).count()
        error_bool=False
        if verify != password:
            mismatch="These passwords do not match."
            error_bool=True
        if len(password) <3:
            bad_password="Please enter a password that is at least 3 characters long"
            error_bool=True
        if len(username) <3:
            bad_username="Please enter a username that is at least 3 characters long"    
            error_bool=True
        if taken_username > 0:
            other_username="This username has already been taken.  Please pick another one."
            error_bool=True
        if error_bool == False:  
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            session["user"] = username
            return redirect('/newpost?username='+username)
        else:
            return render_template("signup.html", mismatch=mismatch, bad_password=bad_password, bad_username=bad_username, other_username=other_username)
    else: 
        return render_template("signup.html")


@app.route('/blog')
def optimus_prime():
    #TODO 4: have a second query param for user id, which 
    # when going down that route will serve up a page
    # of all the entries written by a single user.
    boomstick=request.args.get("boomstick")
    seahorse=request.args.get("seahorse")
    if boomstick is None and seahorse is None:
        entries = Entry.query.all()
        return render_template('blog.html', entries=entries)
    elif seahorse:
        user_entries = User.query.get(int(seahorse))
        return render_template('blog.html', entries=user_entries.blogs)
    else:
        entry = Entry.query.get(int(boomstick))
        return render_template('blog.html', entries=[entry])

@app.route('/newpost', methods=['GET', 'POST'])
def avocado():
    no_title = ""
    no_body = ""
    if request.method == 'GET':
        return render_template('newpost.html')
    else:    
        entry_title = request.form['title']
        entry_body = request.form['body']
        error_bool = False
        if len(entry_title) < 1:
            no_title = "Please enter a title"
            error_bool = True
        if len(entry_body) < 1:
            no_body = "Please enter some text"
            error_bool = True
        if error_bool == False:
            owner=User.query.filter_by(username = session['user']).first()    
            new_entry = Entry(entry_title, entry_body, owner)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?boomstick=' + str(new_entry.id))
        else: 
            return render_template('/newpost.html', no_title=no_title, no_body=no_body)


@app.route("/welcome")
def welcome_in():
    username = request.args.get("username")  
    return render_template("welcome.html", username=username)

@app.route("/")
def index():
    return redirect("/signup")

endpoints_with_login = ["avocado"]

@app.before_request
def require_login():
    if ("user" not in session and request.endpoint in endpoints_with_login):
        return redirect("/login")
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'
if __name__ == "__main__":
    app.run()