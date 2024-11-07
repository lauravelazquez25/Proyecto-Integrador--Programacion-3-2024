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
    
    # Crear tabla Empleados (actualizada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empleados (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Cargo TEXT NOT NULL,
        Fecha_Contratacion TEXT NOT NULL
    )
    """)
    print("Tabla 'Empleados' creada o ya existe.")

    # Crear tabla Cobranzas (actualizada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cobranzas (
        ID TEXT PRIMARY KEY,
        Matricula TEXT NOT NULL,
        Monto REAL NOT NULL,
        Moneda TEXT NOT NULL,
        Fecha_Hora TEXT NOT NULL,
        Empleado_ID INTEGER NOT NULL,
        FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
    )
    """)
    print("Tabla 'Cobranzas' creada o ya existe.")

    # Crear tabla Usuarios (sin cambios adicionales)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        Membresia TEXT
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
        FOREIGN KEY (Usuario_ID) REFERENCES Usuarios(ID),
        FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
        FOREIGN KEY (Cobranza_ID) REFERENCES Cobranzas(ID)
    )
    ''')
    print("Tabla 'Estacionamientos' creada o ya existe.")
    
    
    #Trigger para generar la ID de las cobranzas
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS trigger_generate_cobranza_id
    BEFORE INSERT ON Cobranzas
    FOR EACH ROW
    BEGIN
        UPDATE Cobranzas
        SET ID = NEW.Matricula || '_' || strftime('%Y%m%d%H%M', NEW.Fecha_Hora)
        WHERE rowid = NEW.rowid;
    END;
    ''')
    print("Tabla 'Estacionamientos' creada o ya existe.")
    
    conn.commit()
    
    # Insertar ejemplos de empleados con nuevos campos
    empleados = [
        ("Juan", "Gerente", "2020-01-15"), ("María", "Cajera", "2019-03-22"), ("Carlos", "Guardia", "2018-07-10"),
        ("Ana", "Recepcionista", "2021-05-30"), ("Miguel", "Supervisor", "2022-02-15"), ("Lucia", "Encargada", "2020-08-19"),
        ("Roberto", "Gerente", "2023-06-05"), ("Patricia", "Cajera", "2017-09-18"), ("Andres", "Guardia", "2016-11-20"),
        ("Sofia", "Recepcionista", "2021-12-01")
    ]
    
    for nombre, cargo, fecha_contratacion in empleados:
        cursor.execute("INSERT INTO Empleados (Nombre, Cargo, Fecha_Contratacion) VALUES (?, ?, ?)", (nombre, cargo, fecha_contratacion))
    
    conn.commit()
    
    # Insertar ejemplos de usuarios
    usuarios = [
        ("Luis", "Paredes", "Gold"), ("Joaquin", "Blanco", "Silver"), ("Gisela", "Ruiz", "Gold"),
        ("Ana", "Paredes", "Platinum"), ("Juan", "Perez", "Bronze"), ("Lucia", "Gutierrez", "Gold"),
        ("Rodrigo", "Sanchez", "Silver"), ("Gabriel", "Martinez", "Platinum"), ("Camila", "Diaz", "Bronze"),
        ("Esteban", "Vega", "Silver")
    ]

    for nombre, apellido, membresia in usuarios:
        cursor.execute("INSERT INTO Usuarios (Nombre, Apellido, Membresia) VALUES (?, ?, ?)", (nombre, apellido, membresia))
    
    conn.commit()

    # Insertar ejemplos de cobranzas
    monedas = ['ARS', 'USD', 'EUR']
    matriculas = [
    'ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345', 
    'PQR678', 'STU901', 'VWX234', 'YZA567', 'BCD890', 
    'EFG321', 'HIJ654', 'KLM987', 'NOP210', 'QRS543', 
    'TUV876', 'WXY109', 'ZAB432', 'CDE765', 'FGH098'
    ]
    empleados_ids = [i + 1 for i in range(10)]  # Asumimos que los empleados tienen IDs del 1 al 10
    
    for _ in range(10):
        monto = round(random.uniform(100, 1000), 2)
        moneda = random.choice(monedas)
        matricula = random.choice(matriculas)
        fecha_hora = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        empleado_id = random.choice(empleados_ids)
        
        cursor.execute("""
        INSERT INTO Cobranzas (Matricula, Monto, Moneda, Fecha_Hora, Empleado_ID)
        VALUES (?, ?, ?, ?, ?)
        """, (matricula, monto, moneda, fecha_hora, empleado_id))
    
    conn.commit()

    # Insertar ejemplos de estacionamientos
    estados = ['Ocupado', 'Disponible', 'Reservado']
    usuario_ids = [i + 1 for i in range(10)]
    cobranza_ids = [i + 1 for i in range(10)]

    for _ in range(10):
        fecha_ingreso = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        fecha_egreso = (datetime.now() + timedelta(hours=random.randint(1, 5))).strftime("%Y-%m-%d %H:%M:%S")
        estado = random.choice(estados)
        usuario_id = random.choice(usuario_ids)
        empleado_id = random.choice(empleados_ids)
        cobranza_id = random.choice(cobranza_ids)

        cursor.execute("""
        INSERT INTO Estacionamientos (Fecha_Ingreso, Fecha_Egreso, Estado, Usuario_ID, Empleado_ID, Cobranza_ID)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (fecha_ingreso, fecha_egreso, estado, usuario_id, empleado_id, cobranza_id))

    conn.commit()

    # Cerrar conexión
    conn.close()
    print("Base de datos SQLite creada y datos insertados exitosamente.")

# Ejecutar la función
if __name__ == "__main__":
    setup_database()
