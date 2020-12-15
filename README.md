# Proyecto 3: Base de Datos 2

## Integrantes
* Rodrigo Céspedes
* Benjamín Díaz
* Gabriel Spranger

# Informe Proyecto 2 

Vér la sección **Instrucciones** (más abajo) para ver cómo poder correr esta aplicación en su computadora.

# Objetivos del proyecto

Este proyecto se basa en crear una aplicación web para reconocimiento facial. Lo que se quiere lograr es que la aplicación, al pasarle una base de datos de fotografías .jpg, pueda indexarlas de manera tal, que al proveer una imagen, te pueda devolver las k fotos que más se parecen. Esto claramente se tiene que hacer en el backend y se realizará a través de un programa en python.

## Sistema de reconocimiento facial

Para este experimento, se está utilizando la librería face_recognition de python para obtener el vector característico de cada imagen. La librería ya cuenta con funciones que decodifican la imagen y la procesan de manera tal, que el vector resultante, es representativo para las características faciales de la persona en la imagen.

Esto implica que, la distancia entre dos vectores significa directamente ‘que tanto se parecen’ las dos personas en las fotos representadas por esos vectores. Para calcular la distancia, se utiliza una función que la librería incluye.

## Indexación

La etapa 1 de este programa consta en procesar las imágenes de la base de datos y obtener sus vectores característicos. Luego, llega la parte de la indexación. 

Para este proceso, se utiliza la librería de python Rtree, esta librería implementa dicha estructura y provee funciones útiles para utilizarla. Cada vector característico consta de 128 elementos, por lo que en el Rtree, se deberán insertar puntos 128-dimensionales. 

Este tipo de Rtrees nos piden insertar lo que llamaremos un ‘área de influencia’, que no es más que un área k-dimensional que está delimitada por dos puntos k-dimensionales (esquinas opuestas), suponemos que para aplicaciones más complejas, es una función más útil que insertar un simple punto k-dimensional.

Para nuestra aplicación, lo que hicimos fue que esos dos puntos sean el mismo, en ese caso, no sería un área, sino un simple punto 128-dimensional. De esa manera se insertan todas las imágenes en el índice. Este índice se guarda en disco para no saturar la RAM y cada vez que se vaya a hacer una consulta, se realiza a través de dichos archivos. La librería provee funciones que facilitan ese proceso.


## KNN


El principal algoritmo de búsqueda que estamos usando es de los ‘K-nearest neighbors’. Lo implementamos de dos maneras: secuencial y con el RTree.

### Secuencial

Para implementar el KNN de manera secuencial, usamos un **max-heap**. Iteramos sobre todo el set de imágenes. Primero, insertamos las K primeras de frente. Luego, chequeamos que la distancia entre la imagen que estamos analizando sea menor al **top del heap**. Si es así, entonces significa que tenemos una imagen que tiene más similitud, por lo tanto tenemos que eliminar el top del heap con **heappop** e insertar el nuevo elemento con **heappush**. Esto se hace ya que como es un max-heap, el heap tendrá las distancias de los K más cercanos hasta ahora y el top del heap tendrá la mayor distancia de estas K distancias. Por lo tanto, basta comparar la nueva distancia con el top del heap, y si es menor, entonces borramos el top del heap e insertamos la nueva distancia en el heap, ya que tenemos una distancia que es menor a la mayor distancia de los K más cercanos (top del heap) hasta ahora.

### RTree

Para la implementación KNN con Rtree, se utilizó la librería ya mencionada anteriormente. Primero se carga en memoria la imagen con el nombre pasado en el query, se saca su respectivo vector característico se utiliza una función implementada de la misma librería para buscar los vecinos más cercanos. Para esto es importante notar que el índice está guardado en disco y se accede cuando se hace la búsqueda, esto es para optimizar el espacio utilizado en ram. Luego simplemente se hace el match de los resultados obtenidos, con sus nombres correspondientes.

## Experimentación

| Tiempo (ms) | KNN-RTree | KNN-Secuencial
|:---:|:---:|:---:|
| N = 100 | 59 | 10,409 |
| N = 200 | 60 | 21,227 |
| N = 400 | 63 | 44,153 |
| N = 800 | 68 | 84,604 |
| N = 1600 | 70 | 170,335 |
| N = 3200 | 82 | 342,199 |
| N = 6400 | 105 | 681,175 |
| N = 12800+ | 176 | 1,553,040 |

### Análisis

TODO

### Discusión

TODO

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
