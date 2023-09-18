from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from neo4j import GraphDatabase
from flask_cors import CORS
import time

app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"

app.config["SECRET_KEY"] = "BDA-2023"
app.config['NEO4J_URI'] = 'bolt://localhost:7687'  # Replace with your Neo4j URI
app.config['NEO4J_USER'] = 'neo4j'
app.config['NEO4J_PASSWORD'] = 'BDA2023'
app.config['VALID_PASSWORD'] = 'asd123'
app.config['VALID_USERNAME'] = 'asd123'

CORS(app)
socketio = SocketIO(app)

# Database check fuction
def get_neo4j_session():
    return GraphDatabase.driver(
        app.config['NEO4J_URI'],
        auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD'])
    ).session()

# Authentication check function
def check_authentication():
    if "username" in session:
        return True
    return False


@app.route("/")
def index():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if app.config['VALID_PASSWORD'] == password and app.config['VALID_USERNAME'] == username:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login", message="Invalid Credentials"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/data_upload")
def data_upload():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("data_upload.html")


@app.route("/researchers")
def researchers():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("researchers.html")


@app.route("/projects")
def projects():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("projects.html")


@app.route("/publications")
def publications():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("publications.html")


@app.route("/associate_researcher")
def associate_researcher():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("associate_researcher.html")


@app.route("/associate_article")
def associate_article():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("associate_article.html")


@app.route("/top_knowledge_areas")
def top_knowledge_areas():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("top_knowledge_areas.html")


@app.route("/top_institutions")
def top_institutions():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("top_institutions.html")


@app.route("/top_researchers")
def top_researchers():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("top_researchers.html")


@app.route("/search_researcher")
def search_researcher():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("search_researcher.html")


@app.route("/search_project")
def search_project():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("search_project.html")


@app.route("/search_publications")
def search_publications():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("search_publications.html")


@app.route("/search_by_area")
def search_by_area():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("search_by_area.html")


@app.route("/search_colleagues")
def search_colleagues():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("search_colleagues.html")


@socketio.on("connectState")
def handle_connect(message):
    if(message == 'successful'):
        return None
    else:
        return redirect(url_for("logout"))

@socketio.on("disconnect")
def handle_disconnect():
    return None


@socketio.on("custom_event")
def handle_custom_event(data):
    return None


if __name__ == "__main__":
    socketio.run(app, debug=True)
