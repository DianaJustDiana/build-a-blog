from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
#This line provides insight into errors.
app.config['DEBUG'] = True
#This line connects my files to the db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lilycat12@localhost:8889/build-a-blog'
#This line provides helpful info in the terminal.
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#Need to set secret key when using session.
#I typed this in -- not a real one.
app.secret_key = 'abc123'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #Limited title to 60 characters for SEO.
    title = db.Column(db.String(60))
    #Limited body to 14,000 characters because that's about 2000 words.
    body = db.Column(db.String(14000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():

    single_id = request.args.get("id")
    if single_id:
        blog = Blog.query.filter_by(id=single_id).first()
        return render_template("single_post.html", blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('index.html', title="Grr", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if len(title) == 0 and len(body) == 0:
            flash("Whoa, slow down! You were a little quick to hit that button.", 'error')
            return render_template('new_post.html')        
        elif len(title) == 0:
            flash('Oops! You forgot to put a title on your blog entry.', 'error')
            return render_template('new_post.html', body=body)
        elif len(body) == 0:
            flash('Not so fast! Nice title, but where is your body copy?', 'error')
            return render_template('new_post.html', title=title)

        else:

            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.flush()
            db.session.commit()

            single_id = new_entry.id
            return redirect("/blog?id={0}".format(single_id))

    return render_template('new_post.html')

if __name__ == '__main__':
    app.run()
