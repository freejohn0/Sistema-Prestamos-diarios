import json
from datetime import datetime

# Cargar datos desde archivo JSON
def cargar_datos():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"clientes": []}

# Guardar datos en archivo JSON
def guardar_datos(datos):
    with open("database.json", "w") as file:
        json.dump(datos, file, indent=4)

# Función para calcular mora
def calcular_mora(dias_atraso, monto_prestamo):
    if dias_atraso <= 0:
        return 0
    tasa_mora = 0.05  # 5% del préstamo original por día de atraso
    return dias_atraso * tasa_mora * monto_prestamo

# Agregar nuevo cliente
def agregar_cliente(datos):
    nombre = input("Nombre del cliente: ")
    telefono = input("Teléfono: ")
    cliente = {
        "nombre": nombre,
        "telefono": telefono,
        "prestamos": []
    }
    datos["clientes"].append(cliente)
    guardar_datos(datos)
    print(f"✅ Cliente {nombre} agregado.")

# Registrar un préstamo
def registrar_prestamo(datos):
    nombre = input("Nombre del cliente: ")
    cliente = next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)
    if not cliente:
        print("❌ Cliente no encontrado.")
        return

    monto = float(input("Monto del préstamo: "))
    plazo_semanas = int(input("Plazo en semanas: "))
    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")

    prestamo = {
        "monto_total": monto,
        "plazo_semanas": plazo_semanas,
        "fecha_inicio": fecha_inicio,
        "pagos": [],
        "renganches": []
    }

    cliente["prestamos"].append(prestamo)
    guardar_datos(datos)
    print(f"✅ Préstamo de ${monto} registrado para {nombre}.")

# Registrar pago
def registrar_pago(datos):
    nombre = input("Nombre del cliente: ").strip()
    cliente = next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)
    if not cliente or not cliente["prestamos"]:
        print("❌ Cliente o préstamo no encontrado.")
        return

    # Mostrar préstamos disponibles
    print("\nPréstamos disponibles:")
    for idx, prestamo in enumerate(cliente["prestamos"]):
        print(f"{idx}. Monto total: ${prestamo['monto_total']} | Pendiente: ${prestamo['monto_total'] - sum(p['monto'] for p in prestamo['pagos'])}")

    # Validar índice del préstamo
    while True:
        try:
            prestamo_index = int(input(f"Índice del préstamo (0 a {len(cliente['prestamos']) - 1}): "))
            if 0 <= prestamo_index < len(cliente["prestamos"]):
                break
            else:
                print(f"❌ Índice inválido. Por favor, elige entre 0 a {len(cliente['prestamos']) - 1}.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")

    monto_pago = float(input("Monto del pago: "))
    fecha_pago = input("Fecha del pago (YYYY-MM-DD): ").strip()

    cliente["prestamos"][prestamo_index]["pagos"].append({
        "monto": monto_pago,
        "fecha": fecha_pago
    })

    guardar_datos(datos)
    print(f"✅ Pago de ${monto_pago} registrado.")

    guardar_datos(datos)
    print(f"✅ Pago de ${monto_pago} registrado.")

    guardar_datos(datos)
    print(f"✅ Pago de ${monto_pago} registrado.")

# Mostrar resumen de hoy
def resumen_diario(datos):
    hoy = datetime.now().strftime("%Y-%m-%d")
    total_pagos = 0
    clientes_deudores = 0

    for cliente in datos["clientes"]:
        for prestamo in cliente["prestamos"]:
            pagos = sum(p["monto"] for p in prestamo["pagos"] if p["fecha"] == hoy)
            total_pagos += pagos
            restante = prestamo["monto_total"] - sum(p["monto"] for p in prestamo["pagos"])
            if restante > 0:
                clientes_deudores += 1

    print(f"\n📅 Resumen del día {hoy}:")
    print(f"💰 Total pagado hoy: ${total_pagos}")
    print(f"👥 Clientes con deudas pendientes: {clientes_deudores}")

# Mostrar estado de cuenta de un cliente
def estado_cuenta(datos):
    nombre = input("Nombre del cliente: ")
    cliente = next((c for c in datos["clientes"] if c["nombre"].lower() == nombre.lower()), None)
    if not cliente:
        print("❌ Cliente no encontrado.")
        return

    print(f"\n👤 Estado de cuenta de {cliente['nombre']}:")
    for idx, prestamo in enumerate(cliente["prestamos"]):
        monto_total = prestamo["monto_total"]
        pagado = sum(p["monto"] for p in prestamo["pagos"])
        restante = monto_total - pagado
        fecha_inicio = datetime.strptime(prestamo["fecha_inicio"], "%Y-%m-%d")
        dias_transcurridos = (datetime.now() - fecha_inicio).days
        semanas_transcurridas = dias_transcurridos // 7
        dias_atraso = max(0, semanas_transcurridas - prestamo["plazo_semanas"])
        mora = calcular_mora(dias_atraso, monto_total)


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
# Menú principal
def menu():
    datos = cargar_datos()
    while True:
        print("\n===== GESTIÓN DE PRÉSTAMOS =====")
        print("1. Agregar cliente")
        print("2. Registrar préstamo")
        print("3. Registrar pago")
        print("4. Estado de cuenta")
        print("5. Resta del pago")
        print("6. Resumen del día")
        print("7. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_cliente(datos)
        elif opcion == "2":
            registrar_prestamo(datos)
        elif opcion == "3":
            registrar_pago (datos)   
        elif opcion == "4":
             estado_cuenta (datos)
        elif opcion == "5":
            resta_pago(datos)
        elif opcion == "6":
            resumen_diario(datos)    
        elif opcion == "7":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu()