import utils
import os
import time
import json
import markdown

#article2.md read of this file and convert mark down to html using this function.mro
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
INDUSTRY_KEYWORD = os.environ.get('INDUSTRY_KEYWORD', 'Vector databases')



file = "data/"+INDUSTRY_KEYWORD+"/article.md"

def read_markdown_file(file):
    with open(file, "r") as f:
        return f.read()

mark=read_markdown_file(file)

def generate_html_from_markdown(mark):
    html = markdown.markdown(mark)
    
    return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="keywords" content="{meta_keywords}">
        <meta name="description" content="{meta_description}">
        <title>{title}</title>
    </head>
    <body>
        {text}
    </body>
    </html>""".format(meta_keywords="keywords", meta_description="description", title="KYC Providers 2023: A Comparative Analysis of Features and Prices", text=html)

html=generate_html_from_markdown(mark)

#save html to file
def save_html_to_file(html):
    with open("data/"+INDUSTRY_KEYWORD+"/article.html", "w") as f:
        f.write(html)

save_html_to_file(html)

