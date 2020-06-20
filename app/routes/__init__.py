from flask import render_template
from markdown2 import Markdown
from app import app


@app.route('/', methods=['GET'])
def root():
    markdowner = Markdown()
    content = markdowner.convert(open('README.md').read(9999))
    return render_template('template.html', content=content)
