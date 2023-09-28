from flask import Flask, jsonify,render_template, redirect, request
from neo4j import GraphDatabase

#conexion con la base de datos
#IMPORTANTE: Agregar datos de la base que se va a usar
driver = GraphDatabase.driver(uri='bolt://localhost:7687',auth=('neo4j','12345678'))
session=driver.session()

api = Flask(__name__) 

#Funciones de POBLACION DE LA BASE


#Esta función crea un investigador en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo: http://127.0.0.1:5050/cargar_invest/juan carmona&phd&tec&juan@hola.com 
@api.route('/cargar_invest/<string:nombre>&<string:titulo>&<string:institucion>&<string:email>', methods = ['GET', 'POST'])
def crearInvest(nombre, titulo, institucion, email):
    query ="create (i:Investigador{Nombre:$nombre,Titulo:$titulo, Institucion:$institucion, Email:$email})"
    map_ ={"nombre":nombre, "titulo":titulo, "institucion":institucion, "email":email}
    try:
        session.run(query,map_)
        return ("Investigador creado con exito")
    except Exception as e:
        return(str(e))
    
#Esta función crea un proyecto en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo http://127.0.0.1:5050/cargar_proy/aguas Negras&2012&8&biologia
@api.route('/cargar_proy/<string:titulo>&<int:anno>&<int:duracion>&<string:area>', methods = ['GET', 'POST'])
def crearProy(titulo, anno, duracion, area):
    query ="create (p:Proyecto{Titulo:$titulo,Anno:$anno, Duracion:$duracion, Area:$area})"
    map_ ={"titulo":titulo, "anno":anno, "duracion":duracion, "area":area}
    try:
        session.run(query,map_)
        return ("Proyecto creado con exito")
    except Exception as e:
        return(str(e))   
#Esta función crea un proyecto en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo http://127.0.0.1:5050/cargar_public/resultados de aguas&2012&ecorevista
@api.route('/cargar_public/<string:titulo>&<int:anno>&<string:revista>', methods = ['GET', 'POST'])
def crearPublic(titulo, anno, revista):
    query ="create (pu:Publicacion{Titulo:$titulo,Anno:$anno, Revista:$revista})"
    map_ ={"titulo":titulo, "anno":anno, "revista":revista}
    try:
        session.run(query,map_)
        return ("Publicacion creado con exito")
    except Exception as e:
        return(str(e))
#Esta función crea una relacion entre un investigador y un proyecto en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo http://127.0.0.1:5050/invest_proy/1&2 NOTA: los parametros son los id de cada uno
@api.route('/invest_proy/<int:investigador>&<int:proyecto>', methods = ['GET', 'POST'])
def crear_relacion_invest_proy(investigador, proyecto):
    query ="Match(i:Investigador),(p:Proyecto) Where id(i)=$investigador and id(p)=$proyecto Create (i)-[r:participaEn]->(p)"
    map_ ={"investigador":investigador,"proyecto":proyecto}
    try:
        session.run(query,map_)
        return ("El investigador se ha relacionado al proyecto")
    except Exception as e:
        return(str(e))
#Esta función crea una relacion entre un investigador y un proyecto en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo http://127.0.0.1:5050/proy_pub/1&2 NOTA: los parametros son los id de cada uno
@api.route('/proy_pub/<int:proyecto>&<int:publicacion>', methods = ['GET', 'POST'])
def crear_relacion_proy_publicacion(proyecto, publicacion):
    query ="Match(pu:Publicacion),(p:Proyecto) Where id(pu)=$publicacion and id(p)=$proyecto Create (p)-[r:sePublicaEn]->(pu)"
    map_ ={"publicacion":publicacion,"proyecto":proyecto}
    try:
        session.run(query,map_)
        return ("El proyecto se ha relacionado a la publicacion")
    except Exception as e:
        return(str(e))
    
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
#Esta función es solo una consulta, al ingresar el query se obtiene las 5 instituciones con más proyectos y la cantidad de proyectos inscritos a esta.
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

if __name__ == "__main__":
    api.run(port=5050)
"""
@app.route('/products', methods=['GET']) # se agregan todas las funciones 
def  getProducts():
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True, port=4000) #se reinicia por cada cambio"""
