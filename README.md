# Proyecto 3: Base de Datos 2

## Integrantes
* Rodrigo Céspedes
* Benjamín Díaz
* Gabriel Spranger

# Instrucciones

## Front
* Entrar al carpeta **/frontend**
* `npm install`
* Entrar a la carpeta `src`
* `npm run serve`

### Backend
* Entrar a la carpeta **backend**
* `python3 -m venv env`
  * En caso de error, correr `apt-get install python3-venv` y luego `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
* `python3 app.py`

### IMPORTANTE
Las fotos utilizadas deben ser unicamente jpg, aqui hay una gran base de datos provista por el profesor http://vis-www.cs.umass.edu/lfw/

### Instrucciones de uso:
Para que funcione bien, primero tienes que hacer ls *.jpg > names.txt,
esto hara que todos los nombres de tus fotos jpg de tu directorio actual se guarden
en un archivo. Para esto estoy tomando en cuenta que todos los archivos incluyendo el .py
y las fotos estan guardados en el mismo directorio

De ahi, tendras que correr la funcion crear_insertar() una UNICA vez. Eso creara
el indice y lo guardara en disco.

De ahi en adelante, usa las busquedas range_q('nombre.jpg', rango), el rango funciona del 1 al 100, pero 
como no es preciso, es preferible empezar de a poco. knn_h('nombre.jpg',k) es un knn secuencial con heap
y luego el knn('nombre.jpg', k) que es un knn pero con el rtree generado al principio. Esas funciones
deberian devolverte una lista de los nombres de los archivos seleccionados.

He hecho un requirements.txt, creo que solo funciona con linux. En cualquier caso, aqui dejo las libreiras que he usado

### Instalacion Mac (no estoy seguro de que funcione, pero eso deberia funcionar)

(face_recognition, si te pide agregar al PATH, hazlo)

brew install cmake

pip3 install face_recognition

(Rtree)

brew install spatialindex

pip install Rtree
