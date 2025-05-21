# Importamos las bibliotecas necesarias
import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Función para cargar datos con cache para mejorar rendimiento
@st.cache_data

#from google.colab import files
#files.upload()

def cargar_datos():
    # Carga el archivo CSV con datos macroeconómicos
    df = pd.read_csv("data.csv")
    return df

# Cargamos los datos
df = cargar_datos()

# Convertir 'Date' a datetime
df['Date'] = pd.to_datetime(df['Date'])

# Se despliega la información de la tabla para conocer la data
# df.head()

# Se visualiza la información realacionada al DATASET para identificar las
# variables y establecer los gáficos a utilizar
# df.info()
# df.describe()
# print(df.columns)


# Filtros
sucursal = st.multiselect("Selecciona sucursal:", df['Branch'].unique())
linea = st.multiselect("Selecciona línea de producto:", df['Product line'].unique())

# Filtro para el gráfico 1 (ambos filtros)
df_filter_full = df.copy()
if sucursal:
    df_filter_full = df_filter_full[df_filter_full['Branch'].isin(sucursal)]
if linea:
    df_filter_full = df_filter_full[df_filter_full['Product line'].isin(linea)]

### GRAFICO 1. TOTAL VENTAS A TRAVES DEL TIEMPO ###
st.subheader("Gráfico 1: Total de Ventas a Través del Tiempo")

# Agrupar por fecha y sumar 'Total'
daily_total = df_filter_full.groupby('Date')['Total'].sum()

# Crear gráfico
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_total.index, daily_total.values, marker='o')
ax.set_title('Total diario')
ax.set_xlabel('Fecha')
ax.set_ylabel('Total')
ax.grid(True)
plt.xticks(rotation=45)

# Mostrar gráfico
st.pyplot(fig)
st.write("*Muestra cómo han variado las ventas totales (Total) a lo largo del tiempo (Date).*")

### GRAFICO 2. Ingresos por Línea de Producto ###
st.subheader("Gráfico 2: Ingresos por Línea de Producto")

# Filtro solo por sucursal
df_filter_sucursal = df.copy()
if sucursal:
    df_filter_sucursal = df_filter_sucursal[df_filter_sucursal['Branch'].isin(sucursal)]

# Agrupar por Product line y sumar Total
product_totals = df_filter_sucursal.groupby('Product line')['Total'].sum().sort_values(ascending=False)

# Crear gráfico de barras
fig2, ax2 = plt.subplots(figsize=(10, 5))
product_totals.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_title('Total de ingresos por línea de producto')
ax2.set_xlabel('Línea de producto')
ax2.set_ylabel('Total de ingresos')
ax2.grid(axis='y')

# Mostrar gráfico
st.pyplot(fig2)
st.write("*Compara los ingresos (Total) generados por cada Product line.*")

### GRAFICO 3. Distribución de la Calificación de Clientes ###
st.subheader("Gráfico 3: Distribución de la Calificación de Clientes")

# Crear histograma con filtro por sucursal
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.hist(df_filter_sucursal['Rating'], bins=10, color='mediumseagreen', edgecolor='black')
ax3.set_title('Distribución de calificaciones')
ax3.set_xlabel('Calificación')
ax3.set_ylabel('Número de clientes')
ax3.grid(axis='y')

# Mostrar gráfico
st.pyplot(fig3)
st.write("*Analiza la distribución de las calificaciones (Rating) de los clientes.*")

### GRAFICO 4. Comparación del Gasto por Tipo de Cliente ###

st.subheader("Gráfico 4: Comparación del Gasto por Tipo de Cliente")

# Usar el DataFrame con ambos filtros aplicados
df_filtered_clients = df.copy()
if sucursal:
    df_filtered_clients = df_filtered_clients[df_filtered_clients['Branch'].isin(sucursal)]
if linea:
    df_filtered_clients = df_filtered_clients[df_filtered_clients['Product line'].isin(linea)]

# Separar por tipo de cliente
members = df_filtered_clients[df_filtered_clients['Customer type'] == 'Member']['Total']
normals = df_filtered_clients[df_filtered_clients['Customer type'] == 'Normal']['Total']

# Crear histograma comparativo
fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.hist(members, bins=15, alpha=0.6, label='Member', color='cornflowerblue', edgecolor='black')
ax4.hist(normals, bins=15, alpha=0.6, label='Normal', color='salmon', edgecolor='black')
ax4.set_title('Distribución del gasto total por tipo de cliente')
ax4.set_xlabel('Total gastado')
ax4.set_ylabel('Número de clientes')
ax4.legend()
ax4.grid(axis='y')

# Mostrar gráfico en Streamlit
st.pyplot(fig4)
st.write("*Compara la distribución del gasto total (Total) entre clientes Member y Normal.*")


### GRAFICO 5. Relación entre Costo y Ganancia Bruta ###

st.subheader("Gráfico 5: Relación entre COGS y Gross Income")

# Filtrar solo por línea de producto
df_filter_linea = df.copy()
if linea:
    df_filter_linea = df_filter_linea[df_filter_linea['Product line'].isin(linea)]

# Crear gráfico de dispersión con línea de tendencia
fig5, ax5 = plt.subplots(figsize=(10, 6))

# Variables
x = df_filter_linea['cogs']
y = df_filter_linea['gross income']

# Gráfico de dispersión
ax5.scatter(x, y, alpha=0.7, color='darkcyan', edgecolors='w', label='Datos')

# Línea de tendencia
if not x.empty and not y.empty:
    # Ajustar regresión lineal
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    ax5.plot(x, y_pred, color='red', linewidth=2, label='Línea de tendencia')

# Personalización
ax5.set_title('Relación entre COGS y Gross Income')
ax5.set_xlabel('Costo de bienes vendidos (COGS)')
ax5.set_ylabel('Ingreso bruto (Gross Income)')
ax5.grid(True)
ax5.legend()

# Mostrar gráfico
st.pyplot(fig5)
st.write("*Visualiza la relación entre el costo de bienes vendidos (COGS) y el ingreso bruto (Gross Income), incluyendo una línea de tendencia.*")

### GRAFICO 6. Métodos de pago preferidos ###

st.subheader("Gráfico 6: Distribución de métodos de pago")

# Filtrar solo por sucursal
df_filter_sucursal = df.copy()
if sucursal:
    df_filter_sucursal = df_filter_sucursal[df_filter_sucursal['Branch'].isin(sucursal)]

# Contar frecuencia de cada método de pago
payment_counts = df_filter_sucursal['Payment'].value_counts()

# Crear gráfico de pastel
fig6, ax6 = plt.subplots(figsize=(7, 7))
ax6.pie(
    payment_counts,
    labels=payment_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Pastel1.colors,
    wedgeprops={'edgecolor': 'white'}
)
ax6.set_title('Proporción de métodos de pago')

# Mostrar en Streamlit
st.pyplot(fig6)
st.write("*Identifica los métodos de pago (Payment) más frecuentes.*")

### GRAFICO 7. Análisis de Correlación Numérica ###   
    
st.subheader("Gráfico 7: Relaciones lineales entre variables numéricas")

# Seleccionar solo las columnas numéricas relevantes
numeric_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
corr_matrix = df[numeric_cols].corr()

# Crear mapa de calor
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax7)
ax7.set_title('Matriz de correlación entre variables numéricas')

st.pyplot(fig7)
st.write("*Explora relaciones lineales entre variables numéricas.*")

### GRAFICO 8.Composición del Ingreso Bruto por Sucursal y Línea de Producto ###

st.subheader("Gráfico 8: Proporción (%) de Product line en el gross income por Branch")

# Agrupar datos y calcular proporciones
contrib_raw = df.groupby(['Branch', 'Product line'])['gross income'].sum().unstack(fill_value=0)
contrib_percent = contrib_raw.div(contrib_raw.sum(axis=1), axis=0) * 100  # convertir a porcentajes

# Crear gráfico apilado porcentual
fig8, ax8 = plt.subplots(figsize=(10, 6))
contrib_percent.plot(kind='bar', stacked=True, ax=ax8, colormap='tab20')
ax8.set_title('Distribución porcentual del gross income por línea de producto en cada sucursal')
ax8.set_xlabel('Sucursal (Branch)')
ax8.set_ylabel('Porcentaje (%) del ingreso bruto')
ax8.legend(title='Product line', bbox_to_anchor=(1.05, 1), loc='upper left')
ax8.set_ylim(0, 100)
ax8.grid(axis='y')

st.pyplot(fig8)
st.write("*Muestra la contribución de cada Product line al gross income dentro de cada Branch.*")

# Pie de página simple
st.markdown("---")
st.caption("Dashboard de Análisis de Ventas Simple | Datos: datos.csv")

