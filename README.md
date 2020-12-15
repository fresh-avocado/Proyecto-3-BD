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

| N | KNN-RTree (ms) | KNN-Secuencial (ms)
|:---:|:---:|:---:|
| 100 | 59 | 10,409 |
| 200 | 60 | 21,227 |
| 400 | 63 | 44,153 |
| 800 | 68 | 84,604 |
| 1600 | 70 | 170,335 |
| 3200 | 82 | 342,199 |
| 6400 | 105 | 681,175 |
| 12800+ | 176 | 1,553,040 |

### Análisis

Los resultados fueron los esperados. El KNN-secuencial se demora mucho más que el KNN con el RTree. Dándole una primera mirada a los resultados, uno podría ver que el tiempo del secuencial crece linealmente mientras que el tiempo del RTree crece de manera logarítmica. Podría surgir la pregunta, ¿por qué el KNN secuencial se demora tanto, si su complejidad es polinomial (**O**(n lg n) ) comparado con la complejidad logarítmica del RTree (**O**(lg n) base M)? La respuesta tiene que ver con el número de accesos a disco del KNN-secuencial. El KNN-secuencial, lee toda la colección de disco para hallar los K más cercanos al query, lo cual hace que el algoritmo sea bien lento, ya que los accesos a disco son lineales y acceder a disco es muy costoso. Por otro lado, el RTree solo hace un número logarítmico de accesos a disco, lo cual lo hace mucho más rápido que el algoritmo secuencial.

### Discusión

Los algoritmos de recuperación KNN son muy usados en este tipo de aplicaciones, pero también existen otros como los algoritmos de búsqueda por rango. En este caso, nosotros implementamos, por mero tema de experimentación, un algoritmo de búsqueda por rango (recibe un radio **r** en vez de un **k**), aunque al final no experimentamos mucho con él. Este procedimiento se hizo basándonos en las funciones implementadas de la librería Rtree. El problema de este algoritmo para este tipo de programas, es que el rango no tiene una unidad definida, entonces es un poco arbitrario asignar un rango ‘r’ para la búsqueda, ya que nos podría retornar muy pocos o muchos resultados. En otras palabras, no tenemos mucho control sobre el número de datos que serán retornados, por lo que no termina siendo práctico para estos propósitos.

Sería interesante comparar la performance de la búsqueda KNN entre el Rtree que usamos (en disco) y uno que esté cargado en RAM. Por obvias razones, los tests que corrimos tuvieron que hacerse con la primera opción, pues era simplemente inviable cargar datos de casi 13000 imágenes para ser procesadas en ram dentro de la estructura del Rtree. Para temas de búsquedas de usuarios, en realidad no importa mucho porque el tiempo que nos da el Rtree en disco es despreciable para la percepción humana, pero si hablamos de búsquedas masivas para investigación o industria, ahí sí nos interesa la velocidad y quizás sería más interesante hacerlo todo en RAM, por supuesto, si contamos con una cantidad significativa de RAM.

Un área de aplicación del KNN es *machine learning*. Se usa el algoritmo KNN para clasificar, un nuevo elemento. Por ejemplo, si tenemos una base de datos de imágenes de frutas y queremos insertar una manzana, hacemos la búsqueda KNN de esa manzana y dependiendo de la clasificación de la mayoría de sus K más cercanos, se le asigna esa misma clasificación. En finanzas, también se usa para predecir la calificación crediticia de un cliente para un banco, de tal manera que el banco pueda medir el posible riesgo asociado a prestarle dinero a ese cliente. También se usa para predecir el candidato por el que un ciudadano podría votar. En conclusión, el KNN es un algoritmo simple que tiene bastantes aplicaciones muy interesantes en distintos ámbitos y su aplicación eficiente se puede dar, en base a los experimentos hechos en este proyecto, usando una estructura de datos como el RTree.

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
