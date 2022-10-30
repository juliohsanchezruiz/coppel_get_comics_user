# Api Get Comics User

# Python-Flask-MongoDB-with-Docker-Compose

Ejecute la instrucción Docker Compose para iniciar Api User (`Python`, `Flask` and `MongoDB`). 

```bash
docker-compose up -d
```

## Modificar credenciales para MongoDB Server

Actualice el archivo `.env` (variables de entorno) con sus credenciales específicas.

```bash
WEB_HOST=api_user

MONGO_HOST=user_mongodb
MONGO_PORT=27017
MONGO_USER=root-coppel
MONGO_PASS=password-coppel
MONGO_DB=db_coppel
```

## Otras instrucciones

#### Eliminar volúmenes
Tenemos dos formas de eliminar nuestros volúmenes con Docker.

Primero está usando el comando `prune`.

```bash
docker volume prune -f
```

El segundo es usar el comando actual `volume rm` con `-f` como parámetro.

```bash
docker volume rm $(docker volume ls -q)
```

#### Limpie el volumen de MongoDB y Cache para Python

```bash
rm -rf mongo-volume app/__pycache__/ && mkdir mongo-volume
```

#### Eliminar caché en el sistema Docker

```bash
docker system prune -a -f && docker builder prune -a -f
```

### Recrear  `web` de contenedor

```bash
docker-compose up --build --force-recreate --no-deps -d web
```

### Mostrar registros de ejecución de API

```bash
docker logs --tail 1000 -f api_register_comics
```
