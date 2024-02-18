from flask import Flask
from recipe_generation import create_recipe

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return flask.render_template("index.html")

if __name__ == '__main__':
   app.run()
