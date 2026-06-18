import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')

class Gasto:

    CATEGORIAS = [
        "Alimentación",
        "Transporte",
        "Vivienda",
        "Educación",
        "Entretenimiento",
        "Otros"
    ]

    def __init__(self, categoria, valor):
        self.categoria = categoria
        self.valor = valor

    def mostrar(self):
        print(f"   • {self.categoria:<18} $ {self.valor:,.0f}")


class Deuda:

    def __init__(self, nombre, valor_pendiente):
        self.nombre = nombre
        self.valor_pendiente = valor_pendiente

    def mostrar(self):
        print(f"   • {self.nombre:<20} $ {self.valor_pendiente:,.0f}")

class Usuario:

    def __init__(self, nombre, ingresos_mensuales):
        self.nombre = nombre
        self.ingresos_mensuales = ingresos_mensuales
        self.gastos = []    
        self.deudas = []    


    def agregar_gasto(self, categoria, valor):
        nuevo_gasto = Gasto(categoria, valor)  
        self.gastos.append(nuevo_gasto)         
        print(f"\n  ✔ Gasto registrado: {categoria} por $ {valor:,.0f}")

    def agregar_deuda(self, nombre, valor_pendiente):
        nueva_deuda = Deuda(nombre, valor_pendiente)   
        self.deudas.append(nueva_deuda)                 
        print(f"\n  ✔ Deuda registrada: {nombre} por $ {valor_pendiente:,.0f}")

    def calcular_total_gastos(self):
        return sum(gasto.valor for gasto in self.gastos)

    def calcular_total_deudas(self):
        return sum(deuda.valor_pendiente for deuda in self.deudas)

    def calcular_saldo_disponible(self):
        return self.ingresos_mensuales - self.calcular_total_gastos()

    def mostrar_analisis(self):
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


    def metodo_snowball(self):

        if not self.deudas:
            print("\n  ℹ No tienes deudas registradas.")
            return

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


    def mostrar_estadisticas(self):

        if not self.gastos:
            print("\n  ℹ No tienes gastos registrados.")
            return

        gastos_por_categoria = {}

        for gasto in self.gastos:
            if gasto.categoria in gastos_por_categoria:
                gastos_por_categoria[gasto.categoria] += gasto.valor
            else:
                gastos_por_categoria[gasto.categoria] = gasto.valor

        categoria_mayor = max(gastos_por_categoria, key=gastos_por_categoria.get)

        print("\n" + "=" * 50)
        print("     ESTADÍSTICAS DE GASTOS POR CATEGORÍA")
        print("=" * 50)

        for categoria, total in gastos_por_categoria.items():
            porcentaje = (total / self.calcular_total_gastos()) * 100
            barra = "█" * int(porcentaje / 5)
            marca = " ← MAYOR" if categoria == categoria_mayor else ""
            print(f"  {categoria:<18} $ {total:>10,.0f}  {porcentaje:5.1f}%  {barra}{marca}")

        print(f"\n  📊 Categoría con mayor gasto: {categoria_mayor}")
        print("=" * 50)

        return gastos_por_categoria   


    def generar_graficos(self):

        if not self.gastos:
            print("\n  ℹ Necesitas registrar gastos para generar gráficos.")
            return

        gastos_por_categoria = {}
        for gasto in self.gastos:
            gastos_por_categoria[gasto.categoria] = (
                gastos_por_categoria.get(gasto.categoria, 0) + gasto.valor
            )

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f"Análisis Financiero de {self.nombre}",
                     fontsize=14, fontweight='bold', y=1.02)

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

        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')

        ax1.set_title("Distribución de Gastos\npor Categoría",
                      fontsize=11, fontweight='bold')

        conceptos = ['Ingresos\nMensuales', 'Total\nGastos', 'Total\nDeudas']
        montos = [
            self.ingresos_mensuales,
            self.calcular_total_gastos(),
            self.calcular_total_deudas()
        ]
        colores_barras = ['#2ECC71', '#E74C3C', '#E67E22']

        barras = ax2.bar(conceptos, montos, color=colores_barras,
                         width=0.5, edgecolor='white', linewidth=1.5)

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

        plt.tight_layout()
        nombre_archivo = "graficos_financieros.png"
        plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight',
                    facecolor='white')
        plt.close()

        print(f"\n  ✅ Gráficos guardados en: '{nombre_archivo}'")


def limpiar_pantalla():
    print("\n" * 2)


def mostrar_menu_principal():
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
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"  ❌ Opción inválida. Elige entre: {', '.join(opciones_validas)}")


def registrar_usuario():
    print("\n" + "=" * 50)
    print("     👤 REGISTRO DE USUARIO")
    print("=" * 50)

    nombre = ""
    while not nombre:
        nombre = input("  Tu nombre: ").strip()
        if not nombre:
            print("  ❌ El nombre no puede estar vacío.")

    ingresos = pedir_numero_positivo("  Ingresos mensuales ($): ")

    usuario = Usuario(nombre, ingresos) 
    print(f"\n  ✅ ¡Bienvenido/a, {nombre}!")
    print(f"  Ingresos registrados: $ {ingresos:,.0f}")
    return usuario


def menu_registrar_gasto(usuario):
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
    usuario.agregar_gasto(categoria, valor)


def menu_registrar_deuda(usuario):
    print("\n" + "=" * 50)
    print("     💳 REGISTRAR DEUDA")
    print("=" * 50)

    nombre = ""
    while not nombre:
        nombre = input("  Nombre de la deuda (ej: Tarjeta, Préstamo): ").strip()
        if not nombre:
            print("  ❌ El nombre no puede estar vacío.")

    valor = pedir_numero_positivo("  Valor pendiente ($): ")
    usuario.agregar_deuda(nombre, valor)  


def ver_gastos(usuario):
    print("\n" + "=" * 50)
    print("     📋 MIS GASTOS REGISTRADOS")
    print("=" * 50)

    if not usuario.gastos:
        print("  ℹ No has registrado gastos aún.")
        return

    for i, gasto in enumerate(usuario.gastos, start=1):
        print(f"  [{i}]", end="")
        gasto.mostrar()   

    print(f"\n  Total: $ {usuario.calcular_total_gastos():,.0f}")
    print("=" * 50)


def ver_deudas(usuario):
    print("\n" + "=" * 50)
    print("     💳 MIS DEUDAS REGISTRADAS")
    print("=" * 50)

    if not usuario.deudas:
        print("  ℹ No has registrado deudas aún.")
        return

    for i, deuda in enumerate(usuario.deudas, start=1):
        print(f"  [{i}]", end="")
        deuda.mostrar() 

    print(f"\n  Total deudas: $ {usuario.calcular_total_deudas():,.0f}")
    print("=" * 50)


def main():

    print("\n" + "=" * 50)
    print("   💰 SISTEMA DE GESTIÓN FINANCIERA PERSONAL")
    print("         con Método Snowball ❄️")
    print("=" * 50)
    print("  Proyecto académico - Primer Semestre")
    print("  Programación Orientada a Objetos (POO)")
    print("=" * 50)
    input("\n  Presiona ENTER para comenzar...")

    usuario = registrar_usuario()

    while True:
        mostrar_menu_principal()
        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            menu_registrar_gasto(usuario)

        elif opcion == "2":
            menu_registrar_deuda(usuario)

        elif opcion == "3":
            if not usuario.gastos and not usuario.deudas:
                print("\n  ℹ Registra gastos o deudas primero.")
            else:
                usuario.mostrar_analisis()

        elif opcion == "4":
            usuario.metodo_snowball()

        elif opcion == "5":
            usuario.mostrar_estadisticas()

        elif opcion == "6":
            usuario.generar_graficos()

        elif opcion == "7":
            ver_gastos(usuario)

        elif opcion == "8":
            ver_deudas(usuario)

        elif opcion == "0":
            print(f"\n  ¡Hasta pronto, {usuario.nombre}! 👋")
            print("  Recuerda: controlar tus finanzas es el primer paso")
            print("  hacia la libertad financiera. 💪")
            print("=" * 50 + "\n")
            break

        else:
            print("\n  ❌ Opción no válida. Elige un número del 0 al 8.")

        input("\n  Presiona ENTER para continuar...")
        
if __name__ == "__main__":
    main()