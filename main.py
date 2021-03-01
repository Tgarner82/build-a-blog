from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:strider1@localhost:8889/build-a-blog' 
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'strider'

class Blog(db.Model):
    # You have the blog creating the unique id here. How do you query it so that it displays? Where would it need to display? 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(999))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/single_blog', methods=['GET'])
def single_blog():
    blog_id = int(request.args.get('id'))
    blog = Blog.query.get(blog_id)
    return render_template('singleblog.html', blog=blog)
   
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    error = ''
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']

        if len(blog_name) == 0 or len(blog_body) == 0:
            error = 'Please enter text.'
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()


            return redirect('/single_blog?id='+str(new_blog.id))
   
    return render_template('newpost.html', error=error)

            
    
if __name__ == '__main__':
    app.run()
