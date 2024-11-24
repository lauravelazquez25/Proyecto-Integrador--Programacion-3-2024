# Proyecto-Integrador--Programacion-3-2024

## Proyecto Grupal – Enunciado del Problema 1

### Gestión de Estacionamiento

Una empresa dueña de un estacionamiento está interesada en automatizar la gestión de su actividad. Este proyecto tiene como objetivo desarrollar un sistema en Python para cubrir las necesidades descritas en el enunciado, incluyendo las siguientes tareas principales:

1. Crear la base de datos en SQLite o similar, para automatizar la gestión de estacionamientos.
2. Generar las sentencias de creación de tablas y relaciones.
3. Crear las tablas con los campos de cada una según su modelo físico (considerando PK y FK).
4. Crear las relaciones entre las tablas.
5. Ingresar al menos 5 registros de ejemplo en cada una de las tablas.
6. Integrar las bases de datos de todos los grupos en una única base de datos consolidada.

---

## Proyecto de Gestión de Cobranzas

Este proyecto forma parte de la gestión del estacionamiento y está enfocado en el manejo de las cobranzas. Permite registrar, eliminar, modificar y consultar cobranzas utilizando una base de datos SQLite. Además, implementa un sistema de roles y permisos para garantizar la seguridad y accesibilidad del sistema.

---

## Características

### Funcionalidades principales
- **Registro de Cobranzas**: Agrega nuevas cobranzas con detalles como usuario, monto y fecha.
- **Cobro y Pago de Cobranzas**: Calcula montos finales considerando descuentos por membresías y reservas, y permite marcar cobranzas como pagadas.
- **Eliminación de Cobranzas**: Realiza una eliminación lógica de cobranzas específicas.
- **Modificación de Cobranzas**: Permite actualizar los detalles de una cobranza existente.
- **Consulta de Cobranzas**: Visualiza todas las cobranzas activas o busca cobranzas específicas por ID.
- **Sistema de Login**: Registra y autentica empleados con contraseñas cifradas (`bcrypt`), asignando roles según permisos.
- **Descuentos Avanzados**: Aplica descuentos automáticos basados en membresías y reservas.
- **Interfaz Gráfica**: Desarrollada con `Tkinter` para facilitar el uso del sistema.

### Modularidad
El proyecto está diseñado de manera modular, lo que permite la reutilización de componentes como:
- **Gestión de Contraseñas**: Registro y autenticación segura.
- **Cálculo de Tarifas**: Lógica de redondeo de horas y aplicación de descuentos.
- **Interfaz de Búsqueda**: Tabla interactiva reutilizable para mostrar resultados.

---

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
   
