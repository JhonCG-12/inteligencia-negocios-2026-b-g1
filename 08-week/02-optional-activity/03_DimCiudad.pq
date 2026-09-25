let
    Dimension = Table.Sort(Table.Distinct(Table.SelectColumns(FactVentas, {"Ciudad"})),{{"Ciudad",Order.Ascending}})
in Dimension
