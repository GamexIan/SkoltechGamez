"""
SELECT a.folio, a.fecha, b.cantidad FROM ventas.cotizaciones AS a INNER JOIN ventas.cotizaciones_productos AS b USING(folio) WHERE b.noidentificacion = 'TEMFLEX1600' AND a.vigente AND a.fecha >= '2021-12-21' ORDER BY folio;
"""
import sys
import psycopg2
from datetime import datetime, date, timedelta

db = psycopg2.connect(database="chales", user="egamez")
curs1 = db.cursor()
curs2 = db.cursor()
curs3 = db.cursor()

noidentificacion = sys.argv[1]
periodo = None
if len(sys.argv) == 3:
    periodo = sys.argv[2]

folioi = 54670
inicio = datetime(2023, 1, 2, 9, 4, 43)
foliof  = 127059
final   = datetime(2024, 7, 31, 19, 0, 0)
if periodo == "B":
    folioi = 127064
    inicio = datetime(2024, 8, 1, 9, 9, 13)
    foliof  = 134409
    final   = datetime(2024, 9, 30, 18, 48, 53)


abre    = None
cierra  = None
gap     = None
mayoreo = False
minutos = None

# The output files
regs = open("ventas-" + noidentificacion + ".sql", "w")
regs.write("BEGIN;\n\n\n")
regs.write("COPY ventas (folio, fecha, noidentificacion, cantidad, " \
           "intervalo) FROM stdin;\n")

query = "SELECT a.folio, a.fecha, sum(b.cantidad) " \
        "FROM ventas.cotizaciones AS a " \
        "INNER JOIN ventas.cotizaciones_productos AS b USING(folio) " \
        "WHERE a.vigente AND NOT a.interno AND folio > %s " \
        "AND folio <= %s AND b.noidentificacion = %s " \
        "AND ((a.cliente IN (SELECT cliente FROM ventas.clientes " \
                            "WHERE tipo = %s)) " \
             "OR a.cliente IS NULL) GROUP BY a.folio, a.fecha ORDER BY a.folio"
params = (folioi, foliof, noidentificacion, 1)
curs1.execute(query, params)
for v in curs1:

    # Check whether this sale took place in 
    if inicio.day == v[1].day:
        # The sale took place on the same day; a simple `timedelta`..
        gap = v[1] - inicio

    else:
        # For a one-day sale, we need to calculate the difference. 
        #We need to fill in the gap from the start date to the current date. 
        #Check and obtain the sales data for the days in between.


        # Initialize the value
        gap = inicio - inicio

        # Get the date of the last previous transaction
        query = "SELECT fecha AS venta " \
                "FROM ventas.cotizaciones WHERE vigente " \
                "AND NOT interno AND fecha < %s " \
                "ORDER BY venta DESC LIMIT %s"
        params = (datetime(inicio.year,inicio.month,inicio.day, 22, 0, 0), 1)
        curs2.execute(query, params)
        ultima = curs2.fetchone()[0]
        # Calculate the difference until closing time; 
        #it's possible that you worked half a day.
        if ultima.hour > 17 and ultima.hour < 19:
            # It's no longer for sale; pick up the difference by 7 p.m.
            ultima = datetime(inicio.year, inicio.month, inicio.day, 19, 0, 0)

        # Add the gap
        gap += ultima - inicio


        inicio = datetime(ultima.year, ultima.month, ultima.day, 1, 0, 0) \
                 + timedelta(1)

        # Now we're going to loop until 
        #we reach the day specified by v[1] and keep adding
        while inicio.day != v[1].day:

            # We must select the first sale
            query = "SELECT fecha FROM ventas.cotizaciones WHERE vigente " \
                    "AND NOT interno AND fecha >= %s ORDER BY folio " \
                    "LIMIT %s"
            params = (inicio, 1)
            curs2.execute(query, params)
            inicio = curs2.fetchone()[0]
            # Check to see if the first sale took place before 9 a.m.
            abre = datetime(inicio.year, inicio.month, inicio.day, 9, 0, 0)
            if abre < inicio:
                # Set the time to the time of entry
                inicio = abre

            
            if inicio.day == v[1].day:
                
                break

            # Now the close
            query = "SELECT fecha FROM ventas.cotizaciones WHERE vigente " \
                    "AND NOT interno AND fecha <%s ORDER BY folio DESC LIMIT %s"
            abre = datetime(inicio.year, inicio.month, inicio.day, 1, 0, 0) \
                   + timedelta(1)
            params = (abre, 1)
            curs2.execute(query, params)
            ultima = curs2.fetchone()[0]
            # The lats sale
            if ultima.hour > 17 and ultima.hour < 19:
                # It's no longer for sale; pick up the difference by 7 p.m.
                ultima = datetime(inicio.year,inicio.month,inicio.day,19, 0, 0)

            # Add a gap
            gap += ultima - inicio

            # Update
            inicio = datetime(inicio.year, inicio.month, inicio.day, 1, 0, 0) \
                     + timedelta(1)

        # It's already the same day; the workday is beginning.
        # We need to select the first sale.
        query = "SELECT fecha FROM ventas.cotizaciones WHERE vigente " \
                "AND NOT interno AND fecha >= %s ORDER BY folio " \
                "LIMIT %s"
        params = (inicio, 1)
        curs2.execute(query, params)
        inicio = curs2.fetchone()[0]
       
        abre = datetime(inicio.year, inicio.month, inicio.day, 9, 0, 0)
        if abre < inicio:
            
            inicio = abre

        # Add a gap
        gap += v[1] - inicio

    # Calculate the gap in minutes
    minutos = gap.total_seconds()/60

    # Update the data at the begining
    inicio = v[1]

    # The Record Counter
    regs.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(v[0], v[1],
                                      noidentificacion, v[2], round(minutos,2)))
    regs.flush()


regs.write("\\.\n\nCOMMIT;\n")
regs.close()

curs3.close()
curs2.close()
curs1.close()
db.close()
