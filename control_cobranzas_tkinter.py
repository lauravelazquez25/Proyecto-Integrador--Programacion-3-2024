import sqlite3
import tkinter as tk
from tkinter import END, Button, Entry, Label, StringVar, Toplevel, ttk, simpledialog, messagebox
from datetime import datetime
import os

conn = sqlite3.connect('estacionamiento.db')
cursor = conn.cursor()

def alta_cobranza(matricula,monto, moneda, empleado_id):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO Cobranzas (Matricula, Monto, Moneda, Fecha_Hora, Empleado_ID)
    VALUES (?, ?, ?, ?, ?)
    """, (matricula, monto, moneda, fecha_hora, empleado_id))
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


#Se modificaron las consultas de cobranza para que devuelvan los resultados del fetch, para poder trabajarlos mejor con tkinter

#Consulta todas las cobranzas existentes
def consultar_cobranzas():
    cursor.execute("SELECT * FROM Cobranzas")
    cobranzas = cursor.fetchall()
    return cobranzas

#Consulta una cobranza por la ID
def consultar_cobranza_por_id(cobranza_id):
    cursor.execute('SELECT * FROM cobranzas WHERE id = ?', (cobranza_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"No se encontro ninguna cobranza con ID {cobranza_id}.")


def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def menu_login():
    def login_verify():
        username1 = username_verify.get()
        password1 = password_verify.get()
        username_entry1.delete(0, END)
        password_entry1.delete(0, END)


        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                ventana_login.destroy()
                menu_cobranzas()
            else:
                messagebox.showwarning("Incorrecto","Usuario o contraseña erroneos, intentelo denuevo.")

        else:
            messagebox.showwarning("Incorrecto","Usuario o contraseña erroneos, intentelo denuevo.")


    
    ventana_login = tk.Tk()
    ventana_login.title("Control Cobranzas v1.0")
    ventana_login.geometry("300x250")
    centrar_ventana(ventana_login)
    Label(ventana_login, text = "Por favor ingrese sus datos para continuar.").pack()
    Label(ventana_login, text = "").pack()


    global username_verify
    global password_verify
    
    username_verify = StringVar()
    password_verify = StringVar()


    global username_entry1
    global password_entry1
    
    Label(ventana_login, text = "Usuario * ").pack()
    username_entry1 = Entry(ventana_login, textvariable = username_verify)
    username_entry1.pack()
    Label(ventana_login, text = "").pack()
    Label(ventana_login, text = "Contraseña * ").pack()
    password_entry1 = Entry(ventana_login, textvariable = password_verify)
    password_entry1.pack()
    Label(ventana_login, text = "").pack()
    Button(ventana_login, text = "Iniciar Sesion", width = 10, height = 1, command = login_verify).pack()

    password_entry1.bind('<Return>', lambda event: login_verify())  

    ventana_login.mainloop()
        

# Menu de cobranzas en Tkinter
def menu_cobranzas():

    # Crea una tabla de la base de datos
    def crear_tabla(ventana):
        columnas = ("id", "matricula", "monto", "moneda", "fecha", "empleado")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

        
        tabla.heading("id", text="ID")
        tabla.heading("matricula", text="Matricula")
        tabla.heading("monto", text="Monto")
        tabla.heading("moneda", text="Moneda")
        tabla.heading("fecha", text="Fecha")
        tabla.heading("empleado", text="ID Empleado")

        tabla.column("id", width=10)
        tabla.column("matricula", width=25)
        tabla.column("monto", width=20)
        tabla.column("moneda", width=15)
        tabla.column("fecha", width=50)
        tabla.column("empleado", width=50)
        tabla.pack(fill=tk.BOTH, expand=True)
        return tabla
    

    #Limpia la tabla // Utilizado para las busquedas principalmente
    def limpiar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

    
    # TEST
    def test():
        print("TODO OK")

    # Busca y muestra las cobranzas en la tabla de tkinter
    #       Muestra:
    #               1 resultado en caso de que se haya encontrado
    #               0 resultados en caso de que no se haya encontrado
    #               Todos los resultados si no se especifico una ID
    def buscar():
        limpiar_tabla()
        id_cobranza = entrada_busqueda.get().lower()
        if (id_cobranza):
            cobranza = consultar_cobranza_por_id(id_cobranza)
            if cobranza:
                tabla.insert("", tk.END, values=cobranza)
        else:
            buscar_todos()
    def buscar_todos():
        cobranzas = consultar_cobranzas()
        for cobranza in cobranzas:
            tabla.insert("", tk.END, values=cobranza)


    #Alta cobranza
    def agregar_cobranza():
        def confirmar():
            alta_cobranza(matricula.get(),monto.get(), moneda.get(), empleado.get())
            limpiar_tabla()
            buscar_todos()
            menu_agregar.destroy()
        def cancelar():
            menu_agregar.destroy()

        # ----- Comienzo ------
        menu_agregar = Toplevel(menu)
        menu_agregar.title("Nueva Cobranza")
        menu_agregar.geometry("300x200")
        menu_agregar.columnconfigure(0, weight=1)
        menu_agregar.columnconfigure(1, weight=1)
        centrar_ventana(menu_agregar)
        Label(menu_agregar, text = "Ingrese los datos de la nueva cobranza", justify=tk.CENTER).grid(row=0, column=0, columnspan=2, pady=5,padx=5)
        
        matricula = StringVar()
        monto = StringVar()
        moneda = StringVar()
        empleado = StringVar()

        Label(menu_agregar, text="Matricula:").grid(row=1, column=0, sticky=tk.E,pady=5,padx=5)
        Label(menu_agregar, text="Monto:").grid(row=2, column=0, sticky=tk.E,pady=5,padx=5)
        Label(menu_agregar, text="Moneda:").grid(row=3, column=0, sticky=tk.E,pady=5,padx=5)
        Label(menu_agregar, text="Empleado:").grid(row=4, column=0, sticky=tk.E,pady=5,padx=5)

        nueva_matricula = Entry(menu_agregar, textvariable=matricula)
        nueva_matricula.grid(row=1, column=1,sticky=tk.W)
        nuevo_monto = Entry(menu_agregar, textvariable=monto)
        nuevo_monto.grid(row=2, column=1,sticky=tk.W)
        nueva_moneda = Entry(menu_agregar, textvariable=moneda)
        nueva_moneda.grid(row=3, column=1,sticky=tk.W)
        nuevo_empleado = Entry(menu_agregar, textvariable=empleado)
        nuevo_empleado.grid(row=4, column=1,sticky=tk.W)

        
        cuadro_botones = tk.Frame(menu_agregar)
        cuadro_botones.grid(row=5,column=0,columnspan=3)
        Button(cuadro_botones, text = "OK", width = 10, height = 1, command = confirmar).pack(side=tk.LEFT, padx=10,pady=10)
        Button(cuadro_botones, text = "Cancel", width = 10, height = 1, command = cancelar).pack(side=tk.LEFT, padx=10,pady=10)
        
    #Modificacion de cobranza
    def modificar():
        def confirmar():
            modificar_cobranza(id_cobranza,monto.get(), moneda.get(), empleado.get())
            limpiar_tabla()
            buscar_todos()
            menu_modificar.destroy()
        def cancelar():
            menu_modificar.destroy()
        

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
            Label(menu_modificar, text="Empleado:").grid(row=4, column=0, sticky=tk.E,pady=5,padx=5)
            Label(menu_modificar, text=f"{cobranza[5]}").grid(row=4, column=1,pady=5,padx=5)

            nuevo_monto = Entry(menu_modificar, textvariable=monto)
            nuevo_monto.grid(row=2, column=2,sticky=tk.W)
            nueva_moneda = Entry(menu_modificar, textvariable=moneda)
            nueva_moneda.grid(row=3, column=2,sticky=tk.W)
            nuevo_empleado = Entry(menu_modificar, textvariable=empleado)
            nuevo_empleado.grid(row=4, column=2,sticky=tk.W)

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
            buscar_todos()
                
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
    cuadro_busqueda = tk.Frame(menu)
    cuadro_busqueda.pack(pady=1,padx=10,fill=tk.X)
    cuadro_busqueda.columnconfigure(0, weight=1)
    cuadro_busqueda.columnconfigure(1, weight=2)
    cuadro_busqueda.columnconfigure(2, weight=2)
    
    boton_agregar = tk.Button(cuadro_busqueda, text="Agregar", command=agregar_cobranza)
    boton_agregar.grid(row=1, column=0, sticky=tk.EW, pady=5, padx=5)
    boton_modificar = tk.Button(cuadro_busqueda, text="Modificar", command=modificar)
    boton_modificar.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
    boton_eliminar = tk.Button(cuadro_busqueda, text="Eliminar", command=eliminar_por_ID)
    boton_eliminar.grid(row=1, column=2, sticky=tk.EW, pady=5, padx=5)

    boton_buscar = tk.Button(cuadro_busqueda, text="Buscar", command=buscar)
    boton_buscar.grid(row=2, column=1, sticky=tk.W, pady=5)
    entrada_busqueda = tk.Entry(cuadro_busqueda)
    entrada_busqueda.grid(row=2, column=0, sticky="WE", pady=5, padx=5)

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
    #menu_cobranzas()
    conn.close()
