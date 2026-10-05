let
    Origen = Csv.Document(File.Contents("C:\RUTA\ventas_sucias.csv"), [Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Texto_limpio = Table.TransformColumns(Encabezados, {
        {"Venta_ID", each Text.Trim(Text.Clean(_)), type text},
        {"Sucursal", each Text.Trim(Text.Clean(_)), type text},
        {"Producto", each Text.Trim(Text.Clean(_)), type text}
    }),
    Texto_uniforme = Table.TransformColumns(Texto_limpio, {
        {"Sucursal", each Text.Upper(_, "es-CO"), type text},
        {"Producto", each Text.Upper(_, "es-CO"), type text}
    }),
    Tipos_corregidos = Table.TransformColumnTypes(Texto_uniforme, {
        {"Venta_ID", type text}, {"Fecha", type date}, {"Sucursal", type text},
        {"Producto", type text}, {"Cantidad", Int64.Type}, {"Precio_Unitario", Currency.Type}
    }, "es-CO"),
    Duplicados_eliminados = Table.Distinct(Tipos_corregidos),
    Importe_agregado = Table.AddColumn(Duplicados_eliminados, "Importe", each [Cantidad] * [Precio_Unitario], Currency.Type),
    Columna_condicional = Table.AddColumn(Importe_agregado, "Segmento", each if [Cantidad] >= 3 then "Mayor volumen" else "Menor volumen", type text)
in
    Columna_condicional
