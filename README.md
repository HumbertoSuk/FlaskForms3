# Flask practica 3

## Modelo ModelUsers.py

En el contexto del desarrollo web, la gestión de sesiones es fundamental para mantener información persistente del usuario a lo largo de su interacción con un sitio. El modelo ModelUsers.py aborda esta funcionalidad en el marco de una aplicación web.

## Sesiones en Desarrollo Web

- **Identificación del Usuario**: Las sesiones permiten asignar un identificador único, conocido como "ID de sesión", que se almacena en una cookie en el navegador del usuario.

- **Almacenamiento de Datos**: Información relevante sobre el usuario, como preferencias y estado de inicio de sesión, se guarda en el servidor en relación con la sesión del usuario, asegurando su disponibilidad a lo largo de la visita del usuario al sitio.

- **Persistencia** : A diferencia de las cookies, las sesiones suelen tener una duración más extensa, pudiendo durar hasta que el usuario cierre el navegador o expire la sesión debido a la inactividad.

- **Estado del Usuario**: Las sesiones permiten que un sitio web recuerde el estado del usuario, por ejemplo, manteniendo la información de inicio de sesión para evitar que el usuario tenga que iniciar sesión en cada página.

- ## Implementación en ModelUsers.py

- 
Modelo ModelUsers.py
En el contexto del desarrollo web, la gestión de sesiones es fundamental para mantener información persistente del usuario a lo largo de su interacción con un sitio. El modelo ModelUsers.py aborda esta funcionalidad en el marco de una aplicación web.

Sesiones en Desarrollo Web
Las sesiones desempeñan un papel crucial en el desarrollo web, brindando los siguientes beneficios:

Identificación del Usuario: Las sesiones permiten asignar un identificador único, conocido como "ID de sesión", que se almacena en una cookie en el navegador del usuario.

Almacenamiento de Datos: Información relevante sobre el usuario, como preferencias y estado de inicio de sesión, se guarda en el servidor en relación con la sesión del usuario, asegurando su disponibilidad a lo largo de la visita del usuario al sitio.

Persistencia: A diferencia de las cookies, las sesiones suelen tener una duración más extensa, pudiendo durar hasta que el usuario cierre el navegador o expire la sesión debido a la inactividad.

Estado del Usuario: Las sesiones permiten que un sitio web recuerde el estado del usuario, por ejemplo, manteniendo la información de inicio de sesión para evitar que el usuario tenga que iniciar sesión en cada página.

## Implementación en ModelUsers.py

El archivo ModelUsers.py presenta métodos para gestionar sesiones en el contexto de una aplicación web. Algunas funciones clave incluyen:

**get_by_id**: Recupera información del usuario a partir de su identificador.

**login**: Maneja la autenticación del usuario, estableciendo la sesión en función de las credenciales proporcionadas.

## LoginManager

En el archivo app.py, se establece una instancia de LoginManager asociada a la aplicación Flask.
Esta instancia es crucial para configurar la autenticación y gestionar las sesiones de usuario en la aplicación.

### Ruta de Login:

Esto asegura que se inicie la sesión para el usuario autenticado.

``` python
if logged_user != None:
    login_user(logged_user)
```

### User Loader

Se implementa un user_loader para cargar los datos del usuario que ha iniciado sesión. En app.py, se crea el método load_user(id):
``` python
@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

```
Este método utiliza la conexión a la base de datos (db) para cargar los datos del usuario a partir de su identificador.

### Metodo get_by_id

En el modelo ModelUsers.py, se define el método get_by_id que retorna los datos del usuario a partir de su ID. En caso de no existir, retorna None:

``` python
@classmethod
def get_by_id(cls, db, id):
    try:
        cursor = db.connection.cursor()
        cursor.execute(
            "SELECT id, username, usertype, fullname FROM user WHERE id = %s", (id,)
        )
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], None, row[2], row[3])
        else:
            return None
    except Exception as ex:
        raise Exception(ex)

```

### Atributo is_active

Para gestionar el control de la sesión, se agrega el atributo is_active a la clase User. Se logra haciendo que la clase User herede de la clase UserMixin del paquete flask_login

Por ultimo añadimos a cada pagina el codigo: `<h1>{{ current_user.fullname }}</h1>`

## Logout

Para implementar el logout en Flask, se crea la ruta /logout en app.py. Dentro de esta ruta, se utiliza logout_user() para cerrar la sesión y luego se redirige a /login:
``` python 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

```

**Agregar el boton**:

`<a class="btn btn-danger" href="{{ url_for('logout') }}" >LogOut</a>`

Al realizar el logout, si se intenta acceder directamente a las plantillas home o admin, por ejemplo, mediante http://127.0.0.1:5000/home, se permitirá el acceso, pero no se mostrará el nombre del usuario, ya que no hay ninguna sesión activa.

### Bloquear accesos

Para restringir el acceso a ciertas páginas a usuarios autenticados, se utiliza el decorador @login_required. Se agrega este decorador a las rutas, como se muestra en el ejemplo de la ruta /home:

``` python 

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

```

### Bloquear paginas a usuarios administradores

Se implementa un decorador personalizado llamado admin_required para bloquear el acceso a páginas que solo deben ser accedidas por administradores. Este decorador verifica si el usuario está autenticado y si su tipo de usuario (usertype) es igual a 1 (administrador). En caso contrario, devuelve un error 403 usando la función abort().

``` python

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)  # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view


```


Se implementa el metodo:

``` python
@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("admin.html")

```

### Conclusion 


En resumen, la implementación de gestión de sesiones y control de acceso en una aplicación Flask sigue un enfoque estructurado y escalonado. Se inicia con la creación de una instancia de LoginManager para administrar la autenticación y las sesiones de usuario. Luego, se establece la funcionalidad de logout, asegurando que la sesión se cierre correctamente y redirigiendo al usuario según sea necesario.

El uso del decorador @login_required permite restringir el acceso a determinadas rutas solo a usuarios autenticados, proporcionando una capa adicional de seguridad. Además, se implementa un decorador personalizado, admin_required, para asegurar que ciertas rutas solo sean accesibles por usuarios administradores.

La estructura de la aplicación incluye la definición de modelos de usuario y métodos asociados, así como la integración de plantillas que reconocen la información del usuario utilizando Jinja2.
