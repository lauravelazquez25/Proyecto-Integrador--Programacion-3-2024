import sqlite3
import tkinter as tk
from tkinter import END, Button, Entry, Label, StringVar, Toplevel, ttk, simpledialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os
import math
import bcrypt

conn = sqlite3.connect('estacionamiento.db')
cursor = conn.cursor()

# Hay que implementar un sistema de login fiable para la parte de permisos
id_empleado_logueado = 0
permisos_empleado = 1


def descuento_membresia(usuario_id) -> int:
    """
    Calcula el multiplicador de descuento basado en la membresía de un usuario.

    Args:
        usuario_id (int): Identificación del usuario.

    Returns:
        int: Multiplicador correspondiente a la membresía, o 1 si no aplica descuento.
    """
    mult_membresia = 1
    cursor.execute('SELECT * FROM Usuarios WHERE DNI = ?', (usuario_id,))
    usuario = cursor.fetchone()
    if usuario is not None:
        membresia_id = usuario[5]
        fecha_vencimiento = usuario[6]
        date_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
        date_actual = datetime.now().date()
        if(date_vencimiento > date_actual):
            print("Membresia valida")
            print(membresia_id)
            cursor.execute('SELECT * FROM Membresia WHERE ID = ?', (membresia_id,))
            membresia = cursor.fetchone()
            if membresia is not None:
                mult_membresia = membresia[2]
                print(mult_membresia)
    return mult_membresia


def roundUP_horas(ingreso: str, egreso: str) -> int:
    """
    Calcula la cantidad de horas entre dos fechas redondeando hacia arriba.

    Args:
        ingreso (str): Fecha y hora de ingreso en formato "YYYY-MM-DD HH:MM:SS".
        egreso (str): Fecha y hora de egreso en el mismo formato.

    Returns:
        int: Cantidad de horas redondeadas hacia arriba.
    """
    ingreso_dt = datetime.strptime(ingreso, "%Y-%m-%d %H:%M:%S")
    egreso_dt = datetime.strptime(egreso, "%Y-%m-%d %H:%M:%S")
    diferencia = egreso_dt - ingreso_dt
    total_horas = diferencia.total_seconds() / 3600
    return math.ceil(total_horas)

def alta_cobranza(Usuario) -> int:
    """
    Registra una nueva cobranza en la base de datos.

    Args:
        Usuario (int): DNI del usuario.

    Returns:
        int: ID de la cobranza recién creada.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO Cobranzas (Usuario_ID, Fecha_Hora)
    VALUES (?, ?)
    """, (Usuario, fecha_hora))
    conn.commit()
    print("Cobranza registrada exitosamente.")
    cobranza_id = cursor.lastrowid
    return cobranza_id

def cobrar_cobranza(ingreso, egreso, cobranza_id, reserva):
    """
    Calcula y actualiza el monto de una cobranza.

    Args:
        ingreso (str): Fecha y hora de ingreso.
        egreso (str): Fecha y hora de egreso.
        cobranza_id (int): ID de la cobranza.
        reserva (bool): Indica si se aplica descuento por reserva.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mult_membresia = 1
    mult_reserva = 1
    if reserva:
        mult_reserva = 0.9
    horas = roundUP_horas(ingreso, egreso)

    #Calculo del monto base
    cursor.execute('SELECT * FROM Precios WHERE Hora = ?', (horas,))
    precio = cursor.fetchone()
    if precio is not None:
        monto_base = precio[2]
        moneda = precio[3]
    else:
        monto_base = horas*2500
        moneda = 'ARS'

    # Consulta del usuario y su membresia
    cobranza = consultar_cobranza_por_id(cobranza_id)
    usuario_id = cobranza[1]
    mult_membresia = descuento_membresia(usuario_id)
    monto_final = monto_base*mult_reserva*mult_membresia
    
    # Actualizacion de la 
    cursor.execute("""
        UPDATE Cobranzas
        SET Monto = ?, Moneda = ?, Fecha_Hora = ?, Empleado_ID = ?
        WHERE ID = ?
    """, (monto_final, moneda, fecha_hora, id_empleado_logueado, cobranza_id))
    conn.commit()

def pagar_cobranza(cobranza):
    """
    Cambia el estado de una cobranza a "Pagado".

    Args:
        cobranza (int): ID de la cobranza.
    """
    cursor.execute("""
        UPDATE Cobranzas
        SET Estado = 'Pagado'
        WHERE ID = ?
    """, (cobranza,))
    conn.commit()


def baja_cobranza(cobranza):
    """
    Marca una cobranza como eliminada en la base de datos.

    Args:
        cobranza (int): ID de la cobranza.
    """
    cursor.execute("""
        UPDATE Cobranzas
        SET Estado = 'Eliminado', Empleado_ID = ?
        WHERE ID = ?
    """, (id_empleado_logueado, cobranza))
    conn.commit()


def modificar_cobranza(cobranza_id, nuevo_monto, nueva_moneda, nuevo_empleado_id):
    """
    Modifica los datos de una cobranza existente.

    Args:
        cobranza_id (int): ID de la cobranza.
        nuevo_monto (float): Nuevo monto a asignar.
        nueva_moneda (str): Nueva moneda del monto.
        nuevo_empleado_id (int): ID del empleado que realiza el cambio.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE Cobranzas
        SET Monto = ?, Moneda = ?, Fecha_Hora = ?, Empleado_ID = ?
        WHERE ID = ?
    """, (nuevo_monto, nueva_moneda, fecha_hora, nuevo_empleado_id, cobranza_id))
    conn.commit()
    print("Cobranza modificada exitosamente.")


#Se modificaron las consultas de cobranza para que devuelvan los resultados del fetch, para poder trabajarlos mejor con tkinter

#Consulta todas las cobranzas existentes
def consultar_cobranzas_disponibles():
    """
    Recupera todas las cobranzas disponibles que no están eliminadas.

    Returns:
        list: Lista de cobranzas disponibles.
    """
    cursor.execute("""
        SELECT * FROM Cobranzas
        WHERE ESTADO NOT LIKE ?
        """, ('Eliminado',))
    cobranzas = cursor.fetchall()
    return cobranzas

def consultar_cobranzas():
    """
    Recupera todas las cobranzas sin filtrar por estado.

    Returns:
        list: Lista de todas las cobranzas.
    """
    cursor.execute("SELECT * FROM Cobranzas")
    cobranzas = cursor.fetchall()
    return cobranzas


#Consulta una cobranza por referencia de ID o DNI de usuario
def consultar_cobranza_por_referencia(referencia):
    """
    Recupera una cobranza por ID o por DNI del usuario.

    Args:
        referencia (str): ID de la cobranza o DNI del usuario.

    Returns:
        tuple or None: Datos de la cobranza o None si no existe.
    """
    cursor.execute('SELECT * FROM cobranzas WHERE ID LIKE ? OR Usuario_ID LIKE ?', (referencia,referencia))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"No se encontro ninguna cobranza con ID {referencia}.")


#Consulta una cobranza por ID
def consultar_cobranza_por_id(referencia):
    """
    Recupera una cobranza por su ID.

    Args:
        referencia (str): ID de la cobranza.

    Returns:
        tuple or None: Datos de la cobranza o None si no existe.
    """
    cursor.execute('SELECT * FROM cobranzas WHERE ID LIKE ?', (referencia,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"No se encontro ninguna cobranza con ID {referencia}.")


def consultar_empleado_por_id(referencia):
    """
    Recupera un empleado por su DNI.

    Args:
        referencia (str): DNI del empleado.

    Returns:
        tuple or None: Datos del empleado o None si no existe.
    """
    cursor.execute('SELECT * FROM empleados WHERE DNI LIKE ?', (referencia,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"No se encontro ninguna empleado con ID {referencia}.")


def consultar_usuario_por_id(referencia):
    """
    Recupera un usuario por su DNI.

    Args:
        referencia (str): DNI del usuario.

    Returns:
        tuple or None: Datos del usuario o None si no existe.
    """
    cursor.execute('SELECT * FROM usuarios WHERE DNI LIKE ?', (referencia,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"No se encontro ninguna usuario con ID {referencia}.")

def centrar_ventana(ventana):
    """
    Centra una ventana de Tkinter en la pantalla.

    Args:
        ventana (tk.Tk or tk.Toplevel): Ventana a centrar.
    """
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# Registro de empleados (con contraseña cifrada)
def registrar_empleado():
    """
    Muestra un formulario para registrar un nuevo empleado con contraseña cifrada.
    """
    def confirmar():
        empleado_id = int(entry_empleado_id.get())
        permisos = int(entry_permisos.get())
        password = entry_password.get()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        empleado_existente = consultar_empleado_por_id(empleado_id)
        if (empleado_existente is not None):
            try:
                cursor.execute("""
                    INSERT INTO Empleado_Contraseña (Empleado_ID, Password, Permisos)
                    VALUES (?, ?, ?)
                """, (empleado_id, hashed_password, permisos))
                conn.commit()
                messagebox.showinfo("Éxito", "Registro exitoso.")
                ventana_registro.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El Empleado ID ya está registrado.")
        else:
            messagebox.showerror("Error", "El Empleado ID especificado no existe.")
        
    def cancelar():
        ventana_registro.destroy()

    ventana_registro = Toplevel()
    ventana_registro.title("Registrar Empleado")
    ventana_registro.geometry("300x200")
    centrar_ventana(ventana_registro)

    Label(ventana_registro, text="Registrar Empleado", font="Helvetica").pack(pady=10)
    Label(ventana_registro, text="Empleado ID:").pack()
    entry_empleado_id = Entry(ventana_registro)
    entry_empleado_id.pack()

    Label(ventana_registro, text="Contraseña:").pack()
    entry_password = Entry(ventana_registro, show="*")
    entry_password.pack()

    Label(ventana_registro, text="Permisos (0-3):").pack()
    entry_permisos = Entry(ventana_registro)
    entry_permisos.pack()

    Button(ventana_registro, text="Confirmar", command=confirmar).pack(pady=5)
    Button(ventana_registro, text="Cancelar", command=cancelar).pack(pady=5)

# Verificar login
def verificar_login(empleado_id, password):
    """
    Verifica las credenciales de un empleado.

    Args:
        empleado_id (int): ID del empleado.
        password (str): Contraseña ingresada.

    Returns:
        tuple: (bool, int) - True y permisos si la verificación es exitosa; False y None si falla.
    """
    cursor.execute("SELECT Password, Permisos FROM Empleado_Contraseña WHERE Empleado_ID = ?", (empleado_id,))
    result = cursor.fetchone()
    if result:
        hashed_password, permisos = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True, permisos
    return False, None

# Modificar el login actual
def login_verify():
    """
    Verifica las credenciales ingresadas en el formulario de inicio de sesión.
    """
    global username_entry1, password_entry1, ventana_login  # Aseguramos que las variables sean accesibles
    empleado_id = username_verify.get()
    password = password_verify.get()

    # Limpiar las entradas después de obtener los valores
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)
    
    # Verificar las credenciales
    valido, permisos = verificar_login(empleado_id, password)
    if valido:
        global id_empleado_logueado, permisos_empleado
        id_empleado_logueado = empleado_id
        permisos_empleado = permisos
        ventana_login.destroy()  # Cerrar la ventana de login
        menu_cobranzas()  # Abrir el menú de cobranzas
    else:
        messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")

# Modificar la ventana de login
def menu_login():
    """
    Crea el formulario de inicio de sesión con opciones para registrarse.
    """
    global username_entry1, password_entry1, ventana_login  # Declaramos como global

    ventana_login = tk.Tk()  # Creamos la ventana principal
    ventana_login.title("Control Cobranzas v1.0")
    ventana_login.geometry("300x250")
    centrar_ventana(ventana_login)

    Label(ventana_login, text="Por favor ingrese sus datos para continuar.").pack(pady=10)

    # Variables para capturar el ID y contraseña
    global username_verify, password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    # Campos para ID y contraseña
    Label(ventana_login, text="Empleado ID:").pack()
    username_entry1 = Entry(ventana_login, textvariable=username_verify)
    username_entry1.pack()

    Label(ventana_login, text="Contraseña:").pack()
    password_entry1 = Entry(ventana_login, textvariable=password_verify, show="*")
    password_entry1.pack()

    # Botones para iniciar sesión y registrarse
    Button(ventana_login, text="Iniciar Sesión", command=login_verify).pack(pady=5)
    Button(ventana_login, text="Registrarse", command=registrar_empleado).pack(pady=5)

    # Asociar la tecla Enter al login
    password_entry1.bind('<Return>', lambda event: login_verify())
    ventana_login.mainloop()

# Menu de cobranzas en Tkinter
def menu_cobranzas():
    """
    Interfaz principal de gestión de cobranzas con opciones de alta, baja, modificación y consulta.
    """
    # Crea una tabla de la base de datos
    def crear_tabla(ventana):
        columnas = ("id", "usuario", "monto", "moneda", "fecha", "empleado","estado")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

        tabla.heading("id", text="ID")
        tabla.heading("usuario", text="Usuario")
        tabla.heading("monto", text="Monto")
        tabla.heading("moneda", text="Moneda")
        tabla.heading("fecha", text="Fecha")
        tabla.heading("empleado", text="Empleado")
        tabla.heading("estado", text="Estado")

        tabla.column("id", width=10)
        tabla.column("usuario", width=25)
        tabla.column("monto", width=20)
        tabla.column("moneda", width=15)
        tabla.column("fecha", width=50)
        tabla.column("empleado", width=50)
        tabla.column("estado", width=50)
        tabla.pack(fill=tk.BOTH, expand=True)
        return tabla
    

    #Limpia la tabla // Utilizado para las busquedas principalmente
    def limpiar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

    
    # TEST
    def test():
        print("TODO OK")

    # Busca y muestra las cobranzas en la tabla de tkinter cuya id o usuario_id coincida
    # Buscar "all" Muestra todas las cobranzas (incluyendo eliminadas)
    def buscar():
        limpiar_tabla()
        referencia = entrada_busqueda.get().lower()
        if (referencia):
            if referencia.lower() == "all": #pero en lowercase
                buscar_todos()
            else:
                cobranza = consultar_cobranza_por_referencia(referencia)
                if cobranza:
                    tabla.insert("", tk.END, values=cobranza)
        else:
            buscar_todos_disponibles()

    def buscar_todos():
        cobranzas = consultar_cobranzas()
        for cobranza in cobranzas:
            tabla.insert("", tk.END, values=cobranza)

    def buscar_todos_disponibles():
        cobranzas = consultar_cobranzas_disponibles()
        for cobranza in cobranzas:
            tabla.insert("", tk.END, values=cobranza)

    #Alta cobranza
    def agregar_cobranza():
        def confirmar():
            alta_cobranza(nuevo_usuario.get())
            limpiar_tabla()
            buscar_todos_disponibles()
            menu_agregar.destroy()
        def cancelar():
            menu_agregar.destroy()

        # ----- Comienzo ------
        menu_agregar = Toplevel(menu)
        menu_agregar.title("Nueva Cobranza")
        menu_agregar.geometry("300x100")
        menu_agregar.columnconfigure(0, weight=1)
        menu_agregar.columnconfigure(1, weight=1)
        centrar_ventana(menu_agregar)
        Label(menu_agregar, text = "Ingrese los datos de la nueva cobranza", justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=5,padx=5)

        Label(menu_agregar, text="DNI Usuario:").grid(row=1, column=0, sticky=tk.E,pady=5,padx=5)
        
        nuevo_usuario = Entry(menu_agregar)
        nuevo_usuario.grid(row=1, column=1,sticky=tk.W)

        
        cuadro_botones = tk.Frame(menu_agregar)
        cuadro_botones.grid(row=5,column=0,columnspan=3)
        Button(cuadro_botones, text = "OK", width = 10, height = 1, command = confirmar).pack(side=tk.LEFT, padx=10,pady=10)
        Button(cuadro_botones, text = "Cancel", width = 10, height = 1, command = cancelar).pack(side=tk.LEFT, padx=10,pady=10)
        
    #Cobrar cobranza
    def cobrar():
        
        def confirmar():
            fecha_hora_ingreso = f"{fecha_ingreso.get()} {hora_ingreso.get()}:{minuto_ingreso.get()}:{segundo_ingreso.get()}"
            print(fecha_hora_ingreso)
            fecha_hora_egreso = f"{fecha_egreso.get()} {hora_egreso.get()}:{minuto_egreso.get()}:{segundo_egreso.get()}"
            print(fecha_hora_egreso)
            cobrar_cobranza(fecha_hora_ingreso,fecha_hora_egreso, id_cobranza, check_reserva.get())
            limpiar_tabla()
            buscar_todos_disponibles()
            menu_cobrar.destroy()
        def cancelar():
            menu_cobrar.destroy()
        
        id_cobranza = simpledialog.askstring("Cobrar Cobranza", "ID de la cobranza a cobrar:", parent=menu)
        if id_cobranza is None:
            return
        cobranza = consultar_cobranza_por_id(id_cobranza)
        
        if(cobranza and cobranza[6] == 'Sin pagar'):
            menu_cobrar = Toplevel(menu)
            menu_cobrar.title("Modificar Cobranza")
            menu_cobrar.geometry("300x250")
            centrar_ventana(menu_cobrar)
            Label(menu_cobrar, text = "Ingrese los nuevos datos de la cobranza a modificar", justify=tk.CENTER).grid(row=0, column=0, pady=5,padx=5)
            

            cuadro_ingreso = tk.Frame(menu_cobrar)
            cuadro_ingreso.grid(row=1, column=0, pady=10,padx=10)
            Label(cuadro_ingreso, text = "Tiempo Ingreso",  anchor="w").grid(row=0, column=0, padx=5)
            fecha_ingreso = DateEntry(cuadro_ingreso, date_pattern='yyyy-mm-dd', width=12, background='white', foreground='white', borderwidth=2)
            fecha_ingreso.grid(row=1, column=0,padx=5)
            hora_ingreso = Entry(cuadro_ingreso, width=2, justify="center")
            hora_ingreso.grid(row=1, column=1, padx=0)
            hora_ingreso.insert(0, "00")
            Label(cuadro_ingreso, text=":").grid(row=1, column=2, padx=0)
            minuto_ingreso = Entry(cuadro_ingreso, width=2, justify="center")
            minuto_ingreso.grid(row=1, column=3, padx=0)
            minuto_ingreso.insert(0, "00")
            Label(cuadro_ingreso, text=":").grid(row=1, column=4, padx=0)
            segundo_ingreso = Entry(cuadro_ingreso, width=2, justify="center")
            segundo_ingreso.grid(row=1, column=6, padx=0)
            segundo_ingreso.insert(0, "00")
            

            cuadro_egreso = tk.Frame(menu_cobrar)
            cuadro_egreso.grid(row=2, column=0, pady=10,padx=10)
            Label(cuadro_egreso, text = "Tiempo Egreso",  anchor="w").grid(row=0, column=0, padx=5)
            fecha_egreso = DateEntry(cuadro_egreso, date_pattern='yyyy-mm-dd', width=12, background='white', foreground='white', borderwidth=2)
            fecha_egreso.grid(row=1, column=0,padx=5)
            hora_egreso = Entry(cuadro_egreso, width=2, justify="center")
            hora_egreso.grid(row=1, column=1, padx=0)
            hora_egreso.insert(0, "00")
            Label(cuadro_egreso, text=":").grid(row=1, column=2, padx=0)
            minuto_egreso = Entry(cuadro_egreso, width=2, justify="center")
            minuto_egreso.grid(row=1, column=3, padx=0)
            minuto_egreso.insert(0, "00")
            Label(cuadro_egreso, text=":").grid(row=1, column=4, padx=0)
            segundo_egreso = Entry(cuadro_egreso, width=2, justify="center")
            segundo_egreso.grid(row=1, column=6, padx=0)
            segundo_egreso.insert(0, "00")

            cuadro_datos  = tk.Frame(menu_cobrar)
            cuadro_datos.grid(row=3, column=0, pady=10,padx=10)
            # Crear la variable para el Checkbutton
            check_reserva = tk.BooleanVar()
            check_reserva.set(False)
            checkbutton = tk.Checkbutton(cuadro_datos, text="Reserva", variable=check_reserva)
            checkbutton.grid(row=1, column=0, padx=0)

            cuadro_botones = tk.Frame(menu_cobrar)
            cuadro_botones.grid(row=5,column=0,columnspan=3)
            Button(cuadro_botones, text = "OK", width = 10, height = 1, command = confirmar).pack(side=tk.LEFT, padx=10,pady=10)
            Button(cuadro_botones, text = "Cancel", width = 10, height = 1, command = cancelar).pack(side=tk.LEFT, padx=10,pady=10)
        else:
            messagebox.showwarning("No encontrado",f"No se encontro cobranza de ID {id_cobranza}")

    def pagar():
        id_cobranza = simpledialog.askstring("Pagar Cobranza", "ID de la cobranza a pagar:", parent=menu)
        pago_correcto = True
        if id_cobranza is None:
            return
        cobranza = consultar_cobranza_por_id(id_cobranza)
        #pago_correcto = cobrar_estacionamiento(cobranza[2]) # Descomentar para trabajar con el otro modulo de cobranzas
        if(cobranza and cobranza[6] == 'Sin pagar' and cobranza[2] is not None and pago_correcto):
            pagar_cobranza(id_cobranza)
            limpiar_tabla()
            buscar_todos_disponibles()
        else:
            messagebox.showwarning("Error",f"Pago incorrecto o cobranza inexistente.")

    #Modificacion de cobranza
    def modificar():
        def confirmar():
            modificar_cobranza(id_cobranza,monto.get(), moneda.get(), id_empleado_logueado)
            limpiar_tabla()
            buscar_todos_disponibles()
            menu_modificar.destroy()
        def cancelar():
            menu_modificar.destroy()
        
        if permisos_empleado == 0:
            messagebox.showwarning("Acceso Denegado",f"No tiene permisos suficientes para realizar esta accion.")
            return
        # ----- Comienzo ------
        id_cobranza = simpledialog.askstring("Modificar Cobranza", "ID de la cobranza a modificar:", parent=menu)
        if id_cobranza is None:
            return
        cobranza = consultar_cobranza_por_id(id_cobranza)
        
        if(cobranza):
            menu_modificar = Toplevel(menu)
            menu_modificar.title("Modificar Cobranza")
            menu_modificar.geometry("300x200")
            centrar_ventana(menu_modificar)
            Label(menu_modificar, text = "Ingrese los nuevos datos de la cobranza a modificar", justify=tk.CENTER).grid(row=0, column=0, columnspan=3, pady=5,padx=5)
            
            monto = StringVar()
            moneda = StringVar()
            empleado = StringVar()

            Label(menu_modificar, text="Antiguo").grid(row=1, column=1,pady=5)
            Label(menu_modificar, text="Nuevo   ").grid(row=1, column=2,pady=5)


            Label(menu_modificar, text="Monto:").grid(row=2, column=0, sticky=tk.E,pady=5,padx=5)
            Label(menu_modificar, text=f"{cobranza[2]}").grid(row=2, column=1,pady=5,padx=5)
            Label(menu_modificar, text="Moneda:").grid(row=3, column=0, sticky=tk.E,pady=5,padx=5)
            Label(menu_modificar, text=f"{cobranza[3]}").grid(row=3, column=1,pady=5,padx=5)

            nuevo_monto = Entry(menu_modificar, textvariable=monto)
            nuevo_monto.grid(row=2, column=2,sticky=tk.W)
            nueva_moneda = Entry(menu_modificar, textvariable=moneda)
            nueva_moneda.grid(row=3, column=2,sticky=tk.W)

            cuadro_botones = tk.Frame(menu_modificar)
            cuadro_botones.grid(row=5,column=0,columnspan=3)
            Button(cuadro_botones, text = "OK", width = 10, height = 1, command = confirmar).pack(side=tk.LEFT, padx=10,pady=10)
            Button(cuadro_botones, text = "Cancel", width = 10, height = 1, command = cancelar).pack(side=tk.LEFT, padx=10,pady=10)
        else:
            messagebox.showwarning("No encontrado",f"No se encontro cobranza de ID {id_cobranza}")

    #Para utilizar con click-derecho y selection (NO IMPLEMENTADO)
    def eliminar_seleccion():
        seleccion = tabla.selection()
        for cobranza in seleccion:
            tabla.delete(cobranza)

    #Baja Cobranza
    def eliminar_por_ID():
        #Para confirmar la eliminacion
        def respuesta_eliminacion(respuesta):
            if respuesta == "Si":
                baja_cobranza(id_cobranza)
                messagebox.showinfo("Eliminado", "El elemento ha sido eliminado.")
            ventana_confirmacion.destroy()
            limpiar_tabla()
            buscar_todos_disponibles()
                
        # ----- Comienzo ------
        id_cobranza = simpledialog.askstring("Eliminar Cobranza", "ID de la cobranza a eliminar:",parent=menu)
        if id_cobranza is None:
            return
        cobranza = consultar_cobranza_por_id(id_cobranza)
        # Crear la ventana emergente Toplevel SOLO SI existe la cobranza a eliminar
        if(cobranza):
            #Ventana emergente
            ventana_confirmacion = tk.Toplevel(menu)
            ventana_confirmacion.geometry("500x150")
            centrar_ventana(ventana_confirmacion)

            ventana_confirmacion.title("Confirmar Eliminación")

            # Botones y texto
            cuadro_botones = tk.Frame(ventana_confirmacion)
            cuadro_botones.pack(pady=10)
        
            mensaje = f"¿Estás seguro de que quieres eliminar el elemento?"
            label = tk.Label(cuadro_botones, text=mensaje, justify=tk.CENTER)
            label.grid(row=0, column=0, columnspan=2, pady=5)
            boton_si = tk.Button(cuadro_botones, text="Si", command=lambda: respuesta_eliminacion("Si"))
            boton_si.grid(row=1, column=0, padx=10, sticky="WE")
            boton_no = tk.Button(cuadro_botones, text="No", command=lambda: respuesta_eliminacion("No"))
            boton_no.grid(row=1, column=1, padx=10, sticky="WE")

            # Elemento a eliminar
            tabla1 = crear_tabla(ventana_confirmacion)
            tabla1.insert("", tk.END, values=cobranza)
        else:
            messagebox.showwarning("No encontrado",f"No se encontro cobranza de ID {id_cobranza}")
        
    # Ventana tkinter
    menu = tk.Tk()
    menu.title("Cobranzas!!!")
    menu.geometry("600x400")
    centrar_ventana(menu)

    Label(menu, text="Gestion Cobranzas",font="Helvetica",justify="center",).pack()

    # Cuadro de busqueda y botones
    cuadro_botones_menu = tk.Frame(menu)
    cuadro_botones_menu.pack(pady=1,padx=10,fill=tk.X)
    cuadro_botones_menu.columnconfigure(0, weight=1)
    cuadro_botones_menu.columnconfigure(1, weight=1)
    cuadro_botones_menu.columnconfigure(2, weight=1)
    cuadro_botones_menu.columnconfigure(3, weight=1)
    cuadro_botones_menu.columnconfigure(4, weight=1)
    
    boton_agregar = tk.Button(cuadro_botones_menu, text="Agregar", command=agregar_cobranza)
    boton_agregar.grid(row=1, column=0, sticky=tk.EW, pady=5, padx=5)
    boton_modificar = tk.Button(cuadro_botones_menu, text="Cobrar", command=cobrar)
    boton_modificar.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
    boton_modificar = tk.Button(cuadro_botones_menu, text="Pagar", command=pagar)
    boton_modificar.grid(row=1, column=2, sticky=tk.EW, pady=5, padx=5)
    boton_modificar = tk.Button(cuadro_botones_menu, text="Modificar", command=modificar)
    boton_modificar.grid(row=1, column=3, sticky=tk.EW, pady=5, padx=5)
    boton_eliminar = tk.Button(cuadro_botones_menu, text="Eliminar", command=eliminar_por_ID)
    boton_eliminar.grid(row=1, column=4, sticky=tk.EW, pady=5, padx=5)

    
    entrada_busqueda = tk.Entry(cuadro_botones_menu)
    entrada_busqueda.grid(row=2, column=0, sticky="WE", columnspan=3, pady=5, padx=5)
    boton_buscar = tk.Button(cuadro_botones_menu, text="Buscar", command=buscar)
    boton_buscar.grid(row=2, column=3, sticky=tk.W, pady=5)
    #Permite la busqueda al apretar la tecla Enter
    entrada_busqueda.bind('<Return>', lambda event: boton_buscar.invoke())

    #Descomentar vvv para busqueda con solo escribir (aunque no tiene mucho sentido)
    #entrada_busqueda.bind('<KeyRelease>', lambda event: boton_buscar.invoke())
    
    #Creacion de la tabla
    cuadro_tabla = tk.Frame(menu)
    cuadro_tabla.pack(pady=1,padx=15,fill=tk.BOTH)
    tabla = crear_tabla(cuadro_tabla)
    menu.after(1,buscar)
    menu.mainloop()

if __name__ == "__main__":
    menu_login()
    conn.close()
