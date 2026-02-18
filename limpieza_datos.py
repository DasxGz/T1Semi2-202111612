# T1 - Daniel Guzmán - 202111612
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 1. CARGA DEL DATASET
df_original = pd.read_csv('dataset_sucio.csv')
df = df_original.copy()

print("=" * 60)
print("   TAREA #1 - LIMPIEZA Y ANÁLISIS DE DATOS")
print("=" * 60)

print("\n📋 ESTADO ORIGINAL DEL DATASET")
print(f"  Filas       : {df.shape[0]}")
print(f"  Columnas    : {df.shape[1]}")
print(f"\n  Primeras 5 filas:")
print(df.head())

print(f"\n  Tipos de datos:")
print(df.dtypes)

print(f"\n  Valores nulos por columna:")
print(df.isnull().sum())

print(f"\n  Duplicados encontrados: {df.duplicated().sum()}")


# 2. ELIMINACIÓN DE DUPLICADOS

print("\n" + "=" * 60)
print("PASO 1: ELIMINACIÓN DE DUPLICADOS")
print("=" * 60)

duplicados_antes = df.duplicated().sum()
df = df.drop_duplicates()
duplicados_eliminados = duplicados_antes - df.duplicated().sum()
print(f"  Duplicados eliminados : {duplicados_eliminados}")
print(f"  Filas restantes       : {df.shape[0]}")


# 3. TRATAMIENTO DE VALORES FALTANTES / NULOS

print("\n" + "=" * 60)
print("PASO 2: TRATAMIENTO DE VALORES FALTANTES")
print("=" * 60)

nulos_antes = df.isnull().sum().sum()
print(f"  Valores nulos antes   : {nulos_antes}")

# Columna ciudad: reemplazar 'NA', '', espacios vacíos por NaN
df['ciudad'] = df['ciudad'].str.strip()
df['ciudad'] = df['ciudad'].replace({'NA': None, '': None, 'N/A': None})
df['ciudad'] = df['ciudad'].fillna('Desconocida')

# Rellenar género nulo con 'Desconocido'
df['genero'] = df['genero'].str.strip().str.upper()
df['genero'] = df['genero'].replace({'': None})
df['genero'] = df['genero'].fillna('Desconocido')

# Rellenar gasto_q nulo con la mediana
df['gasto_q'] = df['gasto_q'].astype(str).str.replace(',', '.').str.strip()
df['gasto_q'] = pd.to_numeric(df['gasto_q'], errors='coerce')
mediana_gasto = df['gasto_q'].median()
df['gasto_q'] = df['gasto_q'].fillna(mediana_gasto)
print(f"  Mediana usada para gasto_q nulo: Q{mediana_gasto:.2f}")

nulos_despues = df.isnull().sum().sum()
print(f"  Valores nulos después : {nulos_despues}")
print(f"  Valores recuperados   : {nulos_antes - nulos_despues}")


# 4. ESTANDARIZACIÓN DE FORMATOS

print("\n" + "=" * 60)
print("PASO 3: ESTANDARIZACIÓN DE FORMATOS")
print("=" * 60)

# --- nombre: eliminar espacios extras y capitalizar correctamente ---
df['nombre'] = df['nombre'].str.strip().str.title()

# --- genero: ya fue limpiado en paso 2 ---

# --- fecha_registro: múltiples formatos (YYYY-MM-DD y DD/MM/YYYY) ---
def parse_fecha(fecha):
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return pd.to_datetime(fecha, format=fmt)
        except:
            pass
    return pd.NaT

df['fecha_registro'] = df['fecha_registro'].apply(parse_fecha)
print(f"  Fechas no parseadas (NaT): {df['fecha_registro'].isna().sum()}")

# --- ciudad: capitalizar correctamente y eliminar espacios ---
df['ciudad'] = df['ciudad'].str.strip().str.title()

# --- categoria: estandarizar a Title Case y quitar espacios ---
df['categoria'] = df['categoria'].str.strip().str.title()

print(f"  Géneros únicos      : {sorted(df['genero'].dropna().unique())}")
print(f"  Ciudades únicas     : {sorted(df['ciudad'].dropna().unique())}")
print(f"  Categorías únicas   : {sorted(df['categoria'].dropna().unique())}")


# 5. ESTADO FINAL DEL DATASET LIMPIO

print("\n" + "=" * 60)
print("RESUMEN: ANTES vs DESPUÉS")
print("=" * 60)

resumen = {
    'Métrica': [
        'Filas totales',
        'Duplicados',
        'Valores nulos (gasto_q)',
        'Valores nulos (ciudad)',
        'Formatos de fecha mixtos',
        'Inconsistencias en género',
        'Inconsistencias en categoría',
        'Inconsistencias en ciudad',
    ],
    'Antes': [
        df_original.shape[0],
        df_original.duplicated().sum(),
        df_original['gasto_q'].isnull().sum(),
        df_original['ciudad'].isnull().sum() + (df_original['ciudad'].str.strip() == 'NA').sum() + (df_original['ciudad'].str.strip() == '').sum(),
        'Sí (YYYY-MM-DD / DD/MM/YYYY)',
        'Sí (m, f, M, F, con espacios)',
        'Sí (retail, RETAIL, Retail...)',
        'Sí (ANTIGUA, antigua, Antigua...)',
    ],
    'Después': [
        df.shape[0],
        df.duplicated().sum(),
        df['gasto_q'].isnull().sum(),
        df['ciudad'].isnull().sum(),
        'No (datetime unificado)',
        f'No ({", ".join(sorted(df["genero"].unique()))})',
        f'No ({", ".join(sorted(df["categoria"].unique()))})',
        'No (Title Case uniforme)',
    ]
}

df_resumen = pd.DataFrame(resumen)
print(df_resumen.to_string(index=False))


# 6. EXPORTAR DATASET LIMPIO

df.to_csv('dataset_limpio.csv', index=False)
print("\n Dataset limpio exportado: dataset_limpio.csv")


# 7. VISUALIZACIONES

print("\n Generando visualizaciones...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis del Dataset de Clientes - Guatemala\n(datos limpios)', fontsize=14, fontweight='bold', y=0.98)

colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4', '#E94F37']

# --- Gráfica 1: Distribución de clientes por ciudad ---
ciudad_counts = df['ciudad'].value_counts()
axes[0, 0].bar(ciudad_counts.index, ciudad_counts.values, color=colores[:len(ciudad_counts)])
axes[0, 0].set_title('Clientes por Ciudad', fontweight='bold')
axes[0, 0].set_xlabel('Ciudad')
axes[0, 0].set_ylabel('Cantidad de clientes')
axes[0, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(ciudad_counts.values):
    axes[0, 0].text(i, v + 5, str(v), ha='center', fontsize=8)

# --- Gráfica 2: Distribución de clientes por categoría ---
cat_counts = df['categoria'].value_counts()
axes[0, 1].pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%',
               colors=colores[:len(cat_counts)], startangle=90)
axes[0, 1].set_title('Distribución por Categoría', fontweight='bold')

# --- Gráfica 3: Histograma de gasto ---
axes[1, 0].hist(df['gasto_q'], bins=30, color='#2E86AB', edgecolor='white', alpha=0.85)
axes[1, 0].axvline(df['gasto_q'].mean(), color='red', linestyle='--', label=f'Media: Q{df["gasto_q"].mean():.2f}')
axes[1, 0].axvline(df['gasto_q'].median(), color='orange', linestyle='--', label=f'Mediana: Q{df["gasto_q"].median():.2f}')
axes[1, 0].set_title('Distribución del Gasto (Q)', fontweight='bold')
axes[1, 0].set_xlabel('Gasto en Quetzales')
axes[1, 0].set_ylabel('Frecuencia')
axes[1, 0].legend()

# --- Gráfica 4: Gasto promedio por categoría y género ---
pivot = df.groupby(['categoria', 'genero'])['gasto_q'].mean().unstack()
pivot.plot(kind='bar', ax=axes[1, 1], color=['#A23B72', '#2E86AB'], edgecolor='white')
axes[1, 1].set_title('Gasto Promedio por Categoría y Género', fontweight='bold')
axes[1, 1].set_xlabel('Categoría')
axes[1, 1].set_ylabel('Gasto Promedio (Q)')
axes[1, 1].tick_params(axis='x', rotation=30)
axes[1, 1].legend(title='Género')

plt.tight_layout()
plt.savefig('visualizaciones.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Visualizaciones guardadas: visualizaciones.png")


# 8. COMPARACIÓN: DATAFRAME ANTES vs DESPUÉS (muestra)

print("\n MUESTRA DATAFRAME ORIGINAL (primeras 5 filas):")
print(df_original.head().to_string())

print("\n MUESTRA DATAFRAME LIMPIO (primeras 5 filas):")
print(df.head().to_string())

print("\n Proceso de limpieza completado exitosamente.")


# El que copie esto es gei y therian :v
