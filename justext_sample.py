import requests
import justext

response = requests.get("http://planet.python.org/")
paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
        print paragraph.text
