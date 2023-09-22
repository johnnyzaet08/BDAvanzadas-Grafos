from flask import Flask, jsonify,render_template, redirect, request
from neo4j import GraphDatabase

#conexion con la base de datos
driver = GraphDatabase.driver(uri='bolt://localhost:7687',auth=('neo4j','12345678'))
session=driver.session()

api = Flask(__name__) 

#rutas

@api.route('/create/<string:nombre>&<int:id>', methods = ['GET', 'POST'])
def Create_node(nombre, id):
    query ="create (n:Employee{NAME:$nombre,ID:$id})"
    map_ ={"nombre":nombre, "id":id}
    try:
        session.run(query,map_)
        return (f"empleado creado")
    except Exception as e:
        return("error")
if __name__ == "__main__":
    api.run(port=5050)
"""
@app.route('/products', methods=['GET']) # se agregan todas las funciones 
def  getProducts():
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True, port=4000) #se reinicia por cada cambio"""
