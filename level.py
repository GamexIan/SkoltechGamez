"""
THIS SCRIPT DOES NOT TAKE INTO ACCOUNT UNITS SOLD WHOLESALE

Script to generate files with the data needed to populate the inventory level table
with the inventory level
"""
import sys
from datetime import date
import psycopg2

"""
TEMFLEX1600	MQJq
100-6211W	jl09
5320-WCI	X9XJ
SPM-12		4J82
OC12		rxAY
"""

noidentificacion = sys.argv[1]
periodo = None
if len(sys.argv) == 3:
    periodo = sys.argv[2]

dbc = psycopg2.connect(database="chales", user="egamez")
dbp = None
if periodo == "B":
    dbp = psycopg2.connect(database="chales", user="egamez")
else:
    dbp = psycopg2.connect(database="chales", user="egamez")
cursc = dbc.cursor()
cursp1 = dbp.cursor()
cursp2 = dbp.cursor()

# Year 2023
niveles = {
  "100-6211W":   22,
  "TEMFLEX1600":  76,
  "5320-WCI": 4,
  "SPM-12": 216,
  "OC12": 1135,
}

folioi = 54670
inicio = date(2023, 1, 1)
final  = date(2024, 8, 1)
if periodo == "B":
    folioi = 127064
    inicio = date(2024, 8, 1)
    final  = date(2024, 10, 1)
    niveles = {
      "100-6211W":   169,
      "TEMFLEX1600":  76,
      "5320-WCI": 93,
      "SPM-12": 294,
      "OC12": 938,
    }



query = "SELECT DISTINCT fecha::date AS dia FROM ventas.cotizaciones " \
        "WHERE vigente AND NOT interno AND folio >= %s " \
        "AND fecha < %s ORDER BY dia"
params = (folioi, final)
cursc.execute(query, params)
for d in cursc:
    query = "INSERT INTO nivel (dia, noidentificacion) VALUES(%s, %s)"
    params = (d[0], noidentificacion)
    cursp1.execute(query, params)
dbp.commit()

# Enter all sales made on that day. Sales include both wholesale and retail.
query = "SELECT sum(b.cantidad), a.fecha::date AS dia " \
        "FROM ventas.cotizaciones AS a " \
        "INNER JOIN ventas.cotizaciones_productos AS b USING(folio) " \
        "WHERE a.vigente AND NOT a.interno AND folio >= %s " \
        "AND fecha <= %s AND b.noidentificacion = %s GROUP BY dia"
params = (folioi, final, noidentificacion)
if periodo == "B":
    query = "SELECT sum(b.cantidad), a.fecha::date AS dia " \
            "FROM ventas.cotizaciones AS a " \
            "INNER JOIN ventas.cotizaciones_productos AS b USING(folio) " \
            "WHERE a.vigente AND NOT a.interno AND folio >= %s " \
            "AND fecha <= %s AND b.noidentificacion = %s " \
            "AND ((a.cliente IN (SELECT clave FROM ventas.clientes " \
                            "WHERE tipo = %s)) " \
                 "OR a.cliente IS NULL) GROUP BY dia"
    params = (folioi, final, noidentificacion, 1)

cursc.execute(query, params)
for v in cursc:
    query = "UPDATE nivel SET ventas = %s WHERE dia = %s " \
            "AND noidentificacion = %s"
    params = (v[0], v[1], noidentificacion)
    cursp1.execute(query, params)
dbp.commit()


cursc.close()
dbc.close()



query = "SELECT sum(cantidad), fecha::date AS dia FROM compras " \
        "WHERE noidentificacion = %s GROUP BY dia"
params = (noidentificacion, )
cursp1.execute(query, params)
for c in cursp1:
    query = "UPDATE nivel SET compras = %s WHERE dia = %s " \
            "AND noidentificacion = %s"
    params = (c[0], c[1], noidentificacion)
    cursp2.execute(query, params)
dbp.commit()


nivel = niveles[noidentificacion]
query = "SELECT numero, ventas, compras FROM nivel " \
        "WHERE noidentificacion = %s ORDER BY numero"
params = (noidentificacion, )
cursp1.execute(query, params)
for r in cursp1:
    nivel += r[2] - r[1] 
    query = "UPDATE nivel SET nivel = %s WHERE numero = %s"
    params = (nivel, r[0])
    cursp2.execute(query, params)
dbp.commit()

cursp2.close()
cursp1.close()
dbp.close()
