# Proyecto-Integrador--Programacion-3-2024

Proyecto Grupal – Enunciado del Problema 1
### Gestión de Estacionamiento.

Una empresa dueña de un estacionamiento está interesada en automatizar la gestión de su actividad y para esto se pide codificar un programa en Python, teniendo en cuenta lo siguiente:

Según el enunciado del problema y siguiendo la distribución de las preguntas para cada uno de los estudiantes del grupo, se solicita:

•
Crear la base de datos en MS ACCESS o similar, para automatizar la gestión de estacionamientos
•
Generar las sentencias de creación de tablas y relaciones
•
Crear las tablas con los campos de cada una según su modelo físico (considere PK y FK)
•
Crear las relaciones entre las tablas
•
Ingresar al menos 5 registros de ejemplo en cada una de las tablas
Además, se debe integrar las bases de datos de todos los grupos en una única base de datos.

# Proyecto de Gestión de Cobranzas

Este proyecto permite gestionar cobranzas en un sistema de estacionamiento. Incluye funcionalidades para registrar, eliminar, modificar y consultar cobranzas en una base de datos SQLite.

## Características

- **Registro de Cobranzas**: Añade nuevas cobranzas con información detallada.
- **Eliminación de Cobranzas**: Elimina registros específicos de cobranzas.
- **Modificación de Cobranzas**: Actualiza los detalles de una cobranza ya registrada.
- **Consulta de Cobranzas**: Permite visualizar todas las cobranzas registradas o consultar una específica por su ID.
- **Interfaz de Línea de Comandos (CLI)**: Un menú interactivo que permite al usuario acceder a las funcionalidades del sistema.

## Requisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.6 o superior**: Este proyecto utiliza Python, así que necesitarás tenerlo instalado en tu sistema. Puedes verificar si tienes Python instalado con el siguiente comando:

  ```bash
  python --version
  ```
- **SQLite**: Este proyecto utiliza SQLite como base de datos. SQLite ya viene incluido en Python, por lo que no se necesita instalar nada adicional.

## Instalación

1. Clona este repositorio en tu maquina local: 

   ```
   git clone https://github.com/lauravelazquez25/Proyecto-Integrador--Programacion-3-2024.git
   ```
2. Accede al directorio

   ```
   cd /directorio_del_proyecto
   ```
3. Crea la base de datos: 
    Si el archivo de la base de datos "estacionamiento.db" no existe en el directorio, el script la generará automaticamente cuando se ejecute por primera vez.
    

## Uso


Para ejecutar el sistema de gestión de cobranzas, utiliza el siguiente comando:

  ```
  python control_cobranzas.py
  ```
   
## Menú interactivo 
   
Al ejecutar el script, verás un menú con las siguientes opciones:

1. Registrar Cobranza: Permite añadir una nueva cobranza al sistema.
2. Eliminar Cobranza: Elimina una cobranza del sistema utilizando su ID.
3. Modificar Cobranza: Actualiza los datos de una cobranza específica.
4. Consultar Todas las Cobranzas: Muestra todas las cobranzas registradas.
5. Consultar Cobranza por ID: Busca y muestra una cobranza específica por su ID.
6. Salir: Cierra el sistema de gestión de cobranzas.

### Ejemplo de Uso

1. Registrar Cobranza:
    -Ingresa el monto, la moneda (ARS/USD/EUR) y el ID del empleado cuando se te solicite.

2. Consultar Cobranza por ID:
    -Ingresa el ID de la cobranza que deseas consultar y se mostrará en pantalla.  
   
