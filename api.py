from flask_socketio import SocketIO
from neo4j import GraphDatabase

socketio = SocketIO()

NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '12345678'

singleton = False
base = None

def get_neo4j_session():
    global base
    if not singleton:
        base = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        ).session()
        return base
    else:
        return base


################################################ ADD / UPDATE ###########################################

# Esta función crea un investigador en la base de datos: debe ser llamado desde frontend
@socketio.on("researchersAPI/add")
def addResearcher(nombre, titulo, institucion, email):
    query = ("MATCH (i:Investigador) WITH COALESCE(MAX(i.id), 0) AS max_id CREATE (newInvestigator:Investigador { "
             "id: max_id + 1, nombre_completo: $nombre, titulo_academico: $titulo, institucion: "
             "$institucion, email: $email}) RETURN newInvestigator;")
    map_ = {"nombre": nombre, "titulo": titulo, "institucion": institucion, "email": email}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("researchersAPI", "Successful")
    except Exception as e:
        socketio.emit("researchersAPI", e)

def addResearcherCSV(id, nombre, titulo, institucion, email):
    query = ("CREATE (newInvestigator:Investigador { "
             "id: $id, nombre_completo: $nombre, titulo_academico: $titulo, institucion: "
             "$institucion, email: $email})")
    map_ = {"id":id, "nombre": nombre, "titulo": titulo, "institucion": institucion, "email": email}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            return True
    except Exception as e:
        socketio.emit("researchersAPI", e)
        return False


@socketio.on("researchersAPI/update")
def updateResearcher(id, nombre, titulo, institucion, email):
    query = (
        "MATCH (n:Investigador) WHERE n.id = identi SET n.nombre_completo = $nombre, n.titulo_academico = $titulo, "
        "n.institucion = $titulo, n.email = $email RETURN n")
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
    query = ("match (i:Investigador) return i.nombre_completo")
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
    query = ("MATCH (p:Proyecto) WITH COALESCE(MAX(p.idPry), 0) AS max_id CREATE (p:Proyecto { idPry: max_id + 1, "
             "titulo_proyecto: $titulo, anno_inicio: $anno, duracion_meses: $duracion, area_conocimiento: $area}) "
             "RETURN p;")
    map_ = {"titulo": titulo, "anno": anno, "duracion": duracion, "area": area}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("projectsAPI", "Successful")
    except Exception as e:
        socketio.emit("projectsAPI", e)

def addProjectCSV(id, titulo, anno, duracion, area):
    query = ("CREATE (p:Proyecto { idPry: $id, "
             "titulo_proyecto: $titulo, anno_inicio: $anno, duracion_meses: $duracion, area_conocimiento: $area}) ")
    map_ = {"id":id, "titulo": titulo, "anno": anno, "duracion": duracion, "area": area}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            return True
    except Exception as e:
        return False

@socketio.on("projectsAPI/update")
def updateProject(id, titulo, anno, duracion, area):
    query = (
        "MATCH (n:Proyecto) WHERE n.idPry = $identi SET n.titulo_proyecto = $titulo, n.anno_inicio = $anno, n.duracion_meses = $duracion, n.area_conocimiento = $area RETURN n")
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
    query = ("match (p:Proyecto) return p.titulo_proyecto")
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
    query = ("MATCH (pu:Publicacion) WITH COALESCE(MAX(pu.idPub), 0) AS max_id CREATE (pu:Publicacion { idPub: max_id "
             "+ 1, titulo_publicacion: $titulo, anno_publicacion: $anno, nombre_revista: $revista}) RETURN pu;")
    map_ = {"titulo": titulo, "anno": anno, "revista": revista}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("publicationsAPI", "Successful")
    except Exception as e:
        socketio.emit("publicationsAPI", e)

def addPublicationsCSV(id, titulo, anno, revista):
    query = ("CREATE (pu:Publicacion { idPub: $id, titulo_publicacion: $titulo, anno_publicacion: $anno, nombre_revista: $revista})")
    map_ = {"id":id, "titulo": titulo, "anno": anno, "revista": revista}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            return True
    except Exception as e:
        return False


@socketio.on("publicationsAPI/update")
def updatePublications(id, titulo, anno, revista):
    query = ("MATCH (n:Publicacion) WHERE n.idPub = $identi SET n.titulo_publicacion = $titulo, n.anno_publicacion = "
             "$anno, n.nombre_revista = $revista RETURN n")
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
    query = ("match (pu:Publicacion) return pu.titulo_publicacion")
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
    query = "Match(i:Investigador),(p:Proyecto) Where i.nombre_completo=$investigador and p.titulo_proyecto=$proyecto Create (i)-[r:participaEn]->(p)"
    map_ = {"investigador": researcher, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("associate_researcherAPI", "Successful")
    except Exception as e:
        socketio.emit("associate_researcherAPI", e)

def addAssociateResearcherCSV(researcher, project):
    query = "Match(i:Investigador),(p:Proyecto) Where i.id=$investigador and p.idPry=$proyecto Create (i)-[r:participaEn]->(p)"
    map_ = {"investigador": researcher, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            return True
    except Exception as e:
        return False


# Esta función crea una relacion entre un investigador y un proyecto en la base de datos
@socketio.on("associate_articleAPI/add")
def addAssociateArticle(publication, project):
    query = "Match(pu:Publicacion),(p:Proyecto) Where pu.titulo_publicacion=$publicacion and p.titulo_proyecto=$proyecto Create (p)-[r:sePublicaEn]->(pu)"
    map_ = {"publicacion": publication, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            socketio.emit("associate_articleAPI", "Successful")
    except Exception as e:
        socketio.emit("associate_articleAPI", e)

def addAssociateArticleCSV(project, publication):
    query = "Match(pu:Publicacion),(p:Proyecto) Where pu.idPub=$publicacion and p.idPry=$proyecto Create (p)-[r:sePublicaEn]->(pu)"
    map_ = {"publicacion": publication, "proyecto": project}
    try:
        with get_neo4j_session() as session:
            session.run(query, map_)
            return True
    except Exception as e:
        return False


############################################### CONSULTAS #################################################
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


@socketio.on("findProjectByNameAPI")
def findProjectByName(name):
    query = ("MATCH (p:Proyecto) WHERE p.titulo_proyecto =~ '(?i).*{name}.*'RETURN p.idPry as ".format(name=name) +
             "idPry,p.titulo_proyecto as "
             "titulo_proyecto , p.area_conocimiento as area_conocimiento, p.anno_inicio as anno_inicio, p.duracion_meses as duracion_meses, p.area_conocimiento "
             "AS proyecto, [(i:Investigador)-[:participaEn]->(p) | {nombre_completo: i.nombre_completo, "
             "titulo_academico: i.titulo_academico, institucion: i.institucion, email: i.email, id:i.id}] AS "
             "investigadores,"
             "[(pub:Publicacion)<-[:sePublicaEn]-(p) | {titulo_publicacion: pub.titulo_publicacion, anno_publicacion: "
             "pub.anno_publicacion, nombre_revista: pub.nombre_revista}] AS publicaciones;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("findProjectByNameAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("findProjectByNameAPI/get", e)


@socketio.on("findPublicationByNameAPI")
def findPublicationByName(name):
    query = (
                "MATCH (publicacion:Publicacion) WHERE publicacion.titulo_publicacion =~ '(?i).*{name}.*' OPTIONAL MATCH (".format(
                    name=name) +
                "publicacion)<-[:sePublicaEn]-(proyecto:Proyecto) RETURN publicacion.anno_publicacion AS "
                "anno_publicacion, publicacion.titulo_publicacion AS titulo_publicacion, publicacion.nombre_revista AS "
                "nombre_revista, publicacion.idPub AS idPub, proyecto.titulo_proyecto AS titulo_proyecto;")
    print(query)
    try:
        with get_neo4j_session() as session:
            resultado = session.run(query)
            data = resultado.data()
            json_data = [dict(record) for record in data]
            socketio.emit("findPublicationByNameAPI/get", json_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        socketio.emit("findPublicationByNameAPI/get", e)


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
