from flask_socketio import SocketIO
from neo4j import GraphDatabase

socketio = SocketIO()

NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '12345678'


def get_neo4j_session():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    ).session()


################################################ ADD / UPDATE ###########################################

# Esta función crea un investigador en la base de datos: debe ser llamado desde frontend
@socketio.on("researchersAPI/add")
def addResearcher(nombre, titulo, institucion, email):
    query = "CREATE (i:Investigador{Nombre:$nombre,Titulo:$titulo, Institucion:$institucion, Email:$email})"
    map_ = {"nombre": nombre, "titulo": titulo, "institucion": institucion, "email": email}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("researchersAPI", "Successful")
    except Exception as e:
        socketio.emit("researchersAPI", e)


@socketio.on("researchersAPI/update")
def updateResearcher(id, nombre, titulo, institucion, email):
    query = (
        "MATCH (n) WHERE id(n) = $identi SET n.Nombre = $nombre, n.Titulo = $titulo, n.Institucion = $institucion, n.Email = $email RETURN n")
    map_ = {"identi": int(id), "nombre": nombre, "titulo": titulo, "institucion": institucion, "email": email}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("researchersAPI", "Successful")
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("researchersAPI", e)


@socketio.on("researchersAPI/get")
def getResearcher():
    query = ("match (i:Investigador) return i.Nombre")
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("researchersAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("researchersAPI", e)


# Esta función crea un proyecto en la base de datos
@socketio.on("projectsAPI/add")
def addProject(titulo, anno, duracion, area):
    query = "create (p:Proyecto{Titulo:$titulo,Anno:$anno, Duracion:$duracion, Area:$area})"
    map_ = {"titulo": titulo, "anno": anno, "duracion": duracion, "area": area}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("projectsAPI", "Successful")
    except Exception as e:
        socketio.emit("projectsAPI", e)


@socketio.on("projectsAPI/update")
def updateProject(id, titulo, anno, duracion, area):
    query = (
        "MATCH (n) WHERE id(n) = $identi SET n.Titulo = $titulo, n.Anno = $anno, n.Duracion = $duracion, n.Area = $area RETURN n")
    map_ = {"identi": int(id), "titulo": titulo, "anno": anno, "duracion": duracion, "area": area}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("projectsAPI", "Successful")
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("projectsAPI", e)


@socketio.on("projectsAPI/get")
def getResearcher():
    query = ("match (p:Proyecto) return p.Titulo")
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("projectsAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("projectsAPI", e)


# Esta función crea una publicacion en la base de datos
@socketio.on("publicationsAPI/add")
def addPublications(titulo, anno, revista):
    query = "create (pu:Publicacion{Titulo:$titulo,Anno:$anno, Revista:$revista})"
    map_ = {"titulo": titulo, "anno": anno, "revista": revista}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("publicationsAPI", "Successful")
    except Exception as e:
        socketio.emit("publicationsAPI", e)


@socketio.on("publicationsAPI/update")
def updatePublications(id, titulo, anno, revista):
    query = ("MATCH (n) WHERE id(n) = $identi SET n.Titulo = $titulo, n.Anno = $anno, n.Revista = $revista RETURN n")
    map_ = {"identi": int(id), "titulo": titulo, "anno": anno, "revista": revista}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("publicationsAPI", "Successful")
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("publicationsAPI", e)


@socketio.on("publicationsAPI/get")
def getPublications():
    query = ("match (pu:Publicacion) return pu.Titulo")
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("publicationsAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("publicationsAPI", e)


# Esta función crea una relacion entre un investigador y un proyecto en la base de datos
@socketio.on("associate_researcherAPI/add")
def addAssociateResearcher(researcher, project):
    query = "Match(i:Investigador),(p:Proyecto) Where i.Nombre=$investigador and p.Titulo=$proyecto Create (i)-[r:participaEn]->(p)"
    map_ = {"investigador": researcher, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("associate_researcherAPI", "Successful")
    except Exception as e:
        socketio.emit("associate_researcherAPI", e)


# Esta función crea una relacion entre un investigador y un proyecto en la base de datos
@socketio.on("associate_articleAPI/add")
def addAssociateArticle(publication, project):
    query = "Match(pu:Publicacion),(p:Proyecto) Where pu.Titulo=$publicacion and p.Titulo=$proyecto Create (p)-[r:sePublicaEn]->(pu)"
    map_ = {"publicacion": publication, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("associate_articleAPI", "Successful")
    except Exception as e:
        socketio.emit("associate_articleAPI", e)


@socketio.on("topKnowledgeAPI")
def topKnowledgeAreas():
    query = ("MATCH (p:Proyecto) WITH p.area_conocimiento AS area_conocimiento, COUNT(p) AS cantidad_proyectos RETURN "
             "area_conocimiento, cantidad_proyectos ORDER BY cantidad_proyectos DESC LIMIT 5;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("topKnowledgeAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("topKnowledgeAPI/get", e)


@socketio.on("topInstitutionsAPI")
def topInstitutions():
    query = ("MATCH (i:Investigador)-[:participaEn]->(p:Proyecto) WITH i.institucion AS institucion, COUNT(p) AS "
             "cantidad_proyectos RETURN institucion, cantidad_proyectos ORDER BY cantidad_proyectos DESC LIMIT 5;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("topInstitutionsAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("topInstitutionsAPI/get", e)

@socketio.on("topResearchersAPI")
def topResearchers():
    query = ("MATCH (i:Investigador)-[:participaEn]->(p:Proyecto) WITH i, i.institucion AS institucion, COUNT(p) AS "
             "cantidad_proyectos RETURN i.nombre_completo AS nombre_completo, institucion, cantidad_proyectos ORDER "
             "BY cantidad_proyectos DESC LIMIT 5;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("topResearchersAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("topResearchersAPI/get", e)

@socketio.on("findResearcherByNameAPI")
def findResearcherByName(name):
    query = ("MATCH (i:Investigador) WHERE i.nombre_completo =~ '(?i).*{name}.*' ".format(name=name) +
             "OPTIONAL MATCH (i)-[:participaEn]->(p:Proyecto)"
             "RETURN i.id as id, i.nombre_completo AS nombre_completo, i.titulo_academico AS titulo_academico, "
             "i.institucion AS institucion, i.email as email, COLLECT(p) AS proyectos;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("findResearcherByNameAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("findResearcherByNameAPI/get", e)

'''
#############################CONSULTAS#########################################
#Esta función es solo una consulta, al ingresar el query se obtiene las 5  areas de interés con más proyectos y la cantidad de proyectos inscritos en este.
#Retorna en formato json
@api.route('/top_proyectos', methods = ['GET'])
def top5Proyectos():
    query ="""MATCH (p:Proyecto)
            WITH p.Area AS area, COUNT(p) AS cantidadProyectos
            ORDER BY cantidadProyectos DESC
            LIMIT 5
            RETURN area, cantidadProyectos"""
    try:
        resultado=session.run(query)
        data = resultado.data()
        return (jsonify(data))
    except Exception as e:
        return(str(e))

# Esta función es solo una consulta, al ingresar el query se obtiene las 5 instituciones con más proyectos y la cantidad de proyectos inscritos a esta.
#Retorna en formato json
@api.route('/top_instituciones', methods = ['GET'])
def top5Instituciones():
    query ="""MATCH (p:Proyecto)
            WITH p.Institucion AS institucion, COUNT(p) AS cantidadProyectos
            ORDER BY cantidadProyectos DESC
            LIMIT 5
            RETURN institucion, cantidadProyectos"""
    try:
        resultado=session.run(query)
        data = resultado.data()
        return (jsonify(data))
    except Exception as e:
        return(str(e))
    
#Esta función es solo una consulta, al ingresar el query se obtiene los 5 investigadores con más proyectos y la cantidad de proyectos inscritos a estos.
#Retorna en formato json
@api.route('/top_investigadores', methods = ['GET'])
def top5Investigadores():
    query ="""MATCH (i:Investigador)-[:participaEn]->(p:Proyecto)
            WITH i, COUNT(p) AS cantidadProyectos
            ORDER BY cantidadProyectos DESC
            LIMIT 5
            RETURN i.Nombre, i.Institucion, cantidadProyectos"""
    try:
        resultado=session.run(query)
        data = resultado.data()
        return (jsonify(data))
    except Exception as e:
        return(str(e))
'''
