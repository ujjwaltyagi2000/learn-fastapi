# we have created new HTML files with bootstrap styling and we will use them in this tutorial. 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # to serve static files like CSS, JS, images, etc.
from fastapi import FastAPI, Request

templates = Jinja2Templates(directory="tutorial/02_templates/templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="tutorial/02_templates/static"), name="static")
# the mount() method takes 3 arguments:
# 1. the url path where the static files will be served from (in this case, "/static")
# 2. the StaticFiles instance that points to our local static files directory (in this case, "tutorial/02_templates/static")
# 3. name that we can use to reference in our templates (in this case, "static")

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

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "layout_finished.html")
    # base template in which we enrich posts

@app.get("/blogs")
def get_blogs(request: Request):
    return templates.TemplateResponse(request, "blogs_finished.html", {"posts": posts})
    # blogs_finished.html inherits layout_finished.html and enriches it with the posts data
