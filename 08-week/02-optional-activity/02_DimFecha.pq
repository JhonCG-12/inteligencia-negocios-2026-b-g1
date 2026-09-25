let
    Inicio = Date.StartOfYear(List.Min(FactVentas[Fecha])),
    Fin = Date.EndOfYear(List.Max(FactVentas[Fecha])),
    Fechas = Table.FromList(List.Dates(Inicio, Duration.Days(Fin-Inicio)+1, #duration(1,0,0,0)),Splitter.SplitByNothing(),{"Fecha"}),
    Tipos = Table.TransformColumnTypes(Fechas,{{"Fecha",type date}}),
    Anio = Table.AddColumn(Tipos,"Anio",each Date.Year([Fecha]),Int64.Type),
    Mes = Table.AddColumn(Anio,"Mes",each Date.ToText([Fecha],"yyyy-MM"),type text),
    Orden = Table.AddColumn(Mes,"MesOrden",each Date.Year([Fecha])*100+Date.Month([Fecha]),Int64.Type)
in Orden
