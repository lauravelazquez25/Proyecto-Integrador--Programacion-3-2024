TABLE Empleados (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Cargo TEXT NOT NULL,
        Fecha_Contratacion TEXT NOT NULL
    )
    
TABLE Cobranzas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Monto REAL NOT NULL,
        Moneda TEXT NOT NULL,
        Fecha_Hora TEXT NOT NULL,
        Empleado_ID INTEGER NOT NULL,
        FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
    )

TABLE Usuarios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        Membresia TEXT
    )

TABLE Estacionamientos (
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