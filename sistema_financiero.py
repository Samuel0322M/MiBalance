import matplotlib
matplotlib.use('Agg')           # Backend sin ventana gráfica (guarda en archivo)
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')


# =============================================================================
# CLASE: Gasto
# Representa un gasto individual del usuario
# =============================================================================
class Gasto:
    """
    POO: Esta clase modela un gasto con sus atributos.
    Cada objeto Gasto guarda la categoría y el valor del gasto.
    """

    # Categorías válidas (lista de opciones)
    CATEGORIAS = [
        "Alimentación",
        "Transporte",
        "Vivienda",
        "Educación",
        "Entretenimiento",
        "Otros"
    ]

    def __init__(self, categoria, valor):
        """Constructor: inicializa los atributos del gasto."""
        self.categoria = categoria
        self.valor = valor

    def mostrar(self):
        """Método que muestra la información del gasto formateada."""
        print(f"   • {self.categoria:<18} $ {self.valor:,.0f}")


# =============================================================================
# CLASE: Deuda
# Representa una deuda del usuario
# =============================================================================
class Deuda:
    """
    POO: Esta clase modela una deuda con nombre y valor pendiente.
    Las deudas se ordenarán con el Método Snowball.
    """

    def __init__(self, nombre, valor_pendiente):
        """Constructor: inicializa los atributos de la deuda."""
        self.nombre = nombre
        self.valor_pendiente = valor_pendiente

    def mostrar(self):
        """Método que muestra la información de la deuda formateada."""
        print(f"   • {self.nombre:<20} $ {self.valor_pendiente:,.0f}")


# =============================================================================
# CLASE: Usuario
# Clase principal que gestiona toda la información financiera
# =============================================================================
class Usuario:
    """
    POO: Clase principal del sistema.
    Contiene listas de gastos y deudas, y los métodos de análisis.
    """

    def __init__(self, nombre, ingresos_mensuales):
        """Constructor: crea el usuario con nombre e ingresos."""
        self.nombre = nombre
        self.ingresos_mensuales = ingresos_mensuales
        self.gastos = []    # LISTA de objetos Gasto (POO + listas)
        self.deudas = []    # LISTA de objetos Deuda (POO + listas)

    # -------------------------------------------------------------------------
    # Métodos para agregar gastos y deudas
    # -------------------------------------------------------------------------

    def agregar_gasto(self, categoria, valor):
        """Crea un objeto Gasto y lo agrega a la lista de gastos."""
        nuevo_gasto = Gasto(categoria, valor)   # Instancia de la clase Gasto
        self.gastos.append(nuevo_gasto)         # Se guarda en la lista
        print(f"\n  ✔ Gasto registrado: {categoria} por $ {valor:,.0f}")

    def agregar_deuda(self, nombre, valor_pendiente):
        """Crea un objeto Deuda y lo agrega a la lista de deudas."""
        nueva_deuda = Deuda(nombre, valor_pendiente)   # Instancia de la clase Deuda
        self.deudas.append(nueva_deuda)                 # Se guarda en la lista
        print(f"\n  ✔ Deuda registrada: {nombre} por $ {valor_pendiente:,.0f}")

    # -------------------------------------------------------------------------
    # Métodos de cálculo
    # -------------------------------------------------------------------------

    def calcular_total_gastos(self):
        """Suma todos los valores de los gastos usando una lista."""
        return sum(gasto.valor for gasto in self.gastos)

    def calcular_total_deudas(self):
        """Suma todos los valores pendientes de las deudas."""
        return sum(deuda.valor_pendiente for deuda in self.deudas)

    def calcular_saldo_disponible(self):
        """Calcula el dinero que queda después de los gastos."""
        return self.ingresos_mensuales - self.calcular_total_gastos()

    # -------------------------------------------------------------------------
    # Método: Análisis financiero
    # -------------------------------------------------------------------------

    def mostrar_analisis(self):
        """
        Muestra el resumen financiero completo con advertencias.
        Usa los métodos de cálculo definidos arriba.
        """
        total_gastos = self.calcular_total_gastos()
        total_deudas = self.calcular_total_deudas()
        saldo = self.calcular_saldo_disponible()

        print("\n" + "=" * 50)
        print("        ANÁLISIS FINANCIERO")
        print("=" * 50)
        print(f"  Ingresos mensuales:  $ {self.ingresos_mensuales:>12,.0f}")
        print(f"  Total gastos:        $ {total_gastos:>12,.0f}")
        print(f"  Total deudas:        $ {total_deudas:>12,.0f}")
        print(f"  Saldo disponible:    $ {saldo:>12,.0f}")
        print("-" * 50)

        # Advertencias con condiciones
        if total_gastos > self.ingresos_mensuales:
            print("\n  ⚠️  ADVERTENCIA: Tus gastos SUPERAN tus ingresos!")
            print(f"     Déficit: $ {abs(saldo):,.0f}")
        elif saldo < self.ingresos_mensuales * 0.1:
            print("\n  ⚠️  ATENCIÓN: Tu saldo disponible es muy bajo.")
        else:
            print("\n  ✅ Tus gastos están dentro de tus ingresos.")

        if total_deudas > self.ingresos_mensuales * 0.5:
            print("\n  ⚠️  ADVERTENCIA: Tus deudas representan más del 50%")
            print(f"     de tus ingresos ({(total_deudas/self.ingresos_mensuales)*100:.1f}%).")
        print("=" * 50)

    # -------------------------------------------------------------------------
    # Método: Método Snowball
    # -------------------------------------------------------------------------

    def metodo_snowball(self):
        """
        Ordena las deudas de menor a mayor y recomienda el orden de pago.
        El Método Snowball sugiere pagar primero la deuda más pequeña
        para ganar impulso ("bola de nieve") y motivación.
        """
        if not self.deudas:
            print("\n  ℹ No tienes deudas registradas.")
            return

        # Ordenar la lista de deudas de menor a mayor (sorted())
        deudas_ordenadas = sorted(self.deudas, key=lambda d: d.valor_pendiente)

        print("\n" + "=" * 50)
        print("       MÉTODO SNOWBALL - PLAN DE PAGO")
        print("=" * 50)
        print("  Orden recomendado (de menor a mayor deuda):\n")

        for i, deuda in enumerate(deudas_ordenadas, start=1):
            if i == 1:
                print(f"  {i}. ⭐ {deuda.nombre:<20} $ {deuda.valor_pendiente:>10,.0f}  ← PAGA PRIMERO")
            else:
                print(f"  {i}. {deuda.nombre:<22} $ {deuda.valor_pendiente:>10,.0f}")

        print("\n  💡 Consejo Snowball:")
        primera = deudas_ordenadas[0]
        print(f"     Concentra tus pagos extra en '{primera.nombre}'")
        print(f"     ($ {primera.valor_pendiente:,.0f}). Al liquidarla, usa ese")
        print(f"     dinero para atacar la siguiente deuda.")
        print("=" * 50)

    # -------------------------------------------------------------------------
    # Método: Estadísticas por categoría (usa DICCIONARIO)
    # -------------------------------------------------------------------------

    def mostrar_estadisticas(self):
        """
        Agrupa los gastos por categoría usando un DICCIONARIO.
        Diccionario: {categoria: total_gastado}
        """
        if not self.gastos:
            print("\n  ℹ No tienes gastos registrados.")
            return

        # DICCIONARIO para acumular gastos por categoría
        gastos_por_categoria = {}

        for gasto in self.gastos:
            if gasto.categoria in gastos_por_categoria:
                gastos_por_categoria[gasto.categoria] += gasto.valor
            else:
                gastos_por_categoria[gasto.categoria] = gasto.valor

        # Encontrar la categoría con mayor gasto
        categoria_mayor = max(gastos_por_categoria, key=gastos_por_categoria.get)

        print("\n" + "=" * 50)
        print("     ESTADÍSTICAS DE GASTOS POR CATEGORÍA")
        print("=" * 50)

        for categoria, total in gastos_por_categoria.items():
            porcentaje = (total / self.calcular_total_gastos()) * 100
            barra = "█" * int(porcentaje / 5)   # Barra visual simple
            marca = " ← MAYOR" if categoria == categoria_mayor else ""
            print(f"  {categoria:<18} $ {total:>10,.0f}  {porcentaje:5.1f}%  {barra}{marca}")

        print(f"\n  📊 Categoría con mayor gasto: {categoria_mayor}")
        print("=" * 50)

        return gastos_por_categoria   # Retorna el diccionario para los gráficos

    # -------------------------------------------------------------------------
    # Método: Generar gráficos con matplotlib
    # -------------------------------------------------------------------------

    def generar_graficos(self):
        """
        Genera dos gráficos usando matplotlib:
          1. Gráfico de pastel: distribución de gastos por categoría
          2. Gráfico de barras: comparativa ingresos vs gastos vs deudas
        Los gráficos se guardan como imágenes PNG.
        """
        if not self.gastos:
            print("\n  ℹ Necesitas registrar gastos para generar gráficos.")
            return

        # Obtener datos del diccionario de categorías
        gastos_por_categoria = {}
        for gasto in self.gastos:
            gastos_por_categoria[gasto.categoria] = (
                gastos_por_categoria.get(gasto.categoria, 0) + gasto.valor
            )

        # Crear figura con dos subgráficos lado a lado
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f"Análisis Financiero de {self.nombre}",
                     fontsize=14, fontweight='bold', y=1.02)

        # ---- GRÁFICO 1: PIE CHART (Pastel) ----
        categorias = list(gastos_por_categoria.keys())
        valores = list(gastos_por_categoria.values())
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

        wedges, texts, autotexts = ax1.pie(
            valores,
            labels=categorias,
            colors=colores[:len(categorias)],
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85
        )
        # Estilo del gráfico de pastel
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')

        ax1.set_title("Distribución de Gastos\npor Categoría",
                      fontsize=11, fontweight='bold')

        # ---- GRÁFICO 2: BARRAS (Ingresos vs Gastos vs Deudas) ----
        conceptos = ['Ingresos\nMensuales', 'Total\nGastos', 'Total\nDeudas']
        montos = [
            self.ingresos_mensuales,
            self.calcular_total_gastos(),
            self.calcular_total_deudas()
        ]
        colores_barras = ['#2ECC71', '#E74C3C', '#E67E22']

        barras = ax2.bar(conceptos, montos, color=colores_barras,
                         width=0.5, edgecolor='white', linewidth=1.5)

        # Agregar valores encima de cada barra
        for barra, monto in zip(barras, montos):
            altura = barra.get_height()
            ax2.text(
                barra.get_x() + barra.get_width() / 2.,
                altura + max(montos) * 0.01,
                f'$ {monto:,.0f}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold'
            )

        ax2.set_title("Comparativa Financiera",
                      fontsize=11, fontweight='bold')
        ax2.set_ylabel("Monto ($)", fontsize=10)
        ax2.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'${x:,.0f}')
        )
        ax2.set_ylim(0, max(montos) * 1.15)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.set_facecolor('#F8F9FA')

        # Guardar la imagen
        plt.tight_layout()
        nombre_archivo = "graficos_financieros.png"
        plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight',
                    facecolor='white')
        plt.close()

        print(f"\n  ✅ Gráficos guardados en: '{nombre_archivo}'")


# =============================================================================
# FUNCIONES DEL MENÚ (fuera de las clases)
# =============================================================================

def limpiar_pantalla():
    """Imprime líneas en blanco para simular limpiar la consola."""
    print("\n" * 2)


def mostrar_menu_principal():
    """Muestra el menú principal con las opciones disponibles."""
    print("\n" + "=" * 50)
    print("   💰 SISTEMA DE GESTIÓN FINANCIERA PERSONAL")
    print("=" * 50)
    print("  1. 📋 Registrar gasto")
    print("  2. 💳 Registrar deuda")
    print("  3. 📊 Ver análisis financiero")
    print("  4. ❄️  Aplicar Método Snowball")
    print("  5. 📈 Ver estadísticas por categoría")
    print("  6. 📉 Generar gráficos")
    print("  7. 👀 Ver todos mis gastos")
    print("  8. 👀 Ver todas mis deudas")
    print("  0. 🚪 Salir")
    print("-" * 50)


def pedir_numero_positivo(mensaje):
    """
    Función que valida que el usuario ingrese un número positivo.
    Repite la pregunta hasta recibir un valor válido.
    """
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("  ❌ El valor debe ser mayor a cero.")
            else:
                return valor
        except ValueError:
            print("  ❌ Ingresa un número válido (ej: 50000).")


def pedir_opcion_menu(mensaje, opciones_validas):
    """
    Función que valida la opción ingresada en un menú.
    Recibe la lista de opciones válidas.
    """
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"  ❌ Opción inválida. Elige entre: {', '.join(opciones_validas)}")


def registrar_usuario():
    """
    Solicita el nombre e ingresos del usuario y crea el objeto Usuario.
    Retorna el objeto Usuario creado.
    """
    print("\n" + "=" * 50)
    print("     👤 REGISTRO DE USUARIO")
    print("=" * 50)

    nombre = ""
    while not nombre:
        nombre = input("  Tu nombre: ").strip()
        if not nombre:
            print("  ❌ El nombre no puede estar vacío.")

    ingresos = pedir_numero_positivo("  Ingresos mensuales ($): ")

    usuario = Usuario(nombre, ingresos)   # Instancia de la clase Usuario (POO)
    print(f"\n  ✅ ¡Bienvenido/a, {nombre}!")
    print(f"  Ingresos registrados: $ {ingresos:,.0f}")
    return usuario


def menu_registrar_gasto(usuario):
    """Muestra el submenú para registrar un gasto y llama al método del usuario."""
    print("\n" + "=" * 50)
    print("     📋 REGISTRAR GASTO")
    print("=" * 50)
    print("  Categorías disponibles:")

    for i, cat in enumerate(Gasto.CATEGORIAS, start=1):
        print(f"    {i}. {cat}")

    opciones_cat = [str(i) for i in range(1, len(Gasto.CATEGORIAS) + 1)]
    opcion = pedir_opcion_menu("\n  Elige la categoría: ", opciones_cat)
    categoria = Gasto.CATEGORIAS[int(opcion) - 1]

    valor = pedir_numero_positivo(f"  Valor del gasto en {categoria} ($): ")
    usuario.agregar_gasto(categoria, valor)   # Llama al método del objeto usuario


def menu_registrar_deuda(usuario):
    """Muestra el submenú para registrar una deuda y llama al método del usuario."""
    print("\n" + "=" * 50)
    print("     💳 REGISTRAR DEUDA")
    print("=" * 50)

    nombre = ""
    while not nombre:
        nombre = input("  Nombre de la deuda (ej: Tarjeta, Préstamo): ").strip()
        if not nombre:
            print("  ❌ El nombre no puede estar vacío.")

    valor = pedir_numero_positivo("  Valor pendiente ($): ")
    usuario.agregar_deuda(nombre, valor)   # Llama al método del objeto usuario


def ver_gastos(usuario):
    """Lista todos los gastos registrados en la lista de gastos."""
    print("\n" + "=" * 50)
    print("     📋 MIS GASTOS REGISTRADOS")
    print("=" * 50)

    if not usuario.gastos:
        print("  ℹ No has registrado gastos aún.")
        return

    for i, gasto in enumerate(usuario.gastos, start=1):
        print(f"  [{i}]", end="")
        gasto.mostrar()   # Llama al método mostrar() del objeto Gasto

    print(f"\n  Total: $ {usuario.calcular_total_gastos():,.0f}")
    print("=" * 50)


def ver_deudas(usuario):
    """Lista todas las deudas registradas en la lista de deudas."""
    print("\n" + "=" * 50)
    print("     💳 MIS DEUDAS REGISTRADAS")
    print("=" * 50)

    if not usuario.deudas:
        print("  ℹ No has registrado deudas aún.")
        return

    for i, deuda in enumerate(usuario.deudas, start=1):
        print(f"  [{i}]", end="")
        deuda.mostrar()   # Llama al método mostrar() del objeto Deuda

    print(f"\n  Total deudas: $ {usuario.calcular_total_deudas():,.0f}")
    print("=" * 50)


# =============================================================================
# FUNCIÓN PRINCIPAL: main()
# Punto de entrada del programa
# =============================================================================

def main():
    """Función principal que controla el flujo del programa."""

    # Pantalla de bienvenida
    print("\n" + "=" * 50)
    print("   💰 SISTEMA DE GESTIÓN FINANCIERA PERSONAL")
    print("         con Método Snowball ❄️")
    print("=" * 50)
    print("  Proyecto académico - Primer Semestre")
    print("  Programación Orientada a Objetos (POO)")
    print("=" * 50)
    input("\n  Presiona ENTER para comenzar...")

    # Paso 1: Registrar usuario (crea el objeto Usuario - POO)
    usuario = registrar_usuario()

    # Paso 2: Menú principal con bucle
    while True:
        mostrar_menu_principal()
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            # Registrar gasto
            menu_registrar_gasto(usuario)

        elif opcion == "2":
            # Registrar deuda
            menu_registrar_deuda(usuario)

        elif opcion == "3":
            # Análisis financiero
            if not usuario.gastos and not usuario.deudas:
                print("\n  ℹ Registra gastos o deudas primero.")
            else:
                usuario.mostrar_analisis()

        elif opcion == "4":
            # Método Snowball
            usuario.metodo_snowball()

        elif opcion == "5":
            # Estadísticas por categoría (usa diccionario)
            usuario.mostrar_estadisticas()

        elif opcion == "6":
            # Generar gráficos con matplotlib
            usuario.generar_graficos()

        elif opcion == "7":
            # Ver lista de gastos
            ver_gastos(usuario)

        elif opcion == "8":
            # Ver lista de deudas
            ver_deudas(usuario)

        elif opcion == "0":
            # Salir
            print(f"\n  ¡Hasta pronto, {usuario.nombre}! 👋")
            print("  Recuerda: controlar tus finanzas es el primer paso")
            print("  hacia la libertad financiera. 💪")
            print("=" * 50 + "\n")
            break

        else:
            print("\n  ❌ Opción no válida. Elige un número del 0 al 8.")

        input("\n  Presiona ENTER para continuar...")


# =============================================================================
# Punto de inicio del programa
# =============================================================================
if __name__ == "__main__":
    main()
