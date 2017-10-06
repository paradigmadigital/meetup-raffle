# Meetup raffle

Meetup raffle es una aplicación para rifas o sorteos basados en las listas de asistentes de los meetups. Accesible a través de http://rifa.paradigmadigital.com

## Fichero de asistentes
Está diseñado para ser compatible con los ficheros de asistentes generados por meetup.com, es decir, el fichero debe cumplir las siguientes condiciones:
* Debe estar en formato csv, aunque no es necesario que la extensión sea .csv ya que esto no se comprueba
* El separador entre columnas debe ser un tabulador (\t)
* La primera fila se ignora
* En la columna 1 se espera encontrar el nombre del asistente
* En la columna 3 se espera encontrar el "título" del asistente. En meetup.com esto significa que el miembro tiene algún cargo en la organización del meetup (organizador, coorganizador...) por lo tanto si esta columna no está vacia este asistente es ignorado en la rifa
* En la columna 9 se espera encontrar una url, a la que se enlazará al clickar en el nombre del ganador. En el fichero de meetup.com aquí encontramos la url al perfil del miembro en meetup.com

## Procedimiento de funcionamiento
1. Subir un fichero de asistentes que cumpla las condiciones al bucket de AWS S3 s3://meetup-raffle este bucket está gestionado a través de la cuenta de AWS de marketing de Paradigma. Para tener acceso y permisos para subir ficheros a este bucket se puede solicitar a sistemas
2. Una vez el fichero haya sido subido al bucket, automaticamente aparecerá en el listado de rifas disponibles en la aplicación (usando el mismo nombre del fichero) y podremos seleccionarlo para realizar una rifa basada en este fichero
3. Para coger aleatoriamente un ganador una vez hayamos seleccionado la rifa que queremos, solo es necesario clickar en el botón "get"

## Arquitectura y despliegues
Meetup raffle es una pequeña aplicacion desarrollada en Flask (un microframework web de Python) y desplegada en AWS Lambda (el servicio serverless de AWS) usando Zappa (una herramienta para despliegue de aplicaciones web sobre AWS Lambda y AWS API Gateway). Está desplegado en Irlanda (eu-west-1).

El código del proyecto está disponible en github https://github.com/paradigmadigital/meetup-raffle

Para desplegarlo es necesario tener instalado Python 2.7, un virtualenv con las dependencias instaladas, las credenciales de AWS configuradas y ejecutar el comando de despliegue de Zappa

### Crear el virtualenv

1. crear un nuevo virtualenv
`$ virtualenv raffle-venv`
2. activar el virtualenv
`$ source raffle-venv/bin/activate`
3. instalar las dependencias
`$ pip install -r meetup-raffle/flask/requirements.txt`

### Credenciales AWS 
Es necesario solicitar un access key y un secret key y configurarse un profile de aws llamado "marketing"

### Desplegar con zappa
Los settings que usa zappa para el despliegue están definidos en el fichero zappa_setting.json

Despliegue inicial (sólo es necesario hacerlo la primera vez)
`$ zappa deploy`

Actualizar el código
`$ zappa update`
