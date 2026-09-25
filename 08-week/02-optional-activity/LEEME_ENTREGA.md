# Taller de ventas con Power BI

## Estado de la entrega

Se leyó exclusivamente el Excel de ventas y sus cuatro hojas. No se usaron el taller de notas ni las calificaciones. No se encontró Power BI Desktop en las rutas habituales, paquetes instalados ni procesos activos. Se entrega un **prototipo HTML funcional**, no un PBIX. `Tablero_prototipo.png` es una captura real de ese prototipo, no de Power BI. Las consultas M y las medidas DAX están preparadas, pero no ejecutadas en el motor de Power BI.

## Qué abrir

- `Informe_una_pagina.pdf`: tres hallazgos y decisiones; versión editable en `Informe_editable.md`.
- `Tablero_prototipo.html`: abrir en Edge o Chrome. Funciona sin Internet. Los cuatro filtros afectan todos los indicadores y gráficos. Restablecer recupera la vista completa.
- `PowerBI/`: consultas Power Query y medidas DAX listas para copiar al editor correspondiente.
- CSV: tablas agregadas para comprobar los resultados. `validacion.json` conserva los controles y la huella del original. `pruebas_prototipo.json` documenta pruebas ejecutadas del HTML.
- `taller_power_bi_datos_anonimizados.xlsx`: copia binaria exacta del original; no se ha reescrito ni modificado.

## Modelo y transformaciones

Grano: una fila por venta; 480 Venta_ID distintos. FactVentas conserva medidas aditivas, atributos de transacción y claves de dimensiones. DimFecha cubre todo 2026 para disponer de calendario continuo. DimCiudad, DimCanal y DimCategoria contienen valores únicos derivados del origen.

Relaciones activas, uno a muchos, dirección única de dimensión a hecho:

| Dimensión (lado 1) | Hecho (lado muchos) |
|---|---|
| DimFecha[Fecha] | FactVentas[Fecha] |
| DimCiudad[Ciudad] | FactVentas[Ciudad] |
| DimCanal[Canal] | FactVentas[Canal] |
| DimCategoria[Categoría] | FactVentas[Categoría] |

La carga selecciona la hoja Datos, promueve encabezados, omite solo filas completamente vacías, asigna tipos explícitos y recorta espacios. No elimina ventas duplicadas silenciosamente: detiene la consulta si Venta_ID se repite. Recalcula ingreso bruto, descuento, ingreso neto, costo total y margen desde las columnas base. Elimina Cliente_ID_Anonimo del modelo porque los tres escenarios principales no necesitan identificar clientes. La clasificación Nuevo/Recurrente se conserva como atributo de cada venta, no como prueba de retención longitudinal. Para las entregas no aplicables, conserva el cero original y crea una columna analítica de minutos nulos para excluirlas del promedio.

No se sustituyen nulos por ceros ni se imputan datos. En este archivo no se encontraron nulos, duplicados o dominios inválidos comprobados. No hay moneda identificada en el diccionario: todos los importes se muestran en UM. Una ciudad colombiana no prueba que los importes estén expresados en COP.

## Construcción en Power BI Desktop

1. Extraer el ZIP. Abrir Desktop y crear un archivo vacío. En Transformar datos, crear una consulta en blanco llamada `RutaExcel`; pegar `00_RutaExcel.pq` y cambiar únicamente la ruta por la ubicación del Excel extraído.
2. Crear consultas en blanco llamadas exactamente `FactVentas`, `DimFecha`, `DimCiudad`, `DimCanal` y `DimCategoria`. Pegar el archivo numerado correspondiente en cada editor avanzado. Cerrar y aplicar.
3. Crear las cuatro relaciones de la tabla anterior, marcar DimFecha como tabla de fechas usando Fecha, y ordenar DimFecha[Mes] por MesOrden. Ocultar Venta_ID, claves del hecho y columnas técnicas en la vista de informe. Desactivar la creación automática de fechas para este archivo si genera calendarios ocultos innecesarios.
4. Crear **cada medida por separado** desde `Medidas.dax`. El archivo contiene expresiones individuales, no una consulta DAX para ejecutar de una sola vez. Dar formato monetario sin símbolo a importes, entero a conteos y 0,00 % a tasas.
5. Crear una sola página personalizada de 1440 × 1200. Distribución: título y filtros arriba; cuatro tarjetas debajo; tres filas con dos visuales cada una. Usar fondo claro, tarjetas blancas y barras verde azulado. Agregar segmentadores Mes, Ciudad, Canal y Categoría desde sus dimensiones, con interacciones de filtrado hacia todos los visuales. Limitar el período observado a enero–agosto de 2026; no presentar meses posteriores como ventas reales en cero.

| Elemento | Campos y medidas |
|---|---|
| Tarjetas 1 a 4 | Ingreso neto; Margen bruto; Numero de ventas; Entregas tardias % |
| Línea mensual | Eje DimFecha[Mes]; valor Ingreso neto; orden por MesOrden |
| Barras de margen | Eje DimCategoria[Categoría]; valor Margen bruto; ordenar descendente; tooltip Margen % |
| Matriz canal y ciudad | Filas DimCiudad[Ciudad]; columnas DimCanal[Canal]; valor Ingreso neto |
| Barras de entregas | Eje DimCiudad[Ciudad]; valor Entregas tardias %; tooltips Entregas tardias, Entregas aplicables y Tiempo medio entrega |
| Barras de descuento | Eje FactVentas[Descuento_Pct]; valor Margen %; tooltips Unidades, Numero de ventas, Unidades por venta |
| Barras de pago | Eje FactVentas[Medio_Pago]; valor Ticket promedio; tooltips Numero de ventas y Satisfaccion media |

6. Actualizar. Verificar los totales siguientes y probar Web + Bogotá: 31 ventas, 17 tardías, 54,84 %. En Tienda, la tasa tardía y tiempo de entrega deben quedar en blanco/No aplica, nunca cero por sustitución. Verificar que cada segmentador modifica los seis visuales y las tarjetas. Guardar como PBIX y exportar una captura nativa solo después de estos controles.

## Controles numéricos

| Control | Valor |
|---|---:|
| Ventas únicas | 480 |
| Unidades | 1.260 |
| Ingreso bruto | 27.855.200 |
| Descuento monetario | 1.684.190 |
| Ingreso neto | 26.171.010 |
| Costo total | 16.734.700 |
| Margen bruto | 9.436.310 |
| Margen / ingreso neto | 36,06 % |
| Entregas aplicables | 290 |
| Entregas tardías | 73 |
| Tardías / aplicables | 25,17 % |

Los 2.400 valores monetarios se compararon fila a fila con cálculos decimales independientes, tolerancia 0,005 UM: cero discrepancias. Cada CSV debe reconciliar sus ingresos, margen, unidades y ventas con estos controles; los porcentajes y promedios se recalculan desde sus numeradores y denominadores, nunca se suman ni se promedian sin ponderar.

## Escenarios y límites de interpretación

1. **Ventas y rentabilidad:** Hogar lidera ingreso (9.406.345) y margen absoluto (3.314.545); Bebidas lidera margen % (42,99 %). Neiva aporta 7.098.055 de ingreso. Tienda aporta 11.547.030. Evidencia: categoria.csv, ciudad.csv, canal.csv, mensual.csv.
2. **Descuentos:** sin descuento hay 505/191 = 2,64 unidades por venta y 39,87 % de margen. Con 20 % hay 75/27 = 2,78 unidades por venta y 23,51 % de margen. La composición de productos puede explicar diferencias; no existe grupo experimental ni demanda contrafactual. Evidencia: descuentos.csv.
3. **Operación:** Web 50/165 = 30,30 % tardías; App 23/125 = 18,40 %. Web-Bogotá 17/31 = 54,84 %. Tiempo medio global: 52,91 minutos entre 290 entregas. No se deduce un umbral universal de tardanza: se respeta Estado_Entrega. Evidencia: operacion.csv y ciudad.csv.

Complementos descriptivos: 361/480 ventas están etiquetadas Recurrente (75,21 %); esto no equivale a una tasa de retención ni a 361 clientes distintos. En Tienda-Tarjeta el ticket es 65.230,23 sobre 44 ventas; Web-Tarjeta 54.909,08 sobre 60. No se infieren preferencias personales ni causalidad. Evidencia: recurrencia.csv y pago.csv.

Agosto termina el día 29 en el archivo; el mes no debe compararse como un cierre completo. No hay datos de metas, costos fijos, devoluciones o inventario: el margen bruto no equivale a utilidad neta y no se inventan objetivos de cumplimiento.

## Privacidad e integridad

No se incorporaron identidades ni fuentes externas. Los CSV y el HTML contienen agregaciones sin Venta_ID ni Cliente_ID_Anonimo. El original se incluye por solicitud del taller y conserva sus códigos ficticios. No se intentó reidentificar ni inferir atributos sensibles. Huella SHA-256 del archivo original y su copia: `cc3b824491761a30a445f1d965bc53d52e7f9a1e6a2f663d2fcc70f1ba81a2e9`.

## Referencias técnicas

Diseño contrastado con documentación oficial de Microsoft: [esquema estrella](https://learn.microsoft.com/power-bi/guidance/star-schema), [tablas de fechas](https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables) y [relaciones](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand). Estas referencias sustentan el modelo propuesto; los resultados provienen exclusivamente del Excel suministrado.
