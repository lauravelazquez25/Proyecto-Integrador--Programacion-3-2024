# Proyecto-Integrador--Programacion-3-2024

Proyecto Grupal – Enunciado del Problema 1
Gestión de Estacionamiento.
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
Grupo 1:
Diseñar el procesamiento de los ESTACIONAMIENTOS:
•
Diseñar las Altas de Estacionamientos con los siguientes atributos: ID (código único), fecha y hora de ingreso, fecha y hora de egreso, y estado (por ejemplo: vacío, ocupado, reservado).
•
Diseñar las Bajas de Estacionamientos.
•
Diseñar las Modificaciones de Estacionamientos.
•
Diseñar las Consultas de Estacionamientos.
Tenga en cuenta las Relaciones:
•
Un estacionamiento está asociado a un usuario, pero un usuario puede tener varios estacionamientos activos (ocupado o reservado).
•
Un estacionamiento es realizado por un empleado, pero un empleado puede realizar varios estacionamientos.
•
Un estacionamiento genera una cobranza, pero una cobranza puede incluir varios estacionamientos.
Grupo 2:
Diseñar el procesamiento de los USUARIOS:
•
Diseñar las Altas de Usuarios con los siguientes atributos: ID (código único), nombre, dirección, teléfono y correo electrónico.
•
Diseñar las Bajas de Usuarios.
•
Diseñar las Modificaciones de Usuarios.
•
Diseñar las Consultas de Usuarios.
Tenga en cuenta las Relaciones:
•
Un estacionamiento está asociado a un usuario, pero un usuario puede tener varios estacionamientos activos.
•
Un usuario está suscripto a una membresía, y a una membresía pueden suscribirse muchos usuarios.
Grupo 3:
Diseñar el procesamiento de los EMPLEADOS:
•
Diseñar las Altas de Empleados con los siguientes atributos: ID (código único), nombre, cargo y fecha de contratación.
•
Diseñar las Bajas de Empleados.
•
Diseñar las Modificaciones de Empleados.
•
Diseñar las Consultas de Empleados.
Tenga en cuenta las Relaciones:
•
Un estacionamiento es realizado por un empleado, pero un empleado puede realizar varios estacionamientos.
•
Una reserva es realizada por un empleado, pero un empleado puede realizar varias reservas.
Grupo 4:
Diseñar el procesamiento de las COBRANZAS:
•
Diseñar las Altas de Cobranzas con los siguientes atributos: ID (código único), monto, moneda, fecha y hora.
•
Diseñar las Bajas de Cobranzas.
•
Diseñar las Modificaciones de Cobranzas.
•
Diseñar las Consultas de Cobranzas.
Tenga en cuenta las Relaciones:
•
Una cobranza es realizada por un empleado, pero un empleado puede realizar varias cobranzas.
Todos:
•
Elaborar el Diseño de Altas, Bajas, Modificaciones y Consultas del SG de Estacionamiento. Asimismo, deben integrar las tres partes para obtener un diseño único.
•
Elaborar el Programa para la Gestión del Estacionamiento según lo diseñado.
Además de Estacionamientos, Usuarios, Empleados y Cobranzas, intervienen las siguientes entidades:
ESPACIOS que incluyen los atributos: ID (código único), ancho, largo, altura, ubicación y cantidad disponible.
VEHÍCULOS con los atributos: Patente (código único).
MEMBRESÍA de usuarios con los atributos: ID (código único), tipo de membresía y fecha de vencimiento.
PRECIOS de estacionamiento con los atributos: ID (código único), tiempo en horas, monto, moneda.
Notas:
Asuma todo lo que crea conveniente; si considera necesario, puede agregar otros atributos en las entidades.
