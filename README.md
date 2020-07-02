# My Blog, un pequeño proyecto con Flask.
Puede ir a: [Blog](https://blogjgtc.herokuapp.com/ "Link del proyecto")
***
- 1. Crear un nuevo directorio (folder).
- 2. Estando en el directorio creado, clonar el repositorio.
<br>
Ejem:
<br>
a. Crear un nuevo folder "blog_folder/"
<br>
b. En este folder "blog_folder/" , aqui clonar el repositorio

**Clonar el repisotorio**
```bash
> git clone https://github.com/josetanta/my_blog.git
> cd my_blog/
```
Hasta este momento la estructura del proyecto debera estar asi: <br>
<pre>
    |blog_folder/
    |    my_blog/
</pre>

## Getting Started

**Instalar un entorno virtual en el sistema**
<br>Se tiene dos formas de realizar esta acción.
- a. Instalar **virtualenv** esto es instalar de forma global.
```bash
> pip install virtualenv
```

Una vez instalado *virtualenv*, ejecutar en el directorio "blog_folder/"
```bash
> virtualenv mi_entorno
```
(1) Paso siguiente dirigirse  *mi_entorno/Scripts* para activar el entorno virtual.
```bash
> cd mi_entorno\Scripts
> activate.bat
```

(2) Para instalar todos los requerimientos debemos estar en el "blog_folder/my_blog/".
```bash
(mi_entorno) > pip install -r requirements.txt
```
De esta forma ya se instalo todos los requeremientos del Proyecto(o Blog :D)

- b.La segunda forma es:
```bash
> python -m venv mi_entorno
```
Repetir el paso (1) y (2)

Hasta este momento la estructura del proyecto debe estar así:
<pre>
    blog_folder/
    |   mi_entorno/
    |   my_blog/
    |   |   app/
    |   |   requeriments.txt
    |   |   ...

</pre>


### Para Arrancar con el Proyecto

- Opciones disponibles para los entornos son *production*, *development (o **default**)* y *test*<br>

Para esto dirigirse al directorio del proyecto *blog_folder/my_blog/* <br>

Para poder cambiar las variables de entorno. <br>
Debera de ejecutar en la terminal
```bash
>>> copy .env.example .env
```

<br>En el file creado **.env**, debera de completar las variables que esten ahi. <br>
Para poder generar el SECRET_KEY, solo debera de ejecutar en su terminal(o bash) este script.<br>
```bash
>>> python -c "import secrets; print(secrets.token_hex(15));"
```

```py
# Entorno de desarrollo
FLASK_ENV=development

# Entorno de producción
FLASK_ENV=production
```

En la terminal ejecutar el siguiente comando, esto para realizar la migraciones (Debe estar ubicado en "blog_folder/my_blog/")
- a. Si estas en modo **development** Ejecuta esto
```bash
// Paso 1
(mi_entorno) > python manage.py db init

// Paso 2
(mi_entorno) > python manage.py db migrate -m "Init migration"

// Paso 3
(mi_entorno) > python manage.py db upgrade
```
- b. Si vas ah cambiar a modo **production**
repite los pasos 2 y 3<br>

Nota: en el Paso 2  excluyes el *-m "Init migration"*.

Para arrancar con el servidor local solo ejecutar.
```bash
(mi_entorno) > python manage.py runserver
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
En tu navegador dirigirse a la url: "http://127.0.0.1:5000/"
