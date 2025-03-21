# SGI - Sistema de Gestión de Inventario

SGI es una API Rest desarrollada para gestionar el inventario de una cadena de tiendas minoristas, proporcionando control sobre productos, stock y transferencias entre sucursales.

### Requerimientos

1. Docker
2. Python (Dev)
3. Pipenv (Dev)
4. PostgreSQL (libpq-dev) (Dev)

### Instalacion (Local)

1. Crear un archivo .env con las variables necesarias en la carpeta raiz.

```sh
# configurable
POSTGRES_DB=inventory_management
POSTGRES_USER=usr
POSTGRES_PASSWORD=pword
POSTGRES_ROOT_PASSWORD=root
POSTGRES_PORT=5432
API_GATEWAY_PORT=80

# no configurable
APP_POSTGRES_HOST=postgresql
APP_HOST=0.0.0.0
APP_PORT_1=5001
APP_MODULES_1=[products]
APP_PORT_2=5002
APP_MODULES_2=[inventory]
APP_PORT_3=5003
APP_MODULES_3=[stores]
```

2. Construir la imagen Docker:

```
docker build -t sgi-flask app
```

3. Levantar los servicios con Docker Compose:

```
docker-compose up -d
```

#### Ejecutar testing

1. Crear un archivo .env con las variables necesarias.
2. Inicializar instancia de base de datos

```
pipenv run setup-db
```

3. Mover a carpeta de app e instalar dependencias

```
cd app && pipenv install
```

4. Ejecutar los test

```
pipenv run tests
```

### Despliegue AWS

1. Configurar la base de datos Aurora:

    - Crear una instancia de Amazon Aurora con PostgreSQL.
    - Configurar los parámetros de conexión, grupos de seguridad y actualizar .env con el endpoint de la base de datos.

2. Crear los grupos de autoescalado:

    - Crear una plantilla de lanzamiento que contenga la configuración de la instancia EC2 (tipo de instancia, AMI, roles IAM necesarios, y claves de acceso).
    - Configurar los grupos de autoescalado para que gestionen las instancias de la API, definiendo políticas de escalado según la carga del sistema.

3. Configurar el API Gateway:

    - Crear un nuevo API Gateway y definir los endpoints necesarios.
    - Configurar las integraciones con los grupos de autoescalado y la base de datos Aurora.

4. Desplegar la aplicación:

    - Construir y subir la imagen Docker a Amazon Elastic Container Registry (ECR).
    - Crear las tareas en Amazon ECS para ejecutar los contenedores.

5. Monitoreo y mantenimiento:
    - Establecer alarmas y notificaciones para eventos de autoescalado.

### Documentación

-   [Documentación](./deliverables/Documentation.yaml)
-   [Documentación (Resolved)](./deliverables/Documentation_resolved.yaml)
-   [Postman](./deliverables/SGI.postman_collection.json)

#### Modelos de Base de datos

```json
class Product {
	"id": "string",
	"name": "string",
	"description": "string",
	"category": "string",
	"price": "decimal",
	"sku": "string"
}
```

```json
class Inventory {
	"id": "string",
	"productId": "string",
	"storeId": "string",
	"quantity": "integer",
	"minStock": "integer"
}
```

```json
class Transfer {
	"id": "string",
	"productId": "string",
	"sourceStoreId": "string",
	"targetStoreId": "string",
	"quantity": "integer",
	"timestamp": "datetime",
	"type": "enum(IN, OUT, TRANSFER)"
}
```

### Diagrama

![alt text](./deliverables/SGI_architecture.drawio.svg)

### Desiciones tecnicas

1. **Estructura de Microservicios:** Facilita la escalabilidad y la adaptación a entornos en la nube.

2. **Modularidad:** Separación de rutas de la aplicación para un escalado modular.

3. **Monorepo:** Centraliza el código en un único repositorio para mantener la consistencia entre instancias y simplificar el despliegue.

4. **Clases Personalizadas:** Se crearon clases como CustomSchema y JoinedSchema que heredan de clases base, extendiendo sus capacidades de forma general y reutilizable.

### Dudas

Cualquier duda o comentario, mandar correo a hgm@heribertogm.com
