# Puntualidad en entregas de última milla

**Inteligencia de Negocios · Corte 3 · Semana 4 del corte**

Informe interactivo de Power BI sobre **6.045 pedidos simulados** en seis municipios del Huila durante 2025. Cada fila del [archivo de datos](datos-entregas.csv) representa un pedido y contiene las horas prometidas y las horas reales de entrega. Un pedido se cuenta como tardío cuando las horas reales superan las prometidas. La tasa de tardanza es el número de pedidos tardíos dividido entre todos los pedidos de la selección.

Abre [Entregas-Semana-4.pbix](Entregas-Semana-4.pbix) en Power BI Desktop. El informe tiene los datos incorporados.

## Recorrido del tablero

| Vista | Dato destacado | Cómo explorarlo |
| --- | --- | --- |
| **01 · Contexto** | Diciembre registró el mayor volumen, con **707 pedidos**. | Las columnas mensuales muestran el volumen en orden cronológico. Selecciona un mes para actualizar las tarjetas. |
| **02 · Hallazgo** | **25,2 %** de los pedidos de Conexión Sur llegaron tarde, frente a **17,9 %** en el total del caso. | Las barras comparan tasas por transportadora. La línea muestra la evolución mensual de pedidos tardíos. Las barras por ubicación permiten bajar de zona a ciudad. |
| **03 · Recomendación** | Neiva registró **213 pedidos tardíos de 660** de Conexión Sur, el mayor conteo de esa transportadora por ciudad. | Las barras ordenan las ciudades por pedidos tardíos. Selecciona una para consultar su volumen y su tasa en las tarjetas. |

Los destacados de las tres vistas corresponden al total de 2025. Las tarjetas y los gráficos responden a las selecciones dentro de su página. Los ejes cuantitativos comienzan en cero y las barras comparativas se ordenan de mayor a menor.

## Comprobación de la interactividad

En **02 · Hallazgo**, parte con ambos segmentadores limpios. Las tarjetas muestran pedidos, tardíos y tasa de tardanza, en ese orden.

| Acción | Pedidos | Tardíos | Tasa |
| --- | ---: | ---: | ---: |
| Sin selección | 6.045 | 1.081 | 17,9 % |
| Selecciona **T4** en el segmentador Trimestre | 1.894 | 398 | 21,0 % |
| Mantén **T4** y elige **Exprés** en Servicio | 606 | 140 | 23,1 % |
| Mantén los dos segmentadores y selecciona la barra de **Conexión Sur** | 230 | 72 | 31,3 % |
| Borra todas las selecciones y luego selecciona solo **Conexión Sur** | 2.264 | 571 | 25,2 % |

Al seleccionar la barra de Conexión Sur, comprueba que cambien la línea mensual, el gráfico de zonas y las tarjetas. Conserva la selección de la transportadora con los segmentadores limpios. En **Pedidos tardíos por zona y ciudad**, haz clic derecho en la barra **Centro** y selecciona **Explorar en profundidad**. El gráfico debe mostrar **Neiva (213)** y **Garzón (70)**. Usa la flecha hacia arriba para regresar a zonas.

En **03 · Recomendación**, con los segmentadores limpios, selecciona **Neiva**. Las tarjetas de Conexión Sur deben mostrar **660 pedidos**, **213 tardíos** y **32,3 %** de tardanza.

La combinación de segmentadores, el filtrado cruzado y el desglose se comprobaron en Power BI Desktop. Los resultados de referencia se calcularon por separado a partir del CSV.

## Dashboard & insight

This Power BI report tracks delivery volume and service-level performance for 6,045 simulated last-mile orders across six municipalities in Huila during 2025. Monthly columns show that December had the highest volume, with 707 orders. The carrier comparison shows that Conexión Sur had the highest late delivery rate at 25.2%, compared with 17.9% overall. The geographic drill-down and city ranking show that Neiva accounted for 213 of Conexión Sur's late deliveries, out of 660 orders handled by that carrier in the city. Quarter and service slicers let users narrow the analysis, and selecting a carrier cross-filters the monthly trend and geographic breakdown. The operations team should run a four-week pilot in Neiva to flag orders close to their promised deadline and confirm that they are dispatched. The pilot should aim to lower the late delivery rate by five percentage points against the preceding four weeks, with results reported separately for standard and express services alongside order volumes.
