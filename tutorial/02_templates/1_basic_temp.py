
# earlier we used this to render HTML:
# from fastapi.responses import HTMLResponse

# now, we will use Jinja2 to render HTML
from fastapi.templating import Jinja2Templates

# why we use Jinja2 instead of HTMLResponse?
# because Jinja2 is a template engine that is used to render HTML as managing big HTML pages for multiple pages is a pain

templates = Jinja2Templates(directory="tutorial/02_templates/templates")
# object that looks for templates in the given directory

# ===========================================================
# Basic FastAPI application
from fastapi import FastAPI, Request

app = FastAPI() 

@app.get("/")
@app.get("/posts")
def home(request:Request):
    return templates.TemplateResponse(request, "home.html")

# jinja2 requires this request parameter to be passed to the template, so that it can access the request object and use it in the template.
# not of any use right now, but it is required to be passed to the template.
# this will be useful later

# ===========================================================

