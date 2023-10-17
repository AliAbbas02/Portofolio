from flask import Flask, render_template, request, redirect, url_for
import json

with open('post.json') as file:
  blog_posts = json.load(file)

# def main():
#    print(blog_posts)

def update_blog_posts(author, title, content):
   id:int = blog_posts[-1]['id'] + 1
   post = {
      'id' : id,
      'author' : author,
      'title' : title,
      'content' : content 
   }
   blog_posts.append(post)
   

app = Flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
      author = request.form.get('author')
      title = request.form.get('title')
      content = request.form.get('content')
      update_blog_posts(author, title, content)
      return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
  app.run(debug=True)
  # main()