from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.static_folder = 'static'
app.static_url_path = '/static'
app.config['SECRET_KEY'] = 'BDA-2023'

CORS(app)
socketio = SocketIO(app)

valid_password = "asd123"
valid_username = "asd123"

# Authentication check function
def check_authentication():
    if 'username' in session:
        return True
    return False

@app.route('/')
def index():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    if valid_password == password and valid_username == username:
      session['username'] = username
      return redirect(url_for('index'))
    else:
      return "Invalid login credentials. Please try again."

  return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/data_upload')
def data_upload():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('data_upload.html')

@app.route('/researchers')
def researchers():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('researchers.html')

@app.route('/projects')
def projects():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('projects.html')

@app.route('/publications')
def publications():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('publications.html')

@app.route('/associate_researcher')
def associate_researcher():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('associate_researcher.html')

@app.route('/associate_article')
def associate_article():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('associate_article.html')

@app.route('/top_knowledge_areas')
def top_knowledge_areas():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('top_knowledge_areas.html')

@app.route('/top_institutions')
def top_institutions():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('top_institutions.html')

@app.route('/top_researchers')
def top_researchers():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('top_researchers.html')

@app.route('/search_researcher')
def search_researcher():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('search_researcher.html')

@app.route('/search_project')
def search_project():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('search_project.html')

@app.route('/search_publications')
def search_publications():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('search_publications.html')

@app.route('/search_by_area')
def search_by_area():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('search_by_area.html')

@app.route('/search_colleagues')
def search_colleagues():
    if not check_authentication():
        return redirect(url_for('login'))
    return render_template('search_colleagues.html')

@socketio.on('connect')
def handle_connect():
    return None

@socketio.on('disconnect')
def handle_disconnect():
    return None

@socketio.on('custom_event')
def handle_custom_event(data):
    return None

if __name__ == '__main__':
    socketio.run(app, debug=True)
