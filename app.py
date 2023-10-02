from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
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
            socketio.emit('uploadMessage','Successful Uploading All Data')

@app.route("/")
def start():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    if not check_authentication():
        return redirect(url_for("login"))
    return redirect(url_for("data_upload"))

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
    lines = lines[1:]
    for line in lines:
        datos = line.split(',')
        if not addResearcherCSV(datos[0],datos[1],datos[2],datos[3],datos[4]):
            socketio.emit('uploadMessage','Error uploading Researchers')
    session["loadResearchers"] = True
    check_uploads()
    socketio.emit('uploadMessage','Successful uploading Researchers')

@socketio.on("loadProjects")
def loadProjects_func(data):
    decoded_text = data.decode('utf-8')
    lines = decoded_text.split('\r\n')
    lines = lines[1:]
    for line in lines:
        datos = line.split(',')
        if not addProjectCSV(datos[0],datos[1],datos[2],datos[3],datos[4]):
            socketio.emit('uploadMessage','Error uploading Projects')
    session["loadProjects"] = True
    check_uploads()
    socketio.emit('uploadMessage','Successful uploading Projects')

@socketio.on("loadPublications")
def loadPublications_func(data):
    decoded_text = data.decode('utf-8')
    lines = decoded_text.split('\r\n')
    lines = lines[1:]
    for line in lines:
        datos = line.split(',')
        if not addPublicationsCSV(datos[0],datos[1],datos[2],datos[3]):
            socketio.emit('uploadMessage','Error uploading Publications')
    session["loadPublications"] = True
    check_uploads()
    socketio.emit('uploadMessage','Successful uploading Publications')

@socketio.on("loadResearchersProj")
def loadResearchersProj_func(data):
    decoded_text = data.decode('utf-8')
    lines = decoded_text.split('\r\n')
    lines = lines[1:]
    for line in lines:
        datos = line.split(',')
        if not addAssociateResearcherCSV(datos[0],datos[1]):
            socketio.emit('uploadMessage','Error uploading Researchers-Proj')
    session["loadResearchersProj"] = True
    check_uploads()
    socketio.emit('uploadMessage','Successful uploading Researchers-Proj')

@socketio.on("loadPublicationsProj")
def loadPublicationsProj_func(data):
    decoded_text = data.decode('utf-8')
    lines = decoded_text.split('\r\n')
    lines = lines[1:]
    for line in lines:
        datos = line.split(',')
        if not addAssociateArticleCSV(datos[0],datos[1]):
            socketio.emit('uploadMessage','Error uploading Publications-Proj')
    session["loadPublicationsProj"] = True
    check_uploads()
    socketio.emit('uploadMessage','Successful uploading Publications-Proj')


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
    socketio.run(app, debug=True)
    