# Here we are going to use template inheritance to create a base template that will be used by other templates.

# this is essentially the same code as 2_enrich_data.py
# the only difference that we have created a layout.html that contains the constant parts of the template
# the blogs_template.html will extend the layout.html and only contain the variable parts of the template.

from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request

templates = Jinja2Templates(directory="tutorial/02_templates/templates")

app = FastAPI()

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

@app.get("/blogs")
def get_blogs(request: Request):
    return templates.TemplateResponse(request, "blogs_template.html", {"posts": posts})
    # the blogs_template.html will extend the layout.html and only contain the variable parts of the template.  
