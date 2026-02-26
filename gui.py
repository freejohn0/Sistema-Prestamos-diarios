import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import json

# Funciones del sistema principal
def cargar_datos():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"clientes": []}

def guardar_datos(datos):
    with open("database.json", "w") as file:
        json.dump(datos, file, indent=4)

def calcular_mora(dias_atraso, monto_prestamo):
    if dias_atraso <= 0:
        return 0
    tasa_mora = 0.05  # 5% del préstamo original por día de atraso
    return dias_atraso * tasa_mora * monto_prestamo

def resta_pago(datos, nombre, indice_prestamo=None):
    cliente = next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)
    if not cliente:
        return {"error": "Cliente no encontrado"}

    if indice_prestamo is None or indice_prestamo >= len(cliente["prestamos"]) or indice_prestamo < 0:
        return {"error": "Índice inválido"}

    prestamo = cliente["prestamos"][indice_prestamo]

    monto_total = prestamo["monto_total"]
    pagado = sum(p["monto"] for p in prestamo["pagos"])
    restante = monto_total - pagado

    fecha_inicio = datetime.strptime(prestamo["fecha_inicio"], "%Y-%m-%d")
    dias_transcurridos = (datetime.now() - fecha_inicio).days
    semanas_transcurridas = dias_transcurridos // 7 + 1
    pago_semanal = monto_total / prestamo["plazo_semanas"]

    deberia_haber_pagado = pago_semanal * semanas_transcurridas
    faltante_segun_plazo = max(0, deberia_haber_pagado - pagado)

    return {
        "cliente": nombre,
        "prestamo_idx": indice_prestamo,
        "monto_total": monto_total,
        "pagado": pagado,
        "restante": restante,
        "deberia_haber_pagado": deberia_haber_pagado,
        "faltante_segun_plazo": faltante_segun_plazo
    }

class GestionPrestamos:
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Gestión de Préstamos")
        self.ventana_principal.geometry("500x600")
        self.ventana_principal.configure(bg="#f0f0f0")
        
        # Configurar estilo
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        # Título principal
        titulo = tk.Label(
            self.ventana_principal, 
            text="GESTIÓN DE PRÉSTAMOS", 
            font=("Arial", 18, "bold"), 
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=20)
        
        # Frame para botones
        frame_botones = tk.Frame(self.ventana_principal, bg="#f0f0f0")
        frame_botones.pack(pady=10)
        
        # Crear botones
        botones = [
            ("Agregar Cliente", self.agregar_cliente_gui, "#27ae60"),
            ("Registrar Préstamo", self.registrar_prestamo_gui, "#3498db"),
            ("Registrar Pago", self.registrar_pago_gui, "#e67e22"),
            ("Estado de Cuenta", self.estado_cuenta_gui, "#9b59b6"),
            ("Resta del Pago", self.resta_pago_gui, "#1abc9c"),
            ("Resumen del Día", self.resumen_diario_gui, "#f39c12"),
            ("Ver Todos los Clientes", self.ver_todos_clientes, "#34495e"),
            ("Salir", self.ventana_principal.quit, "#e74c3c")
        ]
        
        for texto, comando, color in botones:
            btn = tk.Button(
                frame_botones,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                padx=25,
                pady=12,
                width=20,
                cursor="hand2"
            )
            btn.pack(pady=5)
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.oscurecer_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

    def oscurecer_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) * 0.8
        g = int(hex_color[2:4], 16) * 0.8
        b = int(hex_color[4:6], 16) * 0.8
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'

    def crear_ventana_datos(self, titulo, contenido, ancho=600, alto=500):
        """Crear una ventana para mostrar datos"""
        ventana = tk.Toplevel(self.ventana_principal)
        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.configure(bg="white")
        ventana.resizable(True, True)
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(ventana, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_label = tk.Label(
            main_frame, 
            text=titulo, 
            font=("Arial", 16, "bold"), 
            bg="white",
            fg="#2c3e50"
        )
        titulo_label.pack(pady=(0, 15))
        
        # Frame con scrollbar para el contenido
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Texto del contenido
        texto_widget = tk.Text(
            scrollable_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            padx=15,
            pady=15,
            relief="flat",
            borderwidth=1
        )
        texto_widget.insert("1.0", contenido)
        texto_widget.config(state=tk.DISABLED)
        texto_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        btn_cerrar = tk.Button(
            main_frame,
            text="Cerrar",
            command=ventana.destroy,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        btn_cerrar.pack(pady=10)
        
        # Centrar ventana
        ventana.transient(self.ventana_principal)
        ventana.grab_set()

    def seleccionar_cliente(self, datos):
        """Pide el nombre del cliente y devuelve su objeto"""
        nombre = simpledialog.askstring("Cliente", "Nombre del cliente:")
        if not nombre:
            return None
        nombre = nombre.strip()
        return next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)

    def agregar_cliente_gui(self):
        nombre = simpledialog.askstring("Agregar Cliente", "Nombre del cliente:")
        telefono = simpledialog.askstring("Agregar Cliente", "Teléfono:")
        if nombre and telefono:
            datos = cargar_datos()
            cliente = {
                "nombre": nombre.strip(),
                "telefono": telefono.strip(),
                "prestamos": []
            }
            datos["clientes"].append(cliente)
            guardar_datos(datos)
            messagebox.showinfo("Éxito", f"✅ Cliente '{nombre}' agregado correctamente.")

    def registrar_prestamo_gui(self):
        datos = cargar_datos()
        cliente = self.seleccionar_cliente(datos)
        if not cliente:
            messagebox.showerror("Error", "❌ Cliente no encontrado.")
            return

        monto = simpledialog.askfloat("Registrar Préstamo", "Monto del préstamo:")
        plazo_semanas = simpledialog.askinteger("Registrar Préstamo", "Plazo en semanas:")
        fecha_inicio = simpledialog.askstring("Registrar Préstamo", "Fecha de inicio (YYYY-MM-DD):")

        if None in [monto, plazo_semanas, fecha_inicio]:
            return

        prestamo = {
            "monto_total": monto,
            "plazo_semanas": plazo_semanas,
            "fecha_inicio": fecha_inicio.strip(),
            "pagos": []
        }

        cliente["prestamos"].append(prestamo)
        guardar_datos(datos)
        messagebox.showinfo("Éxito", f"✅ Préstamo de ${monto} registrado para {cliente['nombre']}.")

    def registrar_pago_gui(self):
        datos = cargar_datos()
        cliente = self.seleccionar_cliente(datos)
        if not cliente or not cliente["prestamos"]:
            messagebox.showerror("Error", "❌ Cliente o préstamo no encontrado.")
            return

        # Mostrar préstamos en una ventana
        prestamos_info = ""
        for i, p in enumerate(cliente["prestamos"]):
            pagado = sum(pago["monto"] for pago in p["pagos"])
            pendiente = p["monto_total"] - pagado
            prestamos_info += f"{i}. Monto total: ${p['monto_total']} | Pagado: ${pagado} | Pendiente: ${pendiente}\n"

        self.crear_ventana_datos(f"Préstamos de {cliente['nombre']}", prestamos_info, 500, 300)

        idx = simpledialog.askinteger("Registrar Pago", f"Selecciona el índice del préstamo (0-{len(cliente['prestamos'])-1}):")

        if idx is None or idx < 0 or idx >= len(cliente["prestamos"]):
            messagebox.showerror("Error", "❌ Índice inválido.")
            return

        monto_pago = simpledialog.askfloat("Registrar Pago", "Monto del pago:")
        fecha_pago = simpledialog.askstring("Registrar Pago", "Fecha del pago (YYYY-MM-DD):")

        if None in [monto_pago, fecha_pago]:
            return

        cliente["prestamos"][idx]["pagos"].append({
            "monto": monto_pago,
            "fecha": fecha_pago.strip()
        })

        guardar_datos(datos)
        messagebox.showinfo("Éxito", f"✅ Pago de ${monto_pago} registrado correctamente.")

    def estado_cuenta_gui(self):
        datos = cargar_datos()
        cliente = self.seleccionar_cliente(datos)
        if not cliente:
            messagebox.showerror("Error", "❌ Cliente no encontrado.")
            return

        contenido = f"👤 ESTADO DE CUENTA - {cliente['nombre'].upper()}\n"
        contenido += f"📞 Teléfono: {cliente.get('telefono', 'No registrado')}\n"
        contenido += "=" * 60 + "\n\n"

        if not cliente["prestamos"]:
            contenido += "No hay préstamos registrados para este cliente."
        else:
            for idx, prestamo in enumerate(cliente["prestamos"]):
                monto_total = prestamo["monto_total"]
                pagado = sum(p["monto"] for p in prestamo["pagos"])
                restante = monto_total - pagado
                
                # Calcular información de plazo
                fecha_inicio = datetime.strptime(prestamo["fecha_inicio"], "%Y-%m-%d")
                dias_transcurridos = (datetime.now() - fecha_inicio).days
                semanas_transcurridas = dias_transcurridos // 7
                
                contenido += f"💰 PRÉSTAMO #{idx + 1}\n"
                contenido += f"   Monto total: ${monto_total:,.2f}\n"
                contenido += f"   Plazo: {prestamo['plazo_semanas']} semanas\n"
                contenido += f"   Fecha inicio: {prestamo['fecha_inicio']}\n"
                contenido += f"   Pagado: ${pagado:,.2f}\n"
                contenido += f"   Pendiente: ${restante:,.2f}\n"
                contenido += f"   Semanas transcurridas: {semanas_transcurridas}\n"
                contenido += f"   Días transcurridos: {dias_transcurridos}\n"
                
                if prestamo["pagos"]:
                    contenido += f"\n   📋 HISTORIAL DE PAGOS:\n"
                    for i, pago in enumerate(prestamo["pagos"], 1):
                        contenido += f"      {i}. ${pago['monto']:,.2f} - {pago['fecha']}\n"
                
                contenido += "\n" + "-" * 50 + "\n\n"

        self.crear_ventana_datos(f"Estado de Cuenta - {cliente['nombre']}", contenido, 700, 600)

    def resta_pago_gui(self):
        datos = cargar_datos()
        nombre = simpledialog.askstring("Cliente", "Nombre del cliente:")
        if not nombre:
            return

        cliente = next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)
        if not cliente:
            messagebox.showerror("Error", "❌ Cliente no encontrado.")
            return

        if not cliente["prestamos"]:
            messagebox.showinfo("Información", "Este cliente no tiene préstamos registrados.")
            return

        # Los préstamos disponibles
        prestamos_info = f"PRÉSTAMOS DISPONIBLES PARA {cliente['nombre'].upper()}:\n\n"
        for i, p in enumerate(cliente["prestamos"]):
            pagado = sum(pago["monto"] for pago in p["pagos"])
            pendiente = p["monto_total"] - pagado
            prestamos_info += f"{i}. Monto total: ${p['monto_total']:,.2f} | Pendiente: ${pendiente:,.2f}\n"

        self.crear_ventana_datos("Seleccionar Préstamo", prestamos_info, 500, 300)

        idx = simpledialog.askinteger("Seleccionar préstamo", f"Selecciona un préstamo (0-{len(cliente['prestamos'])-1}):")

        if idx is None or idx < 0 or idx >= len(cliente["prestamos"]):
            messagebox.showerror("Error", "❌ Índice inválido.")
            return

        resultado = resta_pago(datos, nombre, idx)

        contenido = f"📊 ANÁLISIS DE PAGO - {resultado['cliente'].upper()}\n"
        contenido += "=" * 50 + "\n\n"
        contenido += f"💰 PRÉSTAMO #{idx + 1}:\n"
        contenido += f"   Monto total: ${resultado['monto_total']:,.2f}\n"
        contenido += f"   Pagado hasta ahora: ${resultado['pagado']:,.2f}\n"
        contenido += f"   Restante: ${resultado['restante']:,.2f}\n\n"
        contenido += f"📈 ANÁLISIS DE CUMPLIMIENTO:\n"
        contenido += f"   Debería haber pagado: ${resultado['deberia_haber_pagado']:,.2f}\n"
        contenido += f"   Faltante según plazo: ${resultado['faltante_segun_plazo']:,.2f}\n\n"
        
        if resultado['faltante_segun_plazo'] > 0:
            contenido += f"⚠️  ESTADO: ATRASADO\n"
            contenido += f"   Debe pagar ${resultado['faltante_segun_plazo']:,.2f} para estar al día\n"
        else:
            contenido += f"✅ ESTADO: AL DÍA\n"

        self.crear_ventana_datos("Análisis de Pago", contenido, 600, 400)

    def resumen_diario_gui(self):
        datos = cargar_datos()
        hoy = datetime.now().strftime("%Y-%m-%d")
        total_pagos = 0
        clientes_deudores = 0
        pagos_hoy = []

        for cliente in datos["clientes"]:
            for prestamo in cliente["prestamos"]:
                # Pagos del dia
                pagos_cliente_hoy = [p for p in prestamo["pagos"] if p["fecha"] == hoy]
                for pago in pagos_cliente_hoy:
                    total_pagos += pago["monto"]
                    pagos_hoy.append({
                        "cliente": cliente["nombre"],
                        "monto": pago["monto"],
                        "fecha": pago["fecha"]
                    })
                
                # Deudas pendientes
                restante = prestamo["monto_total"] - sum(p["monto"] for p in prestamo["pagos"])
                if restante > 0:
                    clientes_deudores += 1

        contenido = f"📅 RESUMEN DEL DÍA - {hoy}\n"
        contenido += "=" * 50 + "\n\n"
        contenido += f"💰 Total pagado hoy: ${total_pagos:,.2f}\n"
        contenido += f"👥 Clientes con deudas pendientes: {clientes_deudores}\n"
        contenido += f"📝 Número de pagos recibidos: {len(pagos_hoy)}\n\n"
        
        if pagos_hoy:
            contenido += "📋 DETALLE DE PAGOS DEL DÍA:\n"
            contenido += "-" * 40 + "\n"
            for pago in pagos_hoy:
                contenido += f"• {pago['cliente']}: ${pago['monto']:,.2f}\n"
        else:
            contenido += "No se registraron pagos el día de hoy.\n"

        self.crear_ventana_datos("Resumen Diario", contenido, 600, 500)

    def ver_todos_clientes(self):
        datos = cargar_datos()
        
        if not datos["clientes"]:
            messagebox.showinfo("Información", "No hay clientes registrados.")
            return

        contenido = f"👥 TODOS LOS CLIENTES REGISTRADOS\n"
        contenido += f"Total de clientes: {len(datos['clientes'])}\n"
        contenido += "=" * 60 + "\n\n"

        for idx, cliente in enumerate(datos["clientes"], 1):
            contenido += f"{idx}. 👤 {cliente['nombre'].upper()}\n"
            contenido += f"   📞 Teléfono: {cliente.get('telefono', 'No registrado')}\n"
            contenido += f"   💰 Préstamos activos: {len(cliente['prestamos'])}\n"
            
            # Calculo totales
            total_prestado = sum(p["monto_total"] for p in cliente["prestamos"])
            total_pagado = sum(sum(pago["monto"] for pago in p["pagos"]) for p in cliente["prestamos"])
            total_pendiente = total_prestado - total_pagado
            
            contenido += f"   💸 Total prestado: ${total_prestado:,.2f}\n"
            contenido += f"   ✅ Total pagado: ${total_pagado:,.2f}\n"
            contenido += f"   ⏳ Total pendiente: ${total_pendiente:,.2f}\n"
            contenido += "\n" + "-" * 50 + "\n\n"

        self.crear_ventana_datos("Todos los Clientes", contenido, 700, 600)

    def ejecutar(self):
        self.ventana_principal.mainloop()

# Se la aplicación
if __name__ == "__main__":
    app = GestionPrestamos()
    app.ejecutar()