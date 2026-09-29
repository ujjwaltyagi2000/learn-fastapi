from fastapi import FastAPI # this is a class

app = FastAPI() # this is an instance of the class

# we use the above app object to define our API endpoints or routes

# we use the decorator syntax to define a route 

@app.get("/") # root
def home():
    return {"message": "Hello World!"}

# this is the most basic application that we can create
# to run this, run it via the command line
"""
uv run fastapi dev tutorial/01_intro/main.py

you can use either fastapi dev or fastapi run command to run the application

Difference:

dev --> it will reload the server when you make changes to the code
run --> it will not reload the server when you make changes to the code, but it is optimized for performance

during development, we use dev command to run the application so that we don't have to restart the server every time we make changes to the code
"""

# Let's create an API endpoint that returns data of "posts" posted on a blog

# data
posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/api/posts")
def get_posts():
    return posts
# this is a GET request to the endpoint /api/posts  
# this will return the list of posts in JSON format (FastAPI handles it)


# Returning HTML from an API endpoint
from fastapi.responses import HTMLResponse
user_name = "Ujjwal"
@app.get("/api/page", response_class=HTMLResponse)
def get_page():
    html_content = f"""
    <html>
        <head>
            <title>My FastAPI Page</title>
        </head>
        <body>
            <h1>Hello, {user_name}!</h1>
            <p>This is a simple HTML page served by FastAPI.</p>
        </body>
    </html>
    """
    return html_content


# what if I want two routes to return the same data but with different endpoints?
# we can use the same function to handle multiple routes by using the decorator syntax multiple times
# this is called STACKING DECORATORS

@app.get("/api/new_posts", response_class=HTMLResponse)
@app.get("/api/old_posts", response_class=HTMLResponse)
def get_new_posts():
    return posts[0].get("title","")

