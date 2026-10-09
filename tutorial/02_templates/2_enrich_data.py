# let's try to enrich an HTML template with data from the backend using Jinja2 template engine

from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request

templates = Jinja2Templates(directory="tutorial/02_templates/templates")

app = FastAPI()

# data to be enriched in the template
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
    return templates.TemplateResponse(request, "home.html")

@app.get("/posts")
def get_posts():
    return {"posts": posts}

# embedding posts data in the template:
@app.get("/blogs")
def get_blogs(request: Request):
    # return templates.TemplateResponse(request, "blogs.html", {"posts": posts, "title": "Blogs"})
    return templates.TemplateResponse(request, "blogs.html", {"posts": posts})

# data is passed to the template as a dictionary, where the key is the variable name that will be used in the template, and the value is the data that will be used to enrich the template.
# IMP --> this dictionary is called the "context"