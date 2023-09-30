MATCH (p:Publicacion {idPub: 1}) // Modificar publicaciones por idPub
SET p.titulo_publicacion = 'Nuevo Título',
    p.anno_publicacion = 2023,
    p.nombre_revista = 'Nueva Revista';

MATCH (p:Publicacion {idPub: 1}) // Buscar publicaciones por idPub (Revisar que existe)
RETURN p; 