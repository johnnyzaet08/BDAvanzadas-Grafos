//*****Carga de tablas*****
//Cargar investigadores
LOAD CSV WITH HEADERS FROM 'file:///investigadores.csv' AS row
CREATE (:Investigador {
  id: toInteger(row.id),
  nombre_completo: row.nombre_completo,
  titulo_academico: row.titulo_academico,
  institucion: row.institucion,
  email: row.email
});

//Cargar Proyectos
LOAD CSV WITH HEADERS FROM 'file:///proyectos.csv' AS row
CREATE (:Proyecto {
  idPry: toInteger(row.idPry),
  titulo_proyecto: row.titulo_proyecto,
  anno_inicio: toInteger(row.anno_inicio),
  duracion_meses: toInteger(row.duracion_meses),
  area_conocimiento: row.area_conocimiento
});

//Cargar publicaciones
LOAD CSV WITH HEADERS FROM 'file:///publicaciones.csv' AS row
CREATE (:Publicacion {
  idPub: toInteger(row.idPub),
  titulo_publicacion: row.titulo_publicacion,
  anno_publicacion: toInteger(row.anno_publicacion),
  nombre_revista: row.nombre_revista
});

//Cargar investigadores asociados a proyectos
LOAD CSV WITH HEADERS FROM 'file:///InvestigadoresProy.csv' AS row
MATCH (investigador:Investigador {id: toInteger(row.idInv)})
MATCH (proyecto:Proyecto {idPry: toInteger(row.idProy)})
CREATE (investigador)-[:participaEn]->(proyecto);

//Cargar publicaciones asociadas a proyectos
LOAD CSV WITH HEADERS FROM 'file:///PublicacionesProy.csv' AS row
MATCH (proyecto:Proyecto {idPry: toInteger(row.idProyecto)})
MATCH (publicacion:Publicacion {idPub: toInteger(row.idArt)})
CREATE (publicacion)<-[:sePublicaEn]-(proyecto);


//*****Actualizacion de datos*****
//Actualiza los valores de una publicacion por su ID
MATCH (p:Publicacion {idPub: 1})
SET p.titulo_publicacion = 'Nuevo titulo',
    p.anno_publicacion = 2023,
    p.nombre_revista = 'Nombre revista';

//Actualiza los valores de un proyecto por su ID
MATCH (p:Proyecto {idPry: 1})
SET p.titulo_proyecto = 'Nuevo Título',
    p.anno_inicio = 2023,
    p.duracion_meses = 12,
    p.area_conocimiento = 'Nueva Área';

//Actualiza los valores de una investigacion por su ID
MATCH (i:Investigador {id: 1})
SET i.nombre_completo = 'Nuevo Nombre',
    i.titulo_academico = 'Nuevo Título Académico',
    i.institucion = 'Nueva Institución',
    i.email = 'nuevo_email@example.com';


//______Busqueda de datos_________
//Investigador
MATCH (i:Investigador)
RETURN i;

//Proyecto
MATCH (p:Proyecto)
RETURN p;

//Publicaciones
MATCH (p:Publicacion)
RETURN p;

//_____Busqueda especifica______
//Retorna solo los titulos de los proyectos
MATCH (p:Proyecto)
RETURN p.titulo_proyecto;

//Busqueda de area de conocimiento por proyecto
MATCH (p:Proyecto)
RETURN p.area_conocimiento;

//Busqueda de investigador por nombre, retorna su info y los proyectos donde trabaja
MATCH (i:Investigador {nombre_completo: 'Nombre'})-[:participaEn]->(p:Proyecto)
RETURN i.id, i.titulo_academico, i.institucion, i.email, COLLECT(p) AS proyectos;

//Busqueda por nombre por parecidos
MATCH (i:Investigador)
WHERE i.nombre_completo =~ '(?i).*Nombre.*'
OPTIONAL MATCH (i)-[:participaEn]->(p:Proyecto)
RETURN i.id as id, i.nombre_completo AS nombre_completo, i.titulo_academico AS titulo_academico, i.institucion AS institucion, i.email as email, COLLECT(p) AS proyectos;


//Busqueda de proyectos a partir de nombre. Retorna info del proyecto, de los investigadores y de las publicaciones asociadas
MATCH (p:Proyecto)
WHERE p.titulo_proyecto =~ '(?i).*Nombre_Proyecto.*'
RETURN p.idPry as idPry,p.titulo_proyecto as titulo_proyecto , p.anno_inicio as anno_inicio, p.duracion_meses as duracion_meses, p.area_conocimiento AS proyecto,
       [(i:Investigador)-[:participaEn]->(p) | {nombre_completo: i.nombre_completo, titulo_academico: i.titulo_academico, institucion: i.institucion, email: i.email}] AS investigadores,
       [(pub:Publicacion)<-[:sePublicaEn]-(p) | {titulo_publicacion: pub.titulo_publicacion, anno_publicacion: pub.anno_publicacion, nombre_revista: pub.nombre_revista}] AS publicaciones;

//______Asociaciones_______
//Asociar investigador a proyecto por ID
MATCH (i:Investigador), (p:Proyecto)
WHERE i.id = 1 AND p.idPry = 2 // Cambia 1 y 2 a los ID reales del investigador y el proyecto
CREATE (i)-[:participaEn]->(p);

//Asociar investigador a proyecto por nombres
MATCH (i:Investigador), (p:Proyecto)
WHERE i.nombre_completo = 'Nombre del Investigador' AND p.titulo_proyecto = 'Título del Proyecto'
CREATE (i)-[:participaEn]->(p);

//Asociar un articulo a un proyecto por ID
MATCH (pub:Publicacion), (p:Proyecto)
WHERE pub.idPub = 1 AND p.idPry = 2
CREATE (pub)<-[:sePublicaEn]-(p);

//*****Top 5*****
//Top 5 areas de conocimiento segun su cantidad de proyectos
MATCH (p:Proyecto)
WITH p.area_conocimiento AS area_conocimiento, COUNT(p) AS cantidad_proyectos
RETURN area_conocimiento, cantidad_proyectos
ORDER BY cantidad_proyectos DESC
LIMIT 5;


//Top 5 instituciones segun la cantidad de proyectos que hay
MATCH (i:Investigador)-[:participaEn]->(p:Proyecto)
WITH i.institucion AS institucion, COUNT(p) AS cantidad_proyectos
RETURN institucion, cantidad_proyectos
ORDER BY cantidad_proyectos DESC
LIMIT 5;

//Top 5 investigadores segun la cantidad de proyectos en la que trabajan
MATCH (i:Investigador)-[:participaEn]->(p:Proyecto)
WITH i, i.institucion AS institucion, COUNT(p) AS cantidad_proyectos
RETURN i.nombre_completo AS nombre_completo, institucion, cantidad_proyectos
ORDER BY cantidad_proyectos DESC
LIMIT 5;

//Busqueda de proyecto por titulo que devuelve toda su info y los investigadores que participan
MATCH (proyecto:Proyecto {titulo_proyecto: 'Investigación en Neurociencia'})
RETURN proyecto.anno_inicio AS anno_inicio,
       proyecto.duracion_meses AS duracion_meses,
       proyecto.area_conocimiento AS area_conocimiento,
       [(investigador)-[:participaEn]->(proyecto) | {
         nombre_completo: investigador.nombre_completo,
         titulo_academico: investigador.titulo_academico,
         institucion: investigador.institucion,
         email: investigador.email
       }] AS Investigadores,
       [(publicacion)-[:sePublicaEn]->(proyecto) | {
         titulo_publicacion: publicacion.titulo_publicacion,
         anno_publicacion: publicacion.anno_publicacion,
         nombre_revista: publicacion.nombre_revista
       }] AS Publicaciones


// Busqueda de publicacion por titulo 
MATCH (publicacion:Publicacion)
WHERE publicacion.titulo_publicacion =~ '(?i).*Titulo Publicacion*'  // (?i) para hacer coincidencia insensible a mayúsculas/minúsculas
OPTIONAL MATCH (publicacion)<-[:sePublicaEn]-(proyecto:Proyecto)
RETURN publicacion.anno_publicacion AS anno_publicacion,
       publicacion.nombre_revista AS nombre_revista,
       proyecto.titulo_proyecto AS titulo_proyecto;

// Busqueda area de conocimiento
MATCH (proyecto:Proyecto)
WHERE proyecto.area_conocimiento = 'Energías Renovables'
WITH proyecto
MATCH (publicacion:Publicacion)<-[:sePublicaEn]-(proyecto)
RETURN DISTINCT proyecto.area_conocimiento AS area_conocimiento,
       COLLECT(DISTINCT proyecto.titulo_proyecto) AS TItulos_de_Proyectos,
       COLLECT(DISTINCT publicacion.titulo_publicacion) AS Titulos_de_Publicaciones

//Busqueda de colegas de un investigador
MATCH (investigador:Investigador {nombre_completo: 'Carmen Fernandez'})
MATCH (investigador)-[:participaEn]->(proyecto:Proyecto)<-[:participaEn]-(colega:Investigador)
RETURN investigador.id AS id,
       investigador.nombre_completo AS nombre_completo,
       investigador.titulo_academico AS titulo_academico,
       investigador.institucion AS institucion,
       investigador.email AS email,
       COLLECT(DISTINCT colega.nombre_completo) AS colegas_de_proyectos


