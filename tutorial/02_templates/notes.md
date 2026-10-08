# Templates

Right now, we are manually building HTML inside our Python code:

```python
@app.get("/api/page", response_class=HTMLResponse)
def get_page():
    html_content = f"""
    <html>
        <body>
            <h1>Hello, {user_name}!</h1>
        </body>
    </html>
    """
    return html_content
```

This works, but it becomes horrible once your HTML gets large.

## 1. The problem templates solve

Imagine your page grows to this:

```html
<html>
<head>
    <title>My Blog</title>
</head>

<body>
    <h1>Welcome, Ujjwal!</h1>

    <h2>Posts</h2>

    <div>
        <h3>FastAPI is Awesome</h3>
        <p>FastAPI is really easy to use.</p>
    </div>

    <div>
        <h3>Python is Great</h3>
        <p>Python is a great language.</p>
    </div>

</body>
</html>
```

You **don't want this HTML sitting inside a Python string**.

Instead, you create an actual HTML file:

```text
project/
│
├── main.py
│
└── templates/
    └── home.html
```

Your `home.html` contains the HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
</head>

<body>
    <h1>Welcome, Ujjwal!</h1>
</body>
</html>
```

Now Python's job is simply:

> "Take this HTML template and give it some data."

That's where **Jinja2** comes in.

---

## 2. So what exactly is Jinja2?

**Jinja2 is a templating engine.**

Think of it as a system that allows you to write:

```html
<h1>Hello, {{ name }}!</h1>
```

instead of hardcoding:

```html
<h1>Hello, Ujjwal!</h1>
```

Then Python gives Jinja2:

```python
name = "Ujjwal"
```

Jinja2 combines the two:

```text
HTML template
      +
Python data
      ↓
Jinja2
      ↓
Final HTML
```

Result:

```html
<h1>Hello, Ujjwal!</h1>
```

That final HTML is what gets sent to the browser.

---

## 3. This is the important mental model

You currently have:

```text
Python
   ↓
creates HTML string
   ↓
FastAPI
   ↓
Browser
```

With templates:

```text
Python data
    ↓
Jinja2 ← HTML template
    ↓
Final HTML
    ↓
FastAPI
    ↓
Browser
```

So **Jinja2 isn't replacing FastAPI**.

FastAPI is still your web framework.

Jinja2 is simply helping FastAPI generate HTML dynamically.

---

## 4. Why is this useful?

Look at your `posts` list:

```python
posts = [
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
```

Suppose you want a webpage showing **all posts**.

Without Jinja2, you'd have to manually construct HTML:

```python
html = "<html><body>"

for post in posts:
    html += f"""
        <h2>{post["title"]}</h2>
        <p>{post["content"]}</p>
    """

html += "</body></html>"
```

That's mixing:

* Python
* HTML
* data processing

into one giant mess.

With Jinja2, your HTML can contain the loop.

### `home.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
</head>

<body>

    <h1>My Blog</h1>

    {% for post in posts %}

        <article>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
            <small>By {{ post.author }}</small>
        </article>

    {% endfor %}

</body>
</html>
```

Notice the two different syntaxes:

### `{{ }}` → output a value

```html
{{ post.title }}
```

means:

> Put the value of `post.title` here.

### `{% %}` → execute template logic

```html
{% for post in posts %}
```

means:

> Loop through the posts.

And:

```html
{% endfor %}
```

ends the loop.

---

## 5. Then Python passes `posts` to the template

Your FastAPI code becomes something like:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts = [
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


@app.get("/posts")
def get_posts(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "posts": posts,
        },
    )
```

There are three important things happening here.

---

#### i. `Jinja2Templates`

```python
templates = Jinja2Templates(directory="templates")
```

You're basically telling FastAPI:

> "My HTML templates are inside this `templates` directory."

So:

```text
project/
│
├── main.py
│
└── templates/
    └── home.html
```

---

#### ii. `TemplateResponse`

This:

```python
return templates.TemplateResponse(
    "home.html",
    {
        "request": request,
        "posts": posts,
    },
)
```

means roughly:

> Take `home.html`, give it this data, render it using Jinja2, and return the resulting HTML to the browser.

The dictionary:

```python
{
    "request": request,
    "posts": posts,
}
```

is called the **context**.

You're giving the template variables that it can use.

For example:

```python
"posts": posts
```

allows the template to access:

```jinja2
{{ posts }}
```

and:

```jinja2
{% for post in posts %}
```

---

#### iii. Why do we need `request`?

In the tutorial, Corey does this:
```python
def home(request: Request):
```

and then:

```python
{
    "request": request,
}
```

This is partly because Starlette/FastAPI's `TemplateResponse` expects the request to be available in the template context.

Don't get too hung up on this yet.

For now, remember:

```python
request: Request
```

**gives your route function information about the incoming HTTP request.**

And:

```python
"request": request
```

**makes that request object available to the template.**

You'll understand its usefulness better when you start working with things like URLs, forms, authentication, etc.

---

## 6. Jinja2 can do more than variables

This is where templates become really useful.

### Variables

```jinja2
<h1>{{ user_name }}</h1>
```

### Loops

```jinja2
{% for post in posts %}

    <h2>{{ post.title }}</h2>

{% endfor %}
```

### Conditions

```jinja2
{% if posts %}

    <p>There are posts!</p>

{% else %}

    <p>No posts found.</p>

{% endif %}
```

### Access dictionary values

You can do:

```jinja2
{{ post.title }}
```

instead of:

```jinja2
{{ post["title"] }}
```

Jinja2 supports the dot notation here.

---

## 7. Templates also solve code duplication

This becomes **very important** when you build actual applications.

Suppose every page has:

```text
Navbar
----------------
Page content
----------------
Footer
```

You don't want to copy the navbar and footer into every HTML file.

Jinja2 lets you create:

```text
templates/
│
├── base.html
├── home.html
├── posts.html
└── about.html
```

`base.html`:

```html
<!DOCTYPE html>
<html>

<head>
    <title>{% block title %}{% endblock %}</title>
</head>

<body>

    <nav>
        <a href="/">Home</a>
        <a href="/posts">Posts</a>
        <a href="/about">About</a>
    </nav>

    {% block content %}
    {% endblock %}

</body>

</html>
```

Then `home.html`:

```html
{% extends "base.html" %}

{% block title %}
Home
{% endblock %}

{% block content %}

<h1>Welcome to my blog</h1>

{% endblock %}
```

Now the browser receives a complete HTML page, but you didn't have to repeat the navbar, `<html>`, `<head>`, etc.

This concept is called **template inheritance**.

You'll probably encounter it fairly soon in Corey's tutorial.

---

## 8. One very important distinction

Don't confuse these two:

### API endpoint

```python
@app.get("/api/posts")
def get_posts():
    return posts
```

This is primarily returning **data**:

```json
[
    {
        "id": 1,
        "title": "FastAPI is Awesome"
    }
]
```

Usually consumed by:

```text
Frontend
Mobile app
Another backend
JavaScript
etc.
```

### HTML endpoint

```python
@app.get("/posts")
def get_posts(request: Request):
    return templates.TemplateResponse(...)
```

This returns **HTML**:

```html
<!DOCTYPE html>
<html>
...
</html>
```

Usually consumed directly by a browser.

So you can think:

```text
FastAPI
│
├── API routes
│      ↓
│   JSON/data
│
└── HTML routes
       ↓
    Jinja2
       ↓
      HTML
```

And in a larger application, you can actually use **both**.

---

## The one sentence I'd remember

**Jinja2 lets you keep your HTML in separate `.html` files while dynamically inserting Python data and template logic into those files.**

So when you see:

```jinja2
<h1>Hello {{ user.name }}</h1>

{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

don't think of it as some completely different language you need to learn from scratch.

Think:

> **"This is HTML with placeholders and a little bit of logic. Python/FastAPI supplies the data, and Jinja2 turns the template + data into normal HTML."**

That's the core concept. Once that clicks, the rest of Jinja2—loops, conditions, inheritance, includes, filters—becomes much easier.
