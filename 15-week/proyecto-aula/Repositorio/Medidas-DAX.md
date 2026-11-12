# Modelo estrella y medidas DAX

## Calendario y relaciones

Después de cargar los CSV en Power Query, en Power BI Desktop selecciona **Modelado → Nueva tabla** y pega este bloque.

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "Año", YEAR ( [Date] ),
    "Trimestre", "T" & QUARTER ( [Date] ),
    "Mes", FORMAT ( [Date], "mmmm", "es-CO" ),
    "NumeroMes", MONTH ( [Date] )
)
```

Selecciona `Calendario[Date]`, establece su tipo como **Fecha** y marca `Calendario` como tabla de fechas con esa columna. Selecciona `Calendario[Mes]` y usa **Herramientas de columna → Ordenar por columna → NumeroMes**. Para el gráfico mensual, crea una jerarquía con `Año`, `Trimestre` y `Mes`, en ese orden.

En la vista **Modelo**, revisa o crea estas cuatro relaciones activas. Cada una tiene cardinalidad **uno a varios (1:*)** y filtro **único** desde la dimensión hacia `Ventas`.

| Dimensión (1) | Ventas (*) |
| --- | --- |
| `Productos[ProductoID]` | `Ventas[ProductoID]` |
| `Sedes[SedeID]` | `Ventas[SedeID]` |
| `Canales[Canal]` | `Ventas[Canal]` |
| `Calendario[Date]` | `Ventas[Fecha]` |

## Medidas

Crea una **Nueva medida** por bloque en `Ventas`, en el orden indicado. Si activaste separadores DAX localizados en Power BI y el editor marca error en las comas entre argumentos, cámbialas por punto y coma en los bloques DAX.

```dax
Ventas netas =
SUMX (
    Ventas,
    Ventas[Cantidad] * Ventas[PrecioUnitarioCOP] - Ventas[DescuentoCOP]
)
```

```dax
Costo total =
SUMX ( Ventas, Ventas[Cantidad] * Ventas[CostoUnitarioCOP] )
```

```dax
Utilidad bruta =
[Ventas netas] - [Costo total]
```

```dax
Margen bruto % =
DIVIDE ( [Utilidad bruta], [Ventas netas] )
```

```dax
Número de facturas =
DISTINCTCOUNT ( Ventas[FacturaID] )
```

```dax
Ticket promedio =
DIVIDE ( [Ventas netas], [Número de facturas] )
```

Aplica formato **porcentaje** con dos decimales a `Margen bruto %` y **COP** a ventas, costo, utilidad y ticket promedio. `DescuentoCOP` es el descuento total de una línea, así que se resta una vez por línea. `Número de facturas` cuenta cada factura una vez dentro del contexto de filtros.

## Prueba de las cifras y de los filtros

Usa un visual de tabla con las seis medidas para comparar con `controles.csv`. Si abres ese archivo en Excel, puedes importarlo con **Datos → Desde texto/CSV** y elegir la coma como delimitador. Revisa primero el total general, que debe contar 1.625 facturas. Luego prueba cada uno de estos tres filtros por separado y toma una captura por caso.

1. Selecciona `Canales[Canal] = DOMICILIOS`.
2. Limpia el filtro anterior y selecciona `Sedes[SedeID] = S02` (Pitalito).
3. Limpia el filtro anterior y selecciona `Calendario[Mes] = noviembre`.

Registra por cada prueba el valor esperado y el observado. Compara los porcentajes y el ticket con el mismo número de decimales en ambos archivos. Usa columnas de las dimensiones en los segmentadores y en el eje de fechas para comprobar que las relaciones propagan el filtro.

Referencias de Microsoft Learn. [Diseño de esquema de estrella en Power BI](https://learn.microsoft.com/es-es/power-bi/guidance/star-schema) y [función CALENDAR](https://learn.microsoft.com/es-es/dax/calendar-function-dax).
