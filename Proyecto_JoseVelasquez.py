# ============================================
# PROYECTO UNIDAD I - PROGRAMACIÓN III
# Estudiante: [Jose Luis Velasquez Millan]
# Cédula: V-[27650743]
# Enunciado: #[2 - SISTEMA DE INVENTARIO DE PRODUCTOS]
# Fecha: [27/10/2026]
# ============================================

#las variables globales
ultimos_2_digitos_cedula = 43
Mi_inicial = "J"
Stock_minimo = ultimos_2_digitos_cedula % 10

total_ventas = 0.0
ventas_realizadas = 0
hay_ventas = False

inventario = []
historial_ventas = []

#clase principal
class Producto:
    def __init__(self, nombre, precio, cantidad, categoria):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria

    #metodo de total de producto
    def calcular_total(self):
        return self.precio * self.cantidad 

    #metodo para saber si el stock es bajo
    def stock_critico(self):
        return self.cantidad < Stock_minimo

    #metodo para mostrar los datos del producto
    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Precio: ${self.precio:.2f} | "
                f"Cantidad: {self.cantidad} | Categoría: {self.categoria}")

#aqui empiezan las funciones 

#Oroductos que estaran desde un inicio cuando se inicie el programa
def cargar_producto():
    inventario.append(Producto("Playstaion 5", 850, 20, "Consola"))
    inventario.append(Producto("GTA 6", 100, 50, "Juego Digital"))
    inventario.append(Producto("Monopolio", 60, 2, "Juego de mesa"))
    inventario.append(Producto("Joystick", 25, 10, "Repuesto"))
    
#decirle al usuairio que coloque un numero
def pedir_numero(mensaje, tipo=float):
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida, intenta de nuevo.")

#buscar el producto por el nombre
def buscar_producto(nombre, inventario):
    for producto in inventario:
        if producto.nombre.lower() == nombre.lower():
            return producto
    return None

#metodo para agregar un nuevo producto
def agregar_producto(inventario):
    nombre = input("Ingrese el nombre del producto: ").strip()
    if not nombre or len(nombre) < 2:
        print("El nombre debe tener al menos 2 caracteres.")
        return

    existe = buscar_producto(nombre, inventario)

    #metodo para indicar que hacer si el producto existe o no
    if existe:
        cantidad = pedir_numero("Ya existe este producto. Ingrese la cantidad a sumar: ", int)
        existe.cantidad += cantidad
        print(f"Stock actualizado: {existe.nombre} ahora tiene {existe.cantidad}.")
    else:
        precio = pedir_numero("Precio: ", float)
        cantidad = pedir_numero("Cantidad: ", int)
        categoria = input("Categoría: ").strip()
        inventario.append(Producto(nombre, precio, cantidad, categoria))
        print("Producto agregado correctamente.")

#metodo para indicar como venmder (el "global" esta alli porque hace referencia a lo que esta fuera de la clase)
def vender_producto(inventario):
    global ventas_realizadas, hay_ventas, total_ventas

    if not inventario:
        print("No hay productos en el inventario.")
        return

    mostrar_todos()
    nombre = input("¿Qué producto deseas vender? ").strip()
    producto = buscar_producto(nombre, inventario)

    if producto is None:
        print("Producto no encontrado.")
        return

    cantidad = pedir_numero("Cantidad a vender: ", int)

    if cantidad <= 0 or cantidad > producto.cantidad:
        print(f"Cantidad inválida. Disponible: {producto.cantidad}.")
        return

    #accion que actualiza el stock 
    producto.cantidad -= cantidad
    total_venta = producto.precio * cantidad
    print(f"Venta realizada: {cantidad} x {producto.nombre} = ${total_venta:.2f}")

    #aqui es la accion donde se registra la venta 
    historial_ventas.append(f"{cantidad} x {producto.nombre} = ${total_venta:.2f}")
    ventas_realizadas += 1
    total_ventas += total_venta
    hay_ventas = True

    #funcion para avisar cuando se necesita reestablecer el stock
    if producto.cantidad == 0:
        print(f"¡{producto.nombre} se agotó!")
    elif producto.stock_critico() and producto.cantidad > 0:
        print(f"¡Alerta! {producto.nombre} quedo con stock bajo ({producto.cantidad}).")

#metodo para mostrar que hay en el inventario 
def mostrar_todos():
    if not inventario:
        print("No hay productos en el inventario.")
        return
    print("\n---Productos en inventario: ---")
    for producto in inventario:
        producto.mostrar_info()

#mostrar lo que esta bajo de stock (el "hay" lo coloque para saber que si su valor cambia quiere decir que no hay stock critico)
def mostrar_stock_bajo(inventario):
    print(f"\n-- STOCK BAJO (cantidad < {Stock_minimo}) --")
    hay = False
    for producto in inventario:
        if producto.stock_critico():
            producto.mostrar_info()
            hay = True
    if not hay:
        print("No hay productos con stock bajo.")

#el metodo de cilo for (recordar que el for externo recorre los productos, mientras que el interno suma la cantidad)
def valor_total_inventario():
    total = 0
    for producto in inventario:
        for _ in range(producto.cantidad):
            total += producto.precio
    print(f"\nValor total del inventario: ${total:.2f}")

#el metodo que busca el producto que tenga mi inicial 
def filtrar_por_mi_inicial():
    print(f"\n-- PRODUCTOS QUE EMPIEZAN CON LA INICIAL '{Mi_inicial.upper()}' --")
    hay = False
    for producto in inventario:
        if producto.nombre.upper().startswith(Mi_inicial.upper()):
            producto.mostrar_info()
            hay = True
    if not hay:
        print("No hay productos que empiecen con esa inicial.")

#metodo agg para poder saber que se vendio 
def mostrar_historial_ventas():
    print(f"\n--- HISTORIAL DE VENTAS ({ventas_realizadas}) ---")
    if not hay_ventas:
        print("Aun no se a relaizado ninguna venta")
    else: 
        for venta in historial_ventas:
            print("-", venta)
        print(f"Total vendido: ${total_ventas:.2f}")

#metodo para eliminar productos del inventario 
def eliminar_producto():
    nombre = input("Nombre del producto a eliminar: ").strip()
    Producto = buscar_producto(nombre, inventario)

    if Producto is None:
        print("Producto no encontrado.")
    else:
        confirmacion = input(f"¿Estás seguro de que deseas eliminar '{Producto.nombre}'? (s/n):").strip().lower()

        if confirmacion == "s":
            inventario.remove(Producto)
            print(f"{Producto.nombre} fue eliminado del inventario.")
        else:
            print("Operacion cancelada.")

#las opciones del menu 
def menu():
    while True:
        print(f"\n========= INVENTARIO =========")
        print("1. Agregar producto")
        print("2. Vender producto")
        print("3. Mostrar stock bajo")
        print("4. Valor total del inventario")
        print(f"5. Filtrar productos que empiezan con '{Mi_inicial.upper()}'")
        print("6. Mostrar todos los productos")
        print("7. Historial de ventas")
        print("8. Eliminar producto")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            vender_producto(inventario)
        elif opcion == "3":
            mostrar_stock_bajo(inventario)
        elif opcion == "4":
            valor_total_inventario()
        elif opcion == "5":
            filtrar_por_mi_inicial()
        elif opcion == "6":
            mostrar_todos()
        elif opcion == "7":
            mostrar_historial_ventas()
        elif opcion == "8":
            eliminar_producto()
        elif opcion == "0":
            print("Cerrar programa")
            break
        else: 
            print("Opcion invalida")


if __name__ == "__main__":
    cargar_producto()
    menu()