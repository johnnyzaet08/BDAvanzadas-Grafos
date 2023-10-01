from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import csv
from api import *

app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"
app.config["SECRET_KEY"] = "BDA-2023"
app.config['VALID_PASSWORD'] = 'asd123'
app.config['VALID_USERNAME'] = 'asd123'

CORS(app)
socketio.init_app(app)

loadData = True

# Authentication check function
def check_authentication():
    if "username" in session:
        return True
    return False

def check_uploads():
    data = ["loadResearchers", "loadProjects", "loadPublications", "loadResearchersProj", "loadPublicationsProj"]
    checkCreate = True
    checkData = True
    for i in data:
        if i not in session:
            checkCreate = False
            break

    if checkCreate:
        for i in data:
            if not session[i]:
                checkData = False
                break
        
        if checkData:
            global loadData
            loadData = True

@app.route("/")
def start():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if app.config['VALID_PASSWORD'] == password and app.config['VALID_USERNAME'] == username:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login", message="Invalid Credentials"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/data_upload", methods=["GET", "POST"])
def data_upload():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("data_upload.html")

@socketio.on("loadResearchers")
def loadResearchers_func(data):
    decoded_text = data.decode('utf-8')
    lines = decoded_text.split('\r\n')
    print(lines)
    for line in lines:
        print(line)
    # Si esta correcto, tirar load a True
    session["loadResearchers"] = True
    check_uploads()
    return None

@socketio.on("loadProjects")
def loadProjects_func(data):
    # Subir todo el csv
    lector = csv.reader(data)
    for fila in lector:
        id,titulo_proyecto,anno_inicio,duracion_meses,area_conocimiento = fila
        print(id,titulo_proyecto,anno_inicio,duracion_meses,area_conocimiento)
    # Si esta correcto, tirar load a True
    session["loadProjects"] = True
    check_uploads()
    return None

@socketio.on("loadPublications")
def loadPublications_func(data):
    # Subir todo el csv
    lector = csv.reader(data)
    for fila in lector:
        id_pub,titulo_publicacion,anno_publicacion,nombre_revista = fila
        print(id_pub,titulo_publicacion,anno_publicacion,nombre_revista)
    # Si esta correcto, tirar load a True
    session["loadPublications"] = True
    check_uploads()
    return None

@socketio.on("loadResearchersProj")
def loadResearchersProj_func(data):
    # Subir todo el csv
    lector = csv.reader(data)
    for fila in lector:
        idInv,idProy= fila
        print(idInv,idProy)
    # Si esta correcto, tirar load a True
    session["loadResearchersProj"] = True
    check_uploads()
    return None

@socketio.on("loadPublicationsProj")
def loadPublicationsProj_func(data):
    # Subir todo el csv
    lector = csv.reader(data)
    for fila in lector:
        idProyecto,idArt= fila
        print(idProyecto,idArt)
    # Si esta correcto, tirar load a True
    session["loadPublicationsProj"] = True
    check_uploads()
    return None


@app.route("/researchers", methods=["GET"])
def researchers():
    if not check_authentication():
        return redirect(url_for("login"))

    if loadData:
        return render_template("researchers.html")
    
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/projects", methods=["GET", "POST"])
def projects():
    if not check_authentication():
        return redirect(url_for("login"))
        
    if loadData:
        return render_template("projects.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/publications", methods=["GET", "POST"])
def publications():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
        
    if loadData:
        return render_template("publications.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/associate_researcher", methods=["GET", "POST"])
def associate_researcher():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
        
    if loadData:
        return render_template("associate_researcher.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/associate_article", methods=["GET", "POST"])
def associate_article():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
        
    if loadData:
        return render_template("associate_article.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/top_knowledge_areas", methods=["GET", "POST"])
def top_knowledge_areas():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
        
    if loadData:
        return render_template("top_knowledge_areas.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/top_institutions", methods=["GET", "POST"])
def top_institutions():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
    
    if loadData:
        return render_template("top_institutions.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/top_researchers", methods=["GET", "POST"])
def top_researchers():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
        
    if loadData:
        return render_template("top_researchers.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/search_researcher", methods=["GET", "POST"])
def search_researcher():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        None
    
    if loadData:
        return render_template("search_researcher.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/search_project", methods=["GET", "POST"])
def search_project():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if loadData:
        return render_template("search_project.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/search_publications", methods=["GET", "POST"])
def search_publications():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if loadData:
        return render_template("search_publications.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/search_by_area", methods=["GET", "POST"])
def search_by_area():
    if not check_authentication():
        return redirect(url_for("login"))
    
    if loadData:
        return render_template("search_by_area.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


@app.route("/search_colleagues", methods=["GET", "POST"])
def search_colleagues():
    if not check_authentication():
        return redirect(url_for("login"))

    if loadData:
        return render_template("search_colleagues.html")
        
    return redirect(url_for("data_upload", message="Please Load Data First"))


if __name__ == "__main__":
    socketio.run(app)
    