from flask import Flask, jsonify,render_template, redirect, request
from neo4j import GraphDatabase

#conexion con la base de datos
#IMPORTANTE: Agregar datos de la base que se va a usar
driver = GraphDatabase.driver(uri='bolt://localhost:7687',auth=('neo4j','12345678'))
session=driver.session()

api = Flask(__name__) 

#Funciones de POBLACION DE LA BASE

@api.route('/cargar_invest/<string:nombre>&<string:titulo>&<string:institucion>&<string:email>', methods = ['GET', 'POST'])
def Create_node(nombre, titulo, institucion, email):
    query ="create (i:Investigador{Nombre:$nombre,Titulo:$titulo, Institucion:$institucion, Email:$email})"
    map_ ={"nombre":nombre, "titulo":titulo, "institucion":institucion, "email":email}
    try:
        session.run(query,map_)
        return ("Investigador creado con exito")
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
