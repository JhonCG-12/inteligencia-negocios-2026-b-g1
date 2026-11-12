"""Genera los CSV sintéticos del proyecto de aula. Python 3, sin dependencias."""

import csv
import random
from calendar import monthrange
from collections import Counter
from datetime import date
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
SEMILLA = 20261108
ANIO = 2025
PRODUCTOS = [
    # Código, nombre, categoría, presentación, precio, costo base, peso de demanda.
    ("P01", "Café de la Casa", "Tradicional", "250 g", 16000, 9600, 17),
    ("P02", "Café de la Casa", "Tradicional", "500 g", 29200, 17600, 13),
    ("P03", "Montaña Oscura", "Tradicional", "250 g", 17400, 10600, 11),
    ("P04", "Montaña Oscura", "Tradicional", "500 g", 32000, 19400, 9),
    ("P05", "Origen Pitalito", "Origen", "250 g", 22600, 14200, 12),
    ("P06", "Origen Pitalito", "Origen", "500 g", 41800, 26200, 8),
    ("P07", "Origen Acevedo", "Origen", "250 g", 23700, 14800, 8),
    ("P08", "Origen Acevedo", "Origen", "500 g", 43200, 27400, 6),
    ("P09", "Origen San Agustín", "Origen", "250 g", 24400, 15100, 7),
    ("P10", "Origen San Agustín", "Origen", "500 g", 44800, 28000, 5),
    ("P11", "Microlote Niebla", "Microlote", "250 g", 31800, 20200, 4),
    ("P12", "Microlote Niebla", "Microlote", "500 g", 59200, 37800, 2),
]
SEDES = [
    ("S01", "Neiva Centro", "Neiva"),
    ("S02", "Pitalito Centro", "Pitalito"),
    ("S03", "Garzón Centro", "Garzón"),
]
CANALES = ("TIENDA", "DOMICILIOS", "MAYORISTA")
FACTURAS_POR_MES = (119, 113, 120, 123, 127, 131, 128, 136, 132, 143, 164, 189)
COLUMNAS_VENTAS = [
    "FacturaID", "Linea", "Fecha", "ProductoID", "SedeID", "Canal",
    "Cantidad", "PrecioUnitarioCOP", "DescuentoCOP", "CostoUnitarioCOP",
]


def guardar_csv(ruta, encabezado, filas):
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezado)
        escritor.writerows(filas)


def simular_ventas(azar):
    ventas = []
    factura_numero = 0
    for mes, numero_facturas in enumerate(FACTURAS_POR_MES, 1):
        dias = sorted(
            azar.randint(1, monthrange(ANIO, mes)[1])
            for _ in range(numero_facturas)
        )
        for dia in dias:
            factura_numero += 1
            factura = f"F{factura_numero:06}"
            fecha = date(ANIO, mes, dia)
            sede = azar.choices(SEDES, weights=(48, 32, 20), k=1)[0][0]
            canal = azar.choices(CANALES, weights=(60, 28, 12), k=1)[0]
            lineas = azar.choices((1, 2, 3), weights=(43, 37, 20), k=1)[0]
            disponibles = PRODUCTOS.copy()
            for linea in range(1, lineas + 1):
                producto = azar.choices(
                    disponibles, weights=[p[-1] for p in disponibles], k=1
                )[0]
                disponibles.remove(producto)
                codigo, _, _, _, precio_base, costo_base, _ = producto
                if canal == "MAYORISTA":
                    cantidad = azar.randint(6, 24)
                    precio = precio_base * 90 // 100
                else:
                    cantidad = azar.choices((1, 2, 3, 4), weights=(55, 30, 12, 3), k=1)[0]
                    precio = precio_base
                tasas = (0, 5, 8, 12)
                pesos = (56, 24, 13, 7) if mes >= 11 else (74, 16, 8, 2)
                tasa_descuento = azar.choices(tasas, weights=pesos, k=1)[0]
                descuento = cantidad * precio * tasa_descuento // 100
                costo = costo_base + 60 * (mes - 1)
                ventas.append(
                    (factura, linea, fecha, codigo, sede, canal, cantidad, precio, descuento, costo)
                )
    return ventas


def introducir_problemas(ventas, azar):
    # Se duplica también la primera línea para que la evidencia sea fácil de encontrar.
    indices_duplicados = {0, *azar.sample(range(1, len(ventas)), 23)}
    crudas = []
    for i, venta in enumerate(ventas):
        factura, linea, fecha, producto, sede, canal, *importes = venta
        fecha_texto = fecha.strftime("%d/%m/%Y") if i % 4 == 0 else fecha.isoformat()
        if i % 5 == 0:
            canal = f"  {canal.lower()} "
        elif i % 7 == 0:
            canal = canal.title()
        fila = (factura, linea, fecha_texto, producto, sede, canal, *importes)
        crudas.append(fila)
        if i in indices_duplicados:
            crudas.append(fila)
    return crudas


def resumir(filtro, ventas):
    # Cifras calculadas sobre las filas válidas, antes de alterar los CSV de origen.
    netas = 0
    costo = 0
    facturas = set()
    for factura, _, _, _, _, _, cantidad, precio, descuento, costo_unitario in ventas:
        netas += cantidad * precio - descuento
        costo += cantidad * costo_unitario
        facturas.add(factura)
    utilidad = netas - costo
    return (
        filtro, len(ventas), netas, costo, utilidad,
        f"{100 * utilidad / netas:.6f}", len(facturas), f"{netas / len(facturas):.2f}",
    )


def main():
    azar = random.Random(SEMILLA)
    datos = RAIZ / "datos"
    datos.mkdir(exist_ok=True)
    ventas = simular_ventas(azar)
    crudas = introducir_problemas(ventas, azar)
    guardar_csv(datos / "ventas.csv", COLUMNAS_VENTAS, crudas)
    guardar_csv(
        datos / "productos.csv", ("ProductoID", "Producto", "Categoria", "Presentacion"),
        (producto[:4] for producto in PRODUCTOS),
    )
    guardar_csv(datos / "sedes.csv", ("SedeID", "Sede", "Municipio"), SEDES)
    guardar_csv(datos / "canales.csv", ("Canal",), ((canal,) for canal in CANALES))

    controles = [
        resumir("Sin filtros", ventas),
        resumir("Canal = DOMICILIOS", [v for v in ventas if v[5] == "DOMICILIOS"]),
        resumir("SedeID = S02 (Pitalito Centro)", [v for v in ventas if v[4] == "S02"]),
        resumir("Mes = noviembre (11)", [v for v in ventas if v[2].month == 11]),
    ]
    guardar_csv(
        RAIZ / "controles.csv",
        ("Filtro", "Filas", "VentasNetasCOP", "CostoTotalCOP", "UtilidadBrutaCOP",
         "MargenBrutoPorcentaje", "Facturas", "TicketPromedioCOP"),
        controles,
    )
    print(f"Ventas: {len(crudas)} filas crudas y {len(ventas)} filas válidas.")
    print(f"Facturas: {len({v[0] for v in ventas})}.")
    print(f"Líneas válidas por mes: {sorted(Counter(v[2].month for v in ventas).items())}")
    print(f"Primera fila cruda: {crudas[0]}")


if __name__ == "__main__":
    main()
