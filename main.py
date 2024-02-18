from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return flask.render_template("index.html")

if __name__ == '__main__':
   app.run()