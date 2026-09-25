let
    Dimension = Table.Sort(Table.Distinct(Table.SelectColumns(FactVentas, {"Canal"})),{{"Canal",Order.Ascending}})
in Dimension
