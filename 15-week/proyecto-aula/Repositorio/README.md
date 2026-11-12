# Café Horizonte del Sur

Proyecto de aula de Inteligencia de Negocios. Caso ficticio con datos sintéticos de enero a diciembre de 2025.

## Ficha del proyecto

| Campo | Descripción |
|---|---|
| Integrantes | Completar con uno o dos nombres según la inscripción del proyecto |
| Empresa | Café Horizonte del Sur, comercializadora ficticia de café del Huila |
| Actividad | Venta de café tostado en tres sedes y tres canales: tienda, domicilios y mayorista |
| Problema | En el escenario simulado, la gerencia asigna promociones por volumen vendido y desconoce el margen que obtiene en cada producto y canal |
| Pregunta | ¿Cómo varía el margen bruto porcentual por producto y canal durante 2025? |
| KPI principal | Margen bruto porcentual = 100 × (ventas netas − costo total) ÷ ventas netas |
| KPI de apoyo | Ventas netas y ticket promedio |
| Decisión | Priorizar productos y canales para una campaña comercial con base en margen, utilidad y volumen |
| Fuentes | Cuatro CSV sintéticos en la carpeta `datos`, generados con Python |
| Autorización | No aplica al caso ficticio |

Cada fila de `ventas.csv` representa una línea de una factura. Una factura puede tener varias líneas. La clave de línea es la combinación de `FacturaID` y `Linea`. La sede, la fecha y el canal se mantienen iguales entre las líneas de una misma factura.

## Datos y reglas de generación

El script [generar_datos.py](generar_datos.py) reproduce los datos con semilla fija 20261108. Simula 12 productos, tres sedes, tres canales y 12 meses. La demanda de cada producto tiene un peso distinto. Noviembre y diciembre tienen más facturas y más promociones. Las órdenes mayoristas tienen mayores cantidades por línea y menor precio unitario. Los precios y costos dependen de la presentación. El costo aumenta de forma gradual en el periodo simulado.

Todos los importes están en pesos colombianos. El descuento es el importe **total por línea**. En una venta de dos unidades a 59.200 COP con descuento de 5.920 COP, la venta neta de la línea es 112.480 COP. El ticket promedio divide ventas netas entre facturas distintas.

| Problema introducido | Tratamiento en Power Query |
|---|---|
| 24 copias exactas de líneas | Quitar duplicados por factura y número de línea |
| Fechas de origen con formatos `aaaa-mm-dd` y `dd/mm/aaaa` | Interpretar cada formato explícitamente y asignar tipo fecha |
| Canales con espacios o uso variable de mayúsculas | Recortar espacios y convertir a mayúsculas |

Los valores de control se calculan sobre las filas válidas del generador, antes de introducir problemas de calidad. Úsalos como referencia independiente para comprobar el ETL y las medidas de Power BI.

## Diccionario de datos

| Tabla | Campo | Tipo tras ETL | Descripción | Ejemplo |
|---|---|---|---|---|
| Ventas | FacturaID | Texto | Identificador global de la factura | F000001 |
| Ventas | Linea | Entero | Posición dentro de la factura | 1 |
| Ventas | Fecha | Fecha | Día de la venta | 01/01/2025 |
| Ventas | ProductoID | Texto | Código del producto vendido | P12 |
| Ventas | SedeID | Texto | Código de sede | S03 |
| Ventas | Canal | Texto | Canal normalizado | TIENDA |
| Ventas | Cantidad | Entero | Unidades de la presentación vendida | 2 |
| Ventas | PrecioUnitarioCOP | Entero | Precio de una unidad antes del descuento | 59200 |
| Ventas | DescuentoCOP | Entero | Descuento de toda la línea en COP | 5920 |
| Ventas | CostoUnitarioCOP | Entero | Costo de una unidad en COP | 37800 |
| Productos | ProductoID | Texto | Código único de la presentación | P12 |
| Productos | Producto | Texto | Nombre comercial | Microlote Niebla |
| Productos | Categoria | Texto | Familia del producto | Microlote |
| Productos | Presentacion | Texto | Tamaño de la presentación | 500 g |
| Productos | ProductoCompleto | Texto | Nombre y presentación para distinguir el producto | Microlote Niebla 500 g |
| Sedes | SedeID | Texto | Código único de la sede | S03 |
| Sedes | Sede | Texto | Nombre de la sede | Garzón Centro |
| Sedes | Municipio | Texto | Municipio de la sede | Garzón |
| Canales | Canal | Texto | Nombre único del canal | TIENDA |
| Calendario | Date | Fecha | Día del calendario con el que se relacionan las ventas | 01/01/2025 |
| Calendario | Año | Entero | Año de la fecha | 2025 |
| Calendario | Trimestre | Texto | Trimestre de la fecha | T1 |
| Calendario | Mes | Texto | Nombre del mes | enero |
| Calendario | NumeroMes | Entero | Posición del mes para ordenar el eje | 1 |

## Evidencias y validación

El modelo de Power BI usa los cuatro CSV de origen incorporados en el archivo para que pueda abrirse sin rutas locales. [Power Query](PowerQuery.md) describe una forma de reconstruir las transformaciones desde los CSV. [Modelo y medidas DAX](Medidas-DAX.md) documenta las relaciones, las seis medidas y los filtros. [Cifras de control](controles.csv) contiene los valores calculados por separado.

- [Captura 01 Tablero total](evidencias/01-Tablero-total.jpg)
- [Captura 02 Modelo estrella](evidencias/02-Modelo-estrella.jpg)
- [Captura 03 ETL antes de limpiar](evidencias/03-ETL-antes-de-limpiar.jpg)
- [Captura 04 ETL fechas convertidas](evidencias/04-ETL-fechas-convertidas.jpg)
- [Captura 05 ETL canales normalizados](evidencias/05-ETL-canales-normalizados.jpg)
- [Captura 06 ETL lineas unicas](evidencias/06-ETL-lineas-unicas.jpg)
- [Captura 07 Clic domicilios](evidencias/07-Clic-domicilios.jpg)
- [Captura 08 Clic pitalito](evidencias/08-Clic-pitalito.jpg)
- [Captura 09 Clic noviembre](evidencias/09-Clic-noviembre.jpg)
- [Captura 10 Jerarquia producto](evidencias/10-Jerarquia-producto.jpg)

## Overview & insights

Café Horizonte del Sur is a fictional coffee retailer in Huila that needs to decide which products and sales channels to prioritize in its next commercial campaign. The dataset covers January through December 2025 and uses one invoice line as its grain. In Power Query, the ETL standardizes dates and channel names and removes 24 duplicated lines, leaving 2,840 lines across 1,625 invoices. The star schema connects the Sales fact table to Product, Store, Channel, and Calendar dimensions. Overall gross margin was 32.05% on COP 226,811,099 in net sales in the simulated dataset. Wholesale generated the largest gross profit, COP 33,007,407, while its 28.64% gross margin was the lowest across the three channels. Café de la Casa 500 g generated COP 3,499,808 in gross profit in the store channel at a 37.15% gross margin. The commercial team should run a four-week store pilot for that product and compare incremental profit after campaign costs with a comparable period before expanding it.
