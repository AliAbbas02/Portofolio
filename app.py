from flask import flask, render_template
import json

with open('post.json') as file:
  blog_posts = json.load(file)

app = flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
  app.run(debug=True)