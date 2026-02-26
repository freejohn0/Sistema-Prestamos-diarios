import tkinter as tk
from tkinter import messagebox
from main import menu  # Importamos tu lógica existente


def iniciar_app_consola():
    menu()  # Esta es la función del menú principal de tu app


def mostrar_acerca_de():
    messagebox.showinfo("Acerca de", "App de gestión de préstamos\nVersión 1.0")


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Préstamos")
ventana.geometry("400x300")

# Estilo básico
titulo = tk.Label(ventana, text="GESTIÓN DE PRÉSTAMOS", font=("Arial", 16, "bold"))
titulo.pack(pady=20)

# Botones
btn_agregar_cliente = tk.Button(ventana, text="1. Agregar cliente", width=30)
btn_registrar_prestamo = tk.Button(ventana, text="2. Registrar préstamo", width=30)
btn_registrar_pago = tk.Button(ventana, text="3. Registrar pago", width=30)
btn_resumen_diario = tk.Button(ventana, text="4. Resumen del día", width=30)
btn_estado_cuenta = tk.Button(ventana, text="5. Estado de cuenta", width=30)
btn_salir = tk.Button(ventana, text="6. Salir", command=ventana.destroy, width=30)

# Colocar botones
btn_agregar_cliente.pack(pady=5)
btn_registrar_prestamo.pack(pady=5)
btn_registrar_pago.pack(pady=5)
btn_resumen_diario.pack(pady=5)
btn_estado_cuenta.pack(pady=5)
btn_salir.pack(pady=5)

# Menú superior
menubar = tk.Menu(ventana)
ventana.config(menu=menubar)
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ayuda", menu=help_menu)
help_menu.add_command(label="Acerca de", command=mostrar_acerca_de)

# Iniciar bucle de la ventana
ventana.mainloop()