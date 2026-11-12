# Cargar y limpiar los datos en Power Query

1. Extrae la carpeta del proyecto. En Power BI Desktop, abre **Inicio → Transformar datos**.
2. En Power Query, ve a **Inicio → Administrar parámetros → Nuevo parámetro**. Llámalo `RutaDatos`, selecciona tipo **Texto** y escribe la ruta completa de la carpeta `datos` en **Valor actual**. Por ejemplo, `C:\Proyectos\cafe-horizonte-del-sur\datos`.
3. Crea una **Consulta en blanco** por cada bloque de esta guía. Cambia el nombre de la consulta al indicado y pega su bloque completo en **Editor avanzado**, reemplazando el texto inicial. Crea `LeerCSV` primero, porque las otras consultas la usan.

## Consulta `LeerCSV`

```powerquery
(archivo as text) as table =>
let
    Carpeta = Text.TrimEnd(RutaDatos, {"\", "/"}),
    Origen = Csv.Document(
        File.Contents(Carpeta & "\" & archivo),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true])
in
    Encabezados
```

## Consulta `Ventas`

```powerquery
let
    Origen = LeerCSV("ventas.csv"),
    #"Tipos de datos" = Table.TransformColumnTypes(
        Origen,
        {
            {"FacturaID", type text},
            {"Linea", Int64.Type},
            {"Fecha", type text},
            {"ProductoID", type text},
            {"SedeID", type text},
            {"Canal", type text},
            {"Cantidad", Int64.Type},
            {"PrecioUnitarioCOP", Int64.Type},
            {"DescuentoCOP", Int64.Type},
            {"CostoUnitarioCOP", Int64.Type}
        },
        "es-CO"
    ),
    #"Fechas convertidas" = Table.TransformColumns(
        #"Tipos de datos",
        {{"Fecha", each
            if Text.Contains(_, "/") then
                Date.FromText(_, [Format = "dd/MM/yyyy", Culture = "es-CO"])
            else
                Date.FromText(_, [Format = "yyyy-MM-dd", Culture = "en-US"]),
            type date}}
    ),
    #"Canales normalizados" = Table.TransformColumns(
        #"Fechas convertidas",
        {{"Canal", each Text.Upper(Text.Trim(_), "es-CO"), type text}}
    ),
    #"Líneas únicas" = Table.Distinct(#"Canales normalizados", {"FacturaID", "Linea"})
in
    #"Líneas únicas"
```

Cada fila representa una línea de una factura. Por eso la clave de duplicados combina `FacturaID` y `Linea`.

## Consulta `Productos`

```powerquery
let
    Origen = LeerCSV("productos.csv"),
    Tipos = Table.TransformColumnTypes(Origen, {
        {"ProductoID", type text}, {"Producto", type text},
        {"Categoria", type text}, {"Presentacion", type text}
    })
in
    Tipos
```

## Consulta `Sedes`

```powerquery
let
    Origen = LeerCSV("sedes.csv"),
    Tipos = Table.TransformColumnTypes(Origen, {
        {"SedeID", type text}, {"Sede", type text}, {"Municipio", type text}
    })
in
    Tipos
```

## Consulta `Canales`

```powerquery
let
    Origen = LeerCSV("canales.csv"),
    Tipos = Table.TransformColumnTypes(Origen, {{"Canal", type text}})
in
    Tipos
```

## Evidencias para el informe

Selecciona los pasos de la consulta `Ventas` en el panel **Pasos aplicados**. En la fuente, las primeras dos filas repiten `F000001`, línea `1`. Ambas tienen la fecha `01/01/2025` y el canal `  tienda `. La tercera fila tiene la fecha `2025-01-01`. Usa este grupo para documentar los tres cambios.

| Problema | Paso para la captura antes | Paso para la captura después | Qué comprobar |
| --- | --- | --- | --- |
| Fecha en dos formatos de texto | `Tipos de datos` | `Fechas convertidas` | `Fecha` tiene tipo fecha y se interpreta con día y mes correctos. |
| Canal escrito con espacios o minúsculas | `Fechas convertidas` | `Canales normalizados` | `Canal` coincide con el catálogo en `Canales`. |
| Líneas repetidas | `Canales normalizados` | `Líneas únicas` | La combinación `FacturaID` + `Linea` aparece una sola vez. El recuento baja de 2.864 a 2.840 filas. |

La vista previa de Power Query puede mostrar solo una muestra. Para comprobar el recuento completo, selecciona el último paso y pulsa **fx** en la barra de fórmulas. En ese paso temporal escribe `= Table.RowCount(Origen)` para comprobar las 2.864 filas originales. Sustituye la fórmula por `= Table.RowCount(#"Líneas únicas")` para comprobar las 2.840 filas limpias. Anota ambos valores y elimina el paso temporal para volver a la tabla.

Selecciona **Cerrar y aplicar**. En el modelo deben aparecer `Ventas`, `Productos`, `Sedes` y `Canales`. Sigue con [Medidas DAX y modelo](Medidas-DAX.md).

Referencias de Microsoft Learn. [Lectura de CSV en Power Query](https://learn.microsoft.com/es-es/powerquery-m/csv-document) y [conversión de fechas por formato](https://learn.microsoft.com/es-es/powerquery-m/date-fromtext).
