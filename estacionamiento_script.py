import sqlite3
import random
from datetime import datetime, timedelta

# Ruta para la base de datos SQLite
db_path = r"./estacionamiento.db"  # Cambia esta ruta si deseas guardar el archivo en otro lugar

# Función para crear la base de datos y las tablas
def setup_database():
    # Crear la conexión
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla Cobranzas (actualizada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cobranzas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Usuario_ID INTEGER NOT NULL,
        Monto REAL,
        Moneda TEXT,
        Fecha_Hora TEXT NOT NULL,
        Empleado_ID INTEGER,
        Estado TEXT CHECK (Estado IN ('Eliminado', 'Sin pagar', 'Pagado')) DEFAULT 'Sin pagar',
        FOREIGN KEY (Empleado_ID) REFERENCES Empleados(DNI),
        FOREIGN KEY (Usuario_ID) REFERENCES Usuario(DNI)
    )
    """)
    print("Tabla 'Cobranzas' creada o ya existe.")
    
    # Crear tabla Empleados (actualizada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empleados (
        DNI INTEGER PRIMARY KEY,
        Nombre TEXT NOT NULL,
        Cargo TEXT NOT NULL,
        Fecha_Contratacion TEXT NOT NULL
    )
    """)
    print("Tabla 'Empleados' creada o ya existe.")

    # Crear tabla Usuarios (sin cambios adicionales)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        DNI INTEGER PRIMARY KEY,
        Nombre TEXT NOT NULL,
        Direccion TEXT,
        TELEFONO TEXT,
        CORREO TEXT,
        ID_Membresia INTEGER,
        Vencimiento_Membresia TEXT,
        FOREIGN KEY (ID_Membresia) REFERENCES Membresia(ID)
    )
    """)
    print("Tabla 'Usuarios' creada o ya existe.")

    # Crear tabla Estacionamientos (sin cambios adicionales)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Estacionamientos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha_Ingreso TEXT,
        Fecha_Egreso TEXT,
        Estado TEXT,
        Usuario_ID INTEGER NOT NULL,
        Empleado_ID INTEGER NOT NULL,
        Cobranza_ID INTEGER,
        FOREIGN KEY (Usuario_ID) REFERENCES Usuarios(DNI),
        FOREIGN KEY (Empleado_ID) REFERENCES Empleados(DNI),
        FOREIGN KEY (Cobranza_ID) REFERENCES Cobranzas(ID)
    )
    ''')
    print("Tabla 'Estacionamientos' creada o ya existe.")
    
    # Crear tabla Precios (sin cambios adicionales)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Precios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Hora INTEGER NOT NULL,
        Costo REAL NOT NULL,
        Moneda TEXT CHECK (Moneda IN ('ARS', 'USD', 'EUR')) DEFAULT 'ARS'
    )
    ''')
    print("Tabla 'Precios' creada o ya existe.")
    
    
    # Crear tabla Membresia (sin cambios adicionales)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Membresia (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Descuento REAL NOT NULL
    )
    ''')
    print("Tabla 'Membresia' creada o ya existe.")

    conn.commit()
    
    # Insertar ejemplos de precios

    monedas = ['ARS', 'USD', 'EUR']
    
    precios = [
        ('1','708','ARS'), ('2','2125','ARS'), ('3','4779','ARS'), ('4','8496','ARS'), ('5','10620','ARS'), ('6','12744','ARS'), ('7','14868','ARS'), 
        ('8','16992','ARS'), ('9','19116','ARS'), ('10','21240','ARS'), ('11','23364','ARS'), ('12','25488','ARS')
    ]
    for hora, costo, moneda in precios:
        cursor.execute("INSERT INTO Precios (Hora, Costo, Moneda) VALUES (?, ?, ?)", (hora, costo, moneda))
    conn.commit()

    # Insertar ejemplos de membresia

    
    membresias = [
        ("Bronze",'0.97'),
        ("Silver",'0.95'),
        ("Bronze",'0.90'),
        ("Bronze",'0.85'),
    ]
    for nombre, descuento in membresias:
        cursor.execute("INSERT INTO Membresia (Nombre, Descuento) VALUES ( ?, ?)", (nombre, descuento))
    conn.commit()

    # Insertar ejemplos de empleados con nuevos campos
    empleados_ids = [
        '12345678',
        '23456789',
        '34567890',
        '45678901',
        '56789012',
        '67890123',
        '78901234',
        '89012345',
        '90123456',
        '12345679'
    ]

    empleados = [
        ('12345678',"Juan", "Gerente", "2020-01-15"),
        ('23456789',"María", "Cajera", "2019-03-22"),
        ('34567890',"Carlos", "Guardia", "2018-07-10"),
        ('45678901',"Ana", "Recepcionista", "2021-05-30"),
        ('56789012',"Miguel", "Supervisor", "2022-02-15"),
        ('67890123',"Lucia", "Encargada", "2020-08-19"),
        ('78901234',"Roberto", "Gerente", "2023-06-05"),
        ('89012345',"Patricia", "Cajera", "2017-09-18"),
        ('90123456',"Andres", "Guardia", "2016-11-20"),
        ('12345679',"Sofia", "Recepcionista", "2021-12-01")
    ]
    for empleado_id, nombre, cargo, fecha_contratacion in  empleados:
        cursor.execute(
            "INSERT INTO Empleados (DNI, Nombre, Cargo, Fecha_Contratacion) VALUES (?, ?, ?, ?)",
            (empleado_id, nombre, cargo, fecha_contratacion)
        )
        
    conn.commit()
    
    # Insertar ejemplos de usuarios
    usuarios = [
        ('39521784', "Luis Paredes", "---","---","---", '3'),
        ('39684143', "Joaquin Blanco", "---","---","---", '2'),
        ('40460123', "Gisela Ruiz", "---","---","---", '3'),
        ('40525124', "Ana Paredes", "---","---","---", '4'),
        ('40134125', "Juan Perez", "---","---","---", '1'),
        ('40852126', "Lucia Gutierrez", "---","---","---", '3'),
        ('40496127', "Rodrigo Sanchez", "---","---","---", '2'),
        ('40136128', "Gabriel Martinez", "---","---","---", '4'),
        ('40916129', "Camila Diaz", "---","---","---", '1'),
        ('40307130', "Esteban Vega", "---","---","---", '2')
    ]
    

    for dni,nombre,direccion,telefono,correo, membresia in usuarios:
        vencimiento_membresia = (datetime.now() + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Usuarios (DNI, Nombre, Direccion, Telefono, Correo, ID_Membresia, Vencimiento_Membresia) VALUES (?, ?, ?, ?, ?, ?, ?)", (dni, nombre, direccion, telefono,correo, membresia, vencimiento_membresia))
    
    conn.commit()


    # Insertar ejemplos de cobranzas
    usuarios_ids = [
    ('39521784'),
    ('39684143'),
    ('40460123'),
    ('40525124'),
    ('40134125'),
    ('40852126'),
    ('40496127'),
    ('40136128'),
    ('40916129'),
    ('40307130')
    ]
    
    for _ in range(10):
        usuario_id = random.choice(usuarios_ids)  # Selección aleatoria
        fecha_hora = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
        INSERT INTO Cobranzas (Usuario_ID, Fecha_Hora)
        VALUES (?, ?)
        """, (usuario_id, fecha_hora))
    
    conn.commit()

    # Insertar ejemplos de estacionamientos
    estados = ['Ocupado', 'Disponible', 'Reservado']
    usuario_ids = [i + 1 for i in range(10)]
    cobranza_ids = [i + 1 for i in range(10)]

    matriculas = [
    'ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345', 
    'PQR678', 'STU901', 'VWX234', 'YZA567', 'BCD890', 
    'EFG321', 'HIJ654', 'KLM987', 'NOP210', 'QRS543', 
    'TUV876', 'WXY109', 'ZAB432', 'CDE765', 'FGH098'
    ]

    empleados_ids = [
    '12345678',
    '23456789',
    '34567890',
    '45678901',
    '56789012',
    '67890123',
    '78901234',
    '89012345',
    '90123456',
    '12345679'
    ]

    for _ in range(10):
        fecha_ingreso = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        fecha_egreso = (datetime.now() + timedelta(hours=random.randint(1, 5))).strftime("%Y-%m-%d %H:%M:%S")
        estado = random.choice(estados)
        usuario_id = random.choice(usuarios_ids)
        empleado_id = random.choice(empleados_ids)
        cobranza_id = random.choice(cobranza_ids)

        cursor.execute("""
        INSERT INTO Estacionamientos (Fecha_Ingreso, Fecha_Egreso, Estado, Usuario_ID, Empleado_ID)
        VALUES (?, ?, ?, ?, ?)
        """, (fecha_ingreso, fecha_egreso, estado, usuario_id, empleado_id))

    conn.commit()

    # Cerrar conexión
    conn.close()
    print("Base de datos SQLite creada y datos insertados exitosamente.")

# Ejecutar la función
if __name__ == "__main__":
    setup_database()
