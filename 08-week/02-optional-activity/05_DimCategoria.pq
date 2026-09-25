let
    Dimension = Table.Sort(Table.Distinct(Table.SelectColumns(FactVentas, {"Categoría"})),{{"Categoría",Order.Ascending}})
in Dimension
