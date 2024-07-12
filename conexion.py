import mariadb


try:

    conex = mariadb.connect(host="localhost", port= 3307, username= "root", password="mauro17", database="prueba")

    print(conex)
    print("Conexion EXITOSA")
    cur = conex.cursor()
    cur.execute("SELECT * FROM prueba.muestra")
    datos = cur.fetchall()
    print(datos)

   

except NameError as e:
    print ("Error de conexion, ", e)




