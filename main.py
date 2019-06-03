from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    mismatch=""
    bad_password=""
    bad_username=""
    bad_email=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        mismatch=""
        bad_password=""
        bad_username=""
        error_bool=False
        if verify != password:
            mismatch="These passwords do not match."
            error_bool=True
        if len(password) <3 or len(password) >20:
            bad_password="Please enter a password that is between 3 and 20 characters long"
            error_bool=True
        if len(username) <3 or len(username) >20:
            bad_username="Please enter a username that is between 3 and 20 characters long"    
            error_bool=True
        if is_email(email) == False and len(email) > 0:
            bad_email="That email didn't turn out to be structured correctly.  Please try again."
            error_bool=True
        if error_bool == False:  
            return redirect('/welcome?username='+username)
    return render_template("signup.html", mismatch=mismatch, bad_password=bad_password, bad_username=bad_username, bad_email=bad_email)

def is_email(email):
    find_at = email.find('@')
    has_at = find_at >= 1
    if not has_at:
        return False
    find_dot = email.find('.')
    correct_dot = find_dot > find_at
    if not correct_dot:
        return False
    else:
        return True


@app.route('/blog')
def optimus_prime():
    boomstick=request.args.get("boomstick")
    if boomstick is None:
        entries = Entry.query.all()
        return render_template('blog.html', entries=entries) 
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
        if len(entry_title) < 1:
            no_title = "Please enter a title"
            error_bool = True
        if len(entry_body) < 1:
            no_body = "Please enter some text"
            error_bool = True
        if error_bool == False:    
            new_entry = Entry(entry_title, entry_body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?boomstick=' + str(new_entry.id))
        else: 
            return render_template('/newpost.html', no_title=no_title, no_body=no_body)
@app.route('/')
def seahorse():
    return redirect('/blog')


@app.route("/welcome")
def welcome_in():
    username = request.args.get("username")  
    return render_template("welcome.html", username=username)

@app.route("/")
def index():
    return redirect("/signup")

if __name__ == "__main__":
    app.run()