import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk

# Conexión a la base de datos
conn = sqlite3.connect('estacionamiento.db')
cursor = conn.cursor()

# Funciones de gestión de cobranzas
def alta_cobranza(monto, moneda, empleado_id):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO Cobranzas (Monto, Moneda, Fecha_Hora, Empleado_ID)
        VALUES (?, ?, ?, ?)
    """, (monto, moneda, fecha_hora, empleado_id))
    conn.commit()
    messagebox.showinfo("Alta de Cobranza", "Cobranza registrada exitosamente.")

def baja_cobranza(cobranza_id):
    cursor.execute("""
        DELETE FROM Cobranzas WHERE ID = ?
    """, (cobranza_id,))
    conn.commit()
    messagebox.showinfo("Baja de Cobranza", "Cobranza eliminada exitosamente.")

def modificar_cobranza(cobranza_id, nuevo_monto, nueva_moneda, nuevo_empleado_id):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE Cobranzas
        SET Monto = ?, Moneda = ?, Fecha_Hora = ?, Empleado_ID = ?
        WHERE ID = ?
    """, (nuevo_monto, nueva_moneda, fecha_hora, nuevo_empleado_id, cobranza_id))
    conn.commit()
    messagebox.showinfo("Modificación de Cobranza", "Cobranza modificada exitosamente.")

def consultar_cobranzas():
    cursor.execute("SELECT * FROM Cobranzas")
    cobranzas = cursor.fetchall()
    resultado = "\n".join([str(cobranza) for cobranza in cobranzas])
    messagebox.showinfo("Cobranzas Registradas", resultado if resultado else "No hay cobranzas registradas.")

def consultar_cobranza_por_id(cobranza_id):
    cursor.execute('SELECT * FROM Cobranzas WHERE ID = ?', (cobranza_id,))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Consulta de Cobranza por ID", str(result))
    else:
        messagebox.showinfo("Consulta de Cobranza por ID", f"No se encontró ninguna cobranza con ID {cobranza_id}.")

# Interfaz de usuario con Tkinter
def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Cobranzas")
    root.geometry("400x400")

    # Labels y entradas
    tk.Label(root, text="ID de la Cobranza:").grid(row=0, column=0, pady=5)
    entry_cobranza_id = tk.Entry(root)
    entry_cobranza_id.grid(row=0, column=1, pady=5)

    tk.Label(root, text="Monto:").grid(row=1, column=0, pady=5)
    entry_monto = tk.Entry(root)
    entry_monto.grid(row=1, column=1, pady=5)

    tk.Label(root, text="Moneda (ARS/USD/EUR):").grid(row=2, column=0, pady=5)
    entry_moneda = tk.Entry(root)
    entry_moneda.grid(row=2, column=1, pady=5)

    tk.Label(root, text="ID del Empleado:").grid(row=3, column=0, pady=5)
    entry_empleado_id = tk.Entry(root)
    entry_empleado_id.grid(row=3, column=1, pady=5)

    # Botones de acciones
    button_font = ("Helvetica", 12, "bold")
    tk.Button(root, text="Registrar Cobranza", command=lambda: alta_cobranza(
        float(entry_monto.get()), entry_moneda.get(), int(entry_empleado_id.get())),
        font=button_font).grid(row=4, column=0, pady=10)

    tk.Button(root, text="Eliminar Cobranza", command=lambda: baja_cobranza(
        int(entry_cobranza_id.get())), font=button_font).grid(row=4, column=1, pady=10)

    tk.Button(root, text="Modificar Cobranza", command=lambda: modificar_cobranza(
        int(entry_cobranza_id.get()), float(entry_monto.get()), entry_moneda.get(), int(entry_empleado_id.get())),
        font=button_font).grid(row=5, column=0, pady=10)

    tk.Button(root, text="Consultar Cobranzas", command=consultar_cobranzas,
        font=button_font).grid(row=5, column=1, pady=10)

    tk.Button(root, text="Consultar Cobranza por ID", command=lambda: consultar_cobranza_por_id(
        int(entry_cobranza_id.get())), font=button_font).grid(row=6, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Salir", command=root.quit, font=button_font).grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
    conn.close()
