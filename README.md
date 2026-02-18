# Tarea #1 — Limpieza y Análisis Inicial de Datos con Python y Pandas
**T1-DanielGuzman-202111612 **

---

##  Dataset Utilizado

**Nombre:** `dataset_sucio.csv`  
**Descripción:** Dataset de clientes guatemaltecos con información sobre registros de compras, ciudades, géneros, categorías de consumo y gastos en Quetzales.  
**Registros originales:** 5,000 filas × 7 columnas  
**Columnas:** `id_cliente`, `nombre`, `genero`, `fecha_registro`, `gasto_q`, `ciudad`, `categoria`

---

##  Problemas Encontrados en el Dataset Original

| Problema | Descripción | Cantidad |
|---|---|---|
| Duplicados | Filas completamente repetidas | 100 |
| Valores nulos en `gasto_q` | Celdas vacías sin valor de gasto | 505 |
| Valores nulos/inválidos en `ciudad` | NaN, "NA", cadenas vacías | 227 |
| Valores nulos en `genero` | NaN y cadenas vacías | 60 |
| Formatos de fecha mixtos | `YYYY-MM-DD` y `DD/MM/YYYY` conviviendo | Todo el dataset |
| Inconsistencias en `genero` | `m`, `f`, `M`, `F`, con espacios | Todo el dataset |
| Inconsistencias en `categoria` | `retail`, `RETAIL`, `Retail`, `food`, `FOOD`... | Todo el dataset |
| Inconsistencias en `ciudad` | `ANTIGUA`, `antigua`, `Antigua`, con espacios | Todo el dataset |
| Nombres con formato variable | `ANA DIAZ`, `ana diaz`, `Ana Diaz` | Todo el dataset |
| Comas como separador decimal | `373,33` en lugar de `373.33` | Aprox. 40% de gasto_q |

---

##  Proceso de Limpieza Aplicado

### Paso 1 — Eliminación de Duplicados
Se utilizó `df.drop_duplicates()` para eliminar las **100 filas** que eran copia exacta de otra fila.  
Resultado: de 5,000 filas → **4,900 filas únicas**.

### Paso 2 — Tratamiento de Valores Faltantes
- **`gasto_q`:** Primero se convirtió la columna a numérico reemplazando comas por puntos. Los **505 valores nulos** se rellenaron con la **mediana (Q251.80)**, que es más robusta que la media ante valores atípicos.
- **`ciudad`:** Se reemplazaron cadenas `"NA"`, vacías y espacios en blanco por `NaN`, luego se imputaron con `"Desconocida"`. Se trataron **227 registros**.
- **`genero`:** Las celdas vacías y nulas (60 registros) se imputaron con `"Desconocido"`.

Resultado: **0 valores nulos** en todo el dataset limpio.

### Paso 3 — Estandarización de Formatos
- **`nombre`:** `.str.strip().str.title()` para eliminar espacios y normalizar mayúsculas.
- **`genero`:** `.str.strip().str.upper()` → valores únicos resultantes: `F`, `M`, `Desconocido`.
- **`fecha_registro`:** Se parsearon ambos formatos (`YYYY-MM-DD` y `DD/MM/YYYY`) a `datetime` usando una función personalizada. **0 fechas sin parsear**.
- **`ciudad`:** `.str.strip().str.title()` → 9 ciudades únicas normalizadas.
- **`categoria`:** `.str.strip().str.title()` → 4 categorías únicas: `Education`, `Food`, `Retail`, `Services`.

---

## Comparación: Antes vs. Después

| Métrica | Antes | Después |
|---|---|---|
| Filas totales | 5,000 | 4,900 |
| Duplicados | 100 | 0 |
| Nulos en `gasto_q` | 505 | 0 |
| Nulos/inválidos en `ciudad` | 227 | 0 |
| Nulos en `genero` | 60 | 0 |
| Formatos de fecha | Mixtos (2 formatos) | Unificado (datetime) |
| Inconsistencias en `genero` | m, f, M, F, con espacios | F, M, Desconocido |
| Inconsistencias en `categoria` | 12+ variantes | 4 categorías únicas |
| Inconsistencias en `ciudad` | Múltiples variantes | 9 ciudades en Title Case |

---

## Visualizaciones Generadas

> Archivo: `visualizaciones.png`

Las cuatro visualizaciones generadas fueron:

**1. Clientes por Ciudad**  
Gráfica de barras que muestra la distribución de los 4,900 clientes por ciudad. Guatemala, Quetzaltenango y Escuintla concentran el mayor número de clientes.

**2. Distribución por Categoría (pie chart)**  
Las cuatro categorías (Retail, Services, Food, Education) tienen una distribución bastante equilibrada, rondando el 25% cada una.

**3. Histograma de Gasto (Q)**  
La distribución del gasto tiende a ser relativamente uniforme entre Q0 y Q500. La media y mediana se encuentran alrededor de Q250, lo que indica pocos valores extremos.

**4. Gasto Promedio por Categoría y Género**  
El gasto promedio es similar entre géneros en todas las categorías. Education y Services muestran los gastos promedio ligeramente más altos.

---

##  Interpretación de Resultados

- El dataset presentaba **problemas de calidad significativos**: un 2% de duplicados, 10% de valores nulos en `gasto_q` y múltiples inconsistencias de formato que habrían distorsionado cualquier análisis sin limpieza previa.
- La imputación con mediana para `gasto_q` fue la decisión más adecuada dado que la distribución del gasto no es perfectamente normal y podría haber valores atípicos que sesguen la media.
- Tras la limpieza, el dataset está listo para análisis estadísticos confiables, modelos de segmentación de clientes o reportes de ventas por región/categoría.

---

##  Archivos del Proyecto

```
Tarea1/
├── limpieza_datos.py       # Script principal de limpieza y análisis
├── dataset_sucio.csv       # Dataset original (input)
├── dataset_limpio.csv      # Dataset depurado (output)
├── visualizaciones.png     # Gráficas generadas
└── README.md               # Este archivo
```

---

##  Tecnologías Utilizadas

- **Python 3**
- **Pandas** — limpieza, transformación y exploración de datos
- **Matplotlib / Seaborn** — visualizaciones