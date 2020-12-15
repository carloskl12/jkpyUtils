# jkpyUtils
Utilidades varias de python que utilizan librerías estandar y así evitar tener complejas dependencias para poder utilizarlas.

### Contenido
**[Requisitos](#requisitos)**<br>
**[Modo de uso](#modo-de-uso)**<br>
**[Licencia](#licencia)**<br>

## Requisitos
El paquete es desarrollado en python 3 y probado sobre Linux, utiliza librerías 
estandar de python.

## Modo de uso
Para utilizar el paquete se puede utilizar en modo desarrollo o instalarlo
directamente como un paquete. El modo desarrollo es útil si se quieren hacer 
algunos ajustes particulares en el paquete, en dicho caso hay que descargar 
y descomprimir el paquete en el directorio que se quiera trabajar y ejecutar
este modo de instalación mediante el script setup.py:

			$ python setup.py develop

Para desinstalarlo:
			$ python setup.py develop --uninstall

Finalmente si se quiere instalarlo como una librería que no se quiere modificar

			$ python setup.py install


## Licencia
[GNU GENERAL PUBLIC LICENSE](LICENCE)
