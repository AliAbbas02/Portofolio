from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

#retrieving data from json file
with open('post.json') as file:
  blog_posts = json.load(file)

def update_jsonfile(data):
   '''a function that takes the updated bogposts and updates
   original json file'''
   with open('post.json', 'w') as f:
      json.dump(data, f)


def add_blog_posts(author, title, content):
   ''' function for adding new post in the end all posts
       Args:
       author(string): user who writes the post
       title(string): title of the post
       content(string): user comments/data it enters
       '''
   id:int = blog_posts[-1]['id'] + 1
   post = {
      'id' : id,
      'author' : author,
      'title' : title,
      'content' : content 
   }
   blog_posts.append(post)
   #update the main json file
   update_jsonfile(blog_posts)

   

#main route for the app/ homepage
@app.route('/')
def index():
    '''a function that renders homepage i.e. index.html'''
    return render_template('index.html', posts=blog_posts)


#route for adding a new post
@app.route('/add', methods=['GET', 'POST'])
def add():
    '''a function that takes both get and post requests for adding post'''
    #if user has made a post i.e post request
    if request.method == 'POST':
      author = request.form.get('author')
      title = request.form.get('title')
      content = request.form.get('content')
      #calling add post function for updating posts
      add_blog_posts(author, title, content)
      #redirecting to index function / homepage
      return redirect(url_for('index'))
    #if its a get request then render to add page 
    return render_template('add.html')


#route for deleting a post 
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
  '''function for deleting route which get the id from url and deletes
     the post
     Args
     post_id(int): unique id for the post 
  '''
  index:int = 0
  for post in blog_posts:
    if post['id'] == post_id:
      break
    index +=1
  #delete the post on index   
  del blog_posts[index]
  #updating the orignal post file 
  update_jsonfile(blog_posts)
  #redirecting to homepage
  return redirect(url_for('index'))


def fetch_post_by_id(post_id):
   '''a function that fetches the post by id and return it'''
   for post in blog_posts:
      if post['id'] == post_id:
         return post
    

def update_blog_post(author, title, content, post_id):
   ''' a function that updates the post
       Args:
       author(string): author of the post
       title(string): title of the post
       content(string): data entered by user
       post_id(int): id of the post'''
   for post in blog_posts:
      #if id matches the post id , updates the following data
      if post['id'] == post_id:
         post['author'] = author
         post['title'] = title
         post['content'] = content
         break 


#update route gets id of the post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
  #if id enterend is not in the data, 404 error should be displayed
  post = fetch_post_by_id(post_id)
  if post is None:
    return 'post not found', 404
  #if its a post request retrieve the data from url and update the post
  if request.method == 'POST':
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')
    #update the post data
    update_blog_post(author, title, content, post_id)
    #update main json file for posts
    update_jsonfile(blog_posts)
    return redirect(url_for('index'))
  #if its a get request render the update page with post details
  return render_template('update.html', post=post)    


#like button route for each post
@app.route('/like/<int:post_id>')
def like(post_id):
   '''a function that retrieves id from url and adds a like key into post
      if like key already in the post data than updates it'''
   for post in blog_posts:
      if post['id'] == post_id:
         #if id matches and id has key 'likes' update it else kae a new key 'likes'
         post.update({'likes': post.get('likes', 0) + 1})
   #updating main json file for posts      
   update_jsonfile(blog_posts)   
   #redierct to homepage
   return redirect(url_for('index'))     

         

if __name__ == '__main__':
  app.run(debug=True)