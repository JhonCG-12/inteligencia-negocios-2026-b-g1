# Mini-ETL y primeras medidas — Corte 2

Autor: Jhon Sebastian Caviedes Guevara  
GitHub: JhonCG-12

## Proyecto preparado

`PowerBI/MiniETL.pbip` contiene el modelo con la consulta M, las tres medidas DAX y una página de informe con tres tarjetas, filtro de sucursal y tabla comparativa. Consulta `ABRIR_PROYECTO.md` para abrir, actualizar y guardar como PBIX. Se comprobaron la sintaxis JSON, referencias locales y cálculos independientes. La ejecución de Power Query/DAX y el renderizado **siguen pendientes de validación en Power BI Desktop**.

## Dataset y conexión

Archivo: `ventas_sucias.csv`. Es un dataset **sintético**, preparado con ayuda de IA para practicar limpieza. No proviene de una empresa ni contiene datos personales. Tiene 15 registros de ventas ficticias de artículos de papelería, incluyendo tres duplicados y diferencias de espacios y mayúsculas. Los importes están expresados en pesos colombianos (COP).

El grano final es **una venta de un solo producto por fila**, identificada por `Venta_ID`. Esta condición permite interpretar el promedio del importe como promedio por venta. No se debe extender esa interpretación a facturas con varias líneas sin ajustar el cálculo.

Conexión propuesta: Power BI Desktop → Obtener datos → Texto/CSV → seleccionar el archivo → delimitador punto y coma → Transformar datos. La consulta usa UTF-8 y configuración regional `es-CO` para interpretar fechas `dd/MM/yyyy` y decimales con coma. El código completo está en `consulta_power_query.m`; debe actualizarse la ruta local del CSV. La consulta debe llamarse **Ventas** antes de cargarla al modelo.

## Pasos aplicados definidos en Power Query

| Paso | Transformación y justificación |
| --- | --- |
| Origen | Conectar al CSV con delimitador `;` y codificación UTF-8. |
| Encabezados | Usar la primera fila como nombres de columnas. |
| Texto_limpio | Quitar espacios iniciales/finales y caracteres de control de identificador, sucursal y producto. Evita categorías distintas por espacios. |
| Texto_uniforme | Convertir sucursal y producto a mayúsculas. Unifica, por ejemplo, `neiva` y `NEIVA`. |
| Tipos_corregidos | Asignar fecha, entero a cantidad y decimal fijo a precio. Permite cálculos correctos y fechas ordenables. |
| Duplicados_eliminados | Quitar duplicados comparando **todas las columnas** después de normalizar. Reduce 15 filas a 12 sin borrar ventas distintas del mismo producto. |
| Importe_agregado | Agregar `Importe = Cantidad × Precio_Unitario`, de tipo decimal fijo. Es el ingreso de cada venta, sin descuentos ni impuestos adicionales. |
| Columna_condicional | Agregar `Segmento`: cantidad ≥ 3 corresponde a `Mayor volumen`; las demás, a `Menor volumen`. Es una regla didáctica explícita. |

Las seis transformaciones desde `Texto_limpio` hasta `Columna_condicional` cubren el mínimo de cuatro. Después, **Cerrar y aplicar** carga la tabla al modelo.

## Medidas DAX

Crear cada expresión por separado mediante **Nueva medida**, con la tabla llamada `Ventas`:

```dax
Total Ventas = SUM(Ventas[Importe])
```

Suma el ingreso de las ventas visibles en el contexto de filtro. Formato: moneda COP.

```dax
Promedio por Venta = AVERAGE(Ventas[Importe])
```

Calcula el promedio aritmético del importe de las filas visibles. Formato: moneda COP con dos decimales.

```dax
Ingreso por Unidad = DIVIDE([Total Ventas], SUM(Ventas[Cantidad]))
```

Divide el ingreso total entre las unidades vendidas dentro del mismo filtro. Es un precio promedio ponderado por cantidad, no un promedio simple de precios. `DIVIDE` devuelve un valor en blanco si el denominador es cero. Formato: moneda COP con dos decimales. Si Power BI usa separadores DAX locales, sustituir la coma entre argumentos por punto y coma.

## Contexto de filtro y valores esperados

Construir tres tarjetas con las medidas y una segmentación de datos con `Ventas[Sucursal]`. Agregar una tabla visual con sucursal y las tres medidas. No aplicar otros filtros durante la comprobación.

| Filtro | Filas | Unidades | Total Ventas (COP) | Promedio por Venta (COP) | Ingreso por Unidad (COP) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sin filtro | 12 | 25 | 270.000 | 22.500,00 | 10.800,00 |
| NEIVA | 4 | 8 | 85.000 | 21.250,00 | 10.625,00 |
| BOGOTA | 4 | 9 | 95.000 | 23.750,00 | 10.555,56 |
| PITALITO | 4 | 8 | 90.000 | 22.500,00 | 11.250,00 |

Estos valores se comprobaron de forma independiente sobre el CSV normalizado; **no son evidencia de ejecución de Power BI**. Al seleccionar NEIVA, `Total Ventas` debe cambiar de 270.000 a 85.000 COP porque la segmentación restringe las filas a esa sucursal. La fórmula no cambia; cambia el conjunto de datos sobre el que se evalúa. Al limpiar la selección, debe recuperar 270.000 COP.

## ETL steps & measures

The source is a synthetic CSV dataset with inconsistent text and three duplicate records. The Power Query script trims spaces and removes control characters from the text columns. It converts branch and product names to uppercase to standardize the categories. It assigns the correct data types to dates, quantities, and unit prices using the Colombian locale. It removes duplicate rows after text normalization and creates an amount column by multiplying quantity by unit price. It also creates a conditional column to classify sales by quantity. The Total Ventas measure uses SUM to calculate total revenue. The Promedio por Venta measure uses AVERAGE to calculate the mean amount per sale. The Ingreso por Unidad measure uses DIVIDE to calculate revenue per unit sold. Selecting a branch in the slicer changes the filter context and recalculates the measures for that branch.

## Evidencias y estado de entrega

Este paquete contiene los datos, la consulta, las expresiones y un proyecto Power BI (.pbip). **El archivo `.pbix` y las capturas deben agregarse después de abrir, actualizar y verificar el proyecto en Power BI.**

- [ ] Guardar `mini_etl.pbix` junto al README.
- [ ] Agregar `evidencias/01_origen.png`: conexión y datos originales.
- [ ] Agregar `evidencias/02_pasos.png`: tabla final de 12 filas y panel de pasos aplicados.
- [ ] Agregar `evidencias/03_sin_filtro.png`: tarjetas sin selección de sucursal.
- [ ] Agregar `evidencias/04_neiva.png`: las mismas tarjetas con NEIVA seleccionada.
- [ ] Agregar capturas de las tres fórmulas DAX, con nombre y expresión visibles.
- [ ] Actualizar estas casillas según lo que realmente se realizó.
- [ ] Verificar que el repo de perfil contiene el bloque CONFIG solicitado por la clase.
- [ ] Subir el trabajo dentro de la carpeta exacta de la semana correspondiente en el fork y comprobar los archivos en GitHub.

El enunciado no incluye el Manual de Entrega ni la ruta exacta de esta actividad. No se presupone una subcarpeta específica ni un formato exacto del bloque CONFIG. En el repositorio de perfil deben figurar `FULL_NAME = Jhon Sebastian Caviedes Guevara` y `GITHUB_USER = JhonCG-12` con la sintaxis indicada por el manual.

## Referencias técnicas

- [SUM — Microsoft Learn](https://learn.microsoft.com/en-us/dax/sum-function-dax)
- [AVERAGE — Microsoft Learn](https://learn.microsoft.com/en-us/dax/average-function-dax)
- [DIVIDE — Microsoft Learn](https://learn.microsoft.com/en-us/dax/divide-function-dax)
- [Power Query en Power BI Desktop — Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-query-overview)
