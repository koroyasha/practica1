Instrucciones para instalar y ejecutar el sistema en Django

Este documento describe los pasos necesarios para descargar, instalar y ejecutar el sistema desarrollado en Django, el cual permite subir un archivo de texto y generar un histograma de palabras en forma de tabla.

1. Requisitos previos

Antes de comenzar, asegúrese de contar con lo siguiente instalado en su computadora:

Python 3.10 o superior → https://www.python.org/downloads/

Git (para clonar el repositorio) → https://git-scm.com/downloads

pipenv (para gestionar el entorno virtual).
Puede instalarlo con el siguiente comando:

pip install pipenv

2. Descargar el proyecto

Abra una terminal o consola de comandos.

Clone el repositorio desde GitHub usando el enlace proporcionado:

git clone https://github.com/tu-usuario/tu-proyecto.git


Ingrese al directorio del proyecto:

cd tu-proyecto

3. Archivos importantes para la instalación

El proyecto incluye dos archivos clave para que funcione correctamente:

Pipfile → Contiene la lista de dependencias necesarias para ejecutar el proyecto.

Pipfile.lock → Contiene las versiones exactas de las dependencias para garantizar que todos los usuarios usen la misma configuración.

⚠️ Importante:
No borre, edite ni mueva estos archivos, ya que pipenv los utiliza para instalar automáticamente todo lo necesario.

4. Crear y activar el entorno virtual

El proyecto utiliza pipenv para gestionar dependencias:

Cree el entorno virtual e instale automáticamente las dependencias:

pipenv install


Este comando lee los archivos Pipfile y Pipfile.lock para instalar exactamente las librerías necesarias.

Active el entorno virtual:

pipenv shell

5. Configurar el entorno de Django
5.1. Configuración de idioma y zona horaria

El sistema está configurado para trabajar en español.
Si desea modificar esta configuración, puede editar el archivo:

proyecto/settings.py


Y verificar que las siguientes líneas existan:

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

6. Preparar la base de datos

Ejecute los siguientes comandos para crear la base de datos local necesaria para Django:

python manage.py makemigrations
python manage.py migrate

7. Crear un superusuario para el panel de administración

El sistema habilita el panel de administración de Django. Para ingresar, necesita un usuario administrador:

python manage.py createsuperuser


Siga las instrucciones en pantalla para ingresar nombre de usuario, correo y contraseña.

8. Ejecutar el servidor

Inicie el servidor local con el siguiente comando:

python manage.py runserver


Una vez iniciado, abra su navegador y acceda a:
http://127.0.0.1:8000

9. Uso del sistema
9.1. Subir un archivo

En la página principal, encontrará un formulario para subir un archivo de texto (.txt).

Seleccione el archivo desde su computadora y presione Subir.

9.2. Generar el histograma

Una vez que el archivo esté cargado, presione el botón "Generar histograma".

El sistema analizará el texto y mostrará en una tabla la frecuencia de cada palabra encontrada.

10. Acceso al panel de administración

Para acceder al panel de administración de Django:

10. Detener el servidor

Para detener el servidor, presione las teclas:

CTRL + C


Y para salir del entorno virtual:

exit
