-- Query 1: Precio del nodo 01ANS-85 en MDA y MTR, ordenado por nodo (asc), fecha (desc), y hora (asc)
SELECT mda.claNodo, mda.fecha, mda.hora, mda.pml AS pml_mda, mtr.pml AS pml_mtr
FROM MemTraMDADet mda
JOIN MemTraMTRDet mtr ON mda.claNodo = mtr.claNodo AND mda.fecha = mtr.fecha AND mda.hora = mtr.hora
WHERE mda.claNodo = '01ANS-85'
ORDER BY mda.claNodo ASC, mda.fecha DESC, mda.hora ASC;

-- Query 2: Precio promedio por nodo en MTR y MDA, y diferencia de estos dos precios promedio, ordenado por diferencia descendente
SELECT mda.claNodo, 
       AVG(mda.pml) AS avg_pml_mda, 
       AVG(mtr.pml) AS avg_pml_mtr, 
       ABS(AVG(mda.pml) - AVG(mtr.pml)) AS diff_pml
FROM MemTraMDADet mda
JOIN MemTraMTRDet mtr ON mda.claNodo = mtr.claNodo AND mda.fecha = mtr.fecha AND mda.hora = mtr.hora
GROUP BY mda.claNodo
ORDER BY diff_pml DESC;

-- Query 3: Precio de nodo en dólares tomando el tipo de cambio de MemTraTcDet
SELECT mda.claNodo, mda.fecha, mda.hora, mda.pml, mda.pml / tc.valor AS pml_usd
FROM MemTraMDADet mda
JOIN MemTraTcDet tc ON mda.fecha = tc.fecha
ORDER BY mda.claNodo, mda.fecha, mda.hora;

-- Query 4: Listado de nodos con precios en MDA y MTR, tipo de cambio y precio de la tbfin
SELECT mda.claNodo, mda.fecha, mda.hora, mda.pml AS pml_mda, mtr.pml AS pml_mtr, tc.valor AS tipo_cambio, tb.TbFin
FROM MemTraMDADet mda
JOIN MemTraMTRDet mtr ON mda.claNodo = mtr.claNodo AND mda.fecha = mtr.fecha AND mda.hora = mtr.hora
JOIN MemTraTcDet tc ON mda.fecha = tc.fecha
JOIN MemTraTBFin tb ON mda.fecha = tb.fecha
ORDER BY mda.claNodo, mda.fecha, mda.hora;
