let
    Origen = Excel.Workbook(File.Contents(RutaExcel), null, true),
    Hoja = Origen{[Item="Datos",Kind="Sheet"]}[Data],
    Encabezados = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true]),
    SinVacias = Table.SelectRows(Encabezados, each List.NonNullCount(Record.FieldValues(_)) > 0),
    Tipos = Table.TransformColumnTypes(SinVacias, {
      {"Venta_ID", type text}, {"Fecha", type date}, {"Ciudad", type text}, {"Canal", type text},
      {"Categoría", type text}, {"Producto", type text}, {"Cliente_ID_Anonimo", type text},
      {"Tipo_Cliente", type text}, {"Unidades", Int64.Type}, {"Precio_Unitario", Currency.Type},
      {"Descuento_Pct", type number}, {"Costo_Unitario", Currency.Type}, {"Medio_Pago", type text},
      {"Tiempo_Entrega_Min", type number}, {"Estado_Entrega", type text}, {"Satisfaccion_1_5", Int64.Type},
      {"Ingreso_Bruto", Currency.Type}, {"Descuento_Valor", Currency.Type}, {"Ingreso_Neto", Currency.Type},
      {"Costo_Total", Currency.Type}, {"Margen_Bruto", Currency.Type}}, "es-CO"),
    Textos = Table.TransformColumns(Tipos, List.Transform({"Venta_ID","Ciudad","Canal","Categoría","Producto","Tipo_Cliente","Medio_Pago","Estado_Entrega"}, each {_, Text.Trim, type text})),
    Validados = if Table.RowCount(Textos) <> Table.RowCount(Table.Distinct(Textos, {"Venta_ID"}))
      then error "Venta_ID duplicado. Revisar origen; no se eliminan ventas automáticamente." else Textos,
    SinCalculadas = Table.RemoveColumns(Validados, {"Ingreso_Bruto","Descuento_Valor","Ingreso_Neto","Costo_Total","Margen_Bruto","Cliente_ID_Anonimo"}),
    Bruto = Table.AddColumn(SinCalculadas,"Ingreso_Bruto", each [Unidades]*[Precio_Unitario],Currency.Type),
    Descuento = Table.AddColumn(Bruto,"Descuento_Valor", each [Ingreso_Bruto]*[Descuento_Pct],Currency.Type),
    Neto = Table.AddColumn(Descuento,"Ingreso_Neto", each [Ingreso_Bruto]-[Descuento_Valor],Currency.Type),
    Costo = Table.AddColumn(Neto,"Costo_Total", each [Unidades]*[Costo_Unitario],Currency.Type),
    Margen = Table.AddColumn(Costo,"Margen_Bruto", each [Ingreso_Neto]-[Costo_Total],Currency.Type),
    Aplica = Table.AddColumn(Margen,"Entrega_Aplica",each List.Contains({"A tiempo","Tardía"},[Estado_Entrega]),type logical),
    Minutos = Table.AddColumn(Aplica,"Tiempo_Entrega_Valido",each if [Entrega_Aplica] then [Tiempo_Entrega_Min] else null,type nullable number)
in Minutos
