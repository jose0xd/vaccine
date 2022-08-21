# Preuso
- Tener instaladas las bibliotecas externas de python en 'requirements.txt'
	+ Se puede crear un 'virtual enviroment' de python para instalar paquetes.
- Tener una web local donde probar. Se supone que usar herramientas como 'sqlmap' en sitios donde no tenemos permiso es ilegal.
	+ Se puede iniciar docker y ejecutar algunos de los contenedores del Makefile

# Uso
## Muestra la ayuda
> python vaccine.py -h

## Webs con inicio de sesión
Si haces un request a una web que supone un usuario activo, te redirige a la página de inicio de sesión. Para evitar esto se deben dar las cookies al programa.

### Ejemplo con cookies aleatorias (buscarlas en el navegador):
> python vaccine.py --cookie='PHPSESSID=0sf1qfnn1sk5j31cafqieqijk1&csrftoken=msRoWZqWaRTml90XDoyZT3TwhXtWBQzmRToRXDrkyzsJ3ozSDf6SYty9L0ND0NOS' --forms http://localhost/vulnerabilities/sqli

Se debe indicar el argumento --forms para que busque y rellene formularios con posibles vulnerabilidades. Si no se indica --forms se debe indicar --data y proporcionarle los campos a probar.

### Ejemplo con cookies y petición POST (la url es a la que te manda la web al rellenar un formulario o darle a 'submit')
> python vaccine.py --cookie='JSESSIONID=sM6-pWoqE0eR6B690WVrhuE5nO8tKpl55jvNhC-f' --data='login_count=3&userid=3' -X POST http://127.0.0.1:8080/WebGoat/SqlInjection/assignment5b

## Descargar la base de datos
El programa puede descargar la versión y los nombres de la base de datos, tablas y columnas de las dos webs con las que lo pruebo. No parece viable hacerlo genérico, 'sqlmap' no descarga nada.

En la primera de las webs puedo también descargar datos, en la otro dice que no tengo permisos.

> python vaccine.py --cookie='PHPSESSID=0sf1qfnn1sk5j31cafqieqijk1&csrftoken=msRoWZqWaRTml90XDoyZT3TwhXtWBQzmRToRXDrkyzsJ3ozSDf6SYty9L0ND0NOS' --forms --dump -o output http://localhost/vulnerabilities/sqli
