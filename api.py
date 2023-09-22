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
    
#Esta función crea un proyecto en la base de datos: debe ser llamado desde frontend de la siguiente manera: Ejemplo http://127.0.0.1:5050/cargar_proy/aguas Negras&2012&8&planetahoy
@api.route('/cargar_proy/<string:titulo>&<int:anno>&<int:duracion>&<string:revista>', methods = ['GET', 'POST'])
def crearProy(titulo, anno, duracion, revista):
    query ="create (p:Proyecto{Titulo:$titulo,Anno:$anno, Duracion:$duracion, Revista:$revista})"
    map_ ={"titulo":titulo, "anno":anno, "duracion":duracion, "revista":revista}
    try:
        session.run(query,map_)
        return ("Proyecto creado con exito")
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
