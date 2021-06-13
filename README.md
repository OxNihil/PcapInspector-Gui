Análisis de paquetería:
----------------

Integrantes Grupo:
------------------

Iago Pallares Tato <iago.pallares@udc.es>
Marcos Vázquez Campos <marcos.vazquez3@udc.es>
Daniel Osama González Anwar <daniel.osama.gonzalez@udc.es> 

Cómo ejecutar:
--------------

El contenedor se instala e inicia solo de forma totalmente automatizada con el comando:

./setup.sh


Problemas conocidos:
--------------------

Desde el contenedor de docker algunas funcionalidades no terminan de funcionar por completo, en concreto Maps y Upload (al subir un archivo y procesarlo), no obstante, estas sí funcionan plenamente si ejecutamos el servidor a partir de "python3 manage.py runserver".

Cambios respecto a la documentación previa:
-------------------------------------------

Se han omitido algunas funcionalidades al observar que su implementación no era del todo factible con la idea general que teníamos previamente, por lo tanto, ahora las funcionalidades principales son:

1) HOME: Filtrado de paquetes por todo tipo de campos (tanto por toggle para los protocoles como introduciendo por teclado para las IPs, MACs, etc.)

2) PCAPLIST: Listado de los ficheros .pcap que se han subido con la función de upload.

3) UPLOAD: Subir un fichero .pcap que será procesado por las demás funciones.

4) MAP: Geolocalización de las IPs que aparecen en el .pcap a partir de un mapa del mundo.

5) STATS: Estadísticas de aparación de determinados paquetes e IPs en el fichero .pcap.

6) LOGIN/LOGOUT y REGISTER

En la documentación previa se mencionaba el uso de javascript para generar grafos, esta implementación se ha sustituido por otra más realista, todo el filtrado de paquetes se realiza con el apoyo de este lenguaje.

