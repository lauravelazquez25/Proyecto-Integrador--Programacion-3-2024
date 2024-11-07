import sqlite3
from datetime import datetime

conn = sqlite3.connect('estacionamiento.db')
cursor = conn.cursor()

def alta_cobranza(monto, moneda, empleado_id):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO Cobranzas (Monto, Moneda, Fecha_Hora, Empleado_ID)
    VALUES (?, ?, ?, ?)
    """, (monto, moneda, fecha_hora, empleado_id))
    conn.commit()
    print("Cobranza registrada exitosamente.")

def baja_cobranza(cobranza_id):
    cursor.execute("""
        DELETE FROM Cobranzas WHERE ID = ?
    """, (cobranza_id,))
    conn.commit()
    print("Cobranza eliminada exitosamente.")

def modificar_cobranza(cobranza_id, nuevo_monto, nueva_moneda, nuevo_empleado_id):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE Cobranzas
        SET Monto = ?, Moneda = ?, Fecha_Hora = ?, Empleado_ID = ?
        WHERE ID = ?
    """, (nuevo_monto, nueva_moneda, fecha_hora, nuevo_empleado_id, cobranza_id))
    conn.commit()
    print("Cobranza modificada exitosamente.")

def consultar_cobranzas():
    cursor.execute("SELECT * FROM Cobranzas")
    cobranzas = cursor.fetchall()
    print("Cobranzas registradas:")
    for cobranza in cobranzas:
        print(cobranza)

def consultar_cobranza_por_id(cobranza_id):
    cursor.execute('SELECT * FROM cobranzas WHERE id = ?', (cobranza_id,))
    result = cursor.fetchone()
    if result:
        print(result)
    else:
        print(f"No se encontro ninguna cobranza con ID {cobranza_id}.")
    


def menu_cobranzas():
    while True:
        print("\n--- Gestión de Cobranzas ---")
        print("1. Registrar Cobranza")
        print("2. Eliminar Cobranza")
        print("3. Modificar Cobranza")
        print("4. Consultar Cobranzas")
        print("5. Consultar Cobranza por ID")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            monto = float(input("Monto: "))
            moneda = input("Moneda (ARS/USD/EUR): ")
            empleado_id = int(input("ID del Empleado: "))
            alta_cobranza(monto, moneda, empleado_id)
        elif opcion == "2":
            cobranza_id = int(input("ID de la Cobranza a eliminar: "))
            baja_cobranza(cobranza_id)
        elif opcion == "3":
            cobranza_id = int(input("ID de la Cobranza a modificar: "))
            nuevo_monto = float(input("Nuevo Monto: "))
            nueva_moneda = input("Nueva Moneda (ARS/USD/EUR): ")
            nuevo_empleado_id = int(input("ID del nuevo Empleado: "))
            modificar_cobranza(cobranza_id, nuevo_monto, nueva_moneda, nuevo_empleado_id)
        elif opcion == "4":
            consultar_cobranzas()
        elif opcion == "5":
            cobranza_id = int(input("ID de la Cobranza a consultar: "))
            consultar_cobranza_por_id(cobranza_id)
        elif opcion == "6":
            print("Saliendo del sistema de gestión de cobranzas...")
            break
        else:
            print("Opción inválida, por favor intente de nuevo.")
            

if __name__ == "__main__":
    menu_cobranzas()
    conn.close()
