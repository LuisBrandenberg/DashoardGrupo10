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

# Se despliega la información de la tabla para conocer la data
df.head()

# Se visualiza la información realacionada al DATASET para identificar las
# variables y establecer los gáficos a utilizar
# df.info()
# df.describe()
# print(df.columns)

### GRAFICO 1. TOTAL VENTAS A TRAVES DEL TIEMPO ###
# Convertir 'Date' a datetime
df['Date'] = pd.to_datetime(df['Date'])

# Agrupar por fecha y sumar 'Total'
daily_total = df.groupby('Date')['Total'].sum()

# Mostrar DataFrame (opcional)
st.subheader("Vista previa de los datos agrupados")
st.dataframe(daily_total.reset_index())

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
    
st.subheader("Ingresos por línea de producto")

# Agrupar por Product line y sumar Total
product_totals = df.groupby('Product line')['Total'].sum().sort_values(ascending=False)

# Crear gráfico de barras
fig2, ax2 = plt.subplots(figsize=(10, 5))
product_totals.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_title('Total de ingresos por línea de producto')
ax2.set_xlabel('Línea de producto')
ax2.set_ylabel('Total de ingresos')
ax2.grid(axis='y')

# Mostrar gráfico en Streamlit
st.pyplot(fig2)
st.write("*Compara los ingresos (Total) generados por cada Product line.*")

### GRAFICO 3. Distribución de la Calificación de Clientes ###

st.subheader("Distribución de calificaciones de los clientes")

# Crear histograma
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.hist(df['Rating'], bins=10, color='mediumseagreen', edgecolor='black')
ax3.set_title('Distribución de calificaciones')
ax3.set_xlabel('Calificación')
ax3.set_ylabel('Número de clientes')
ax3.grid(axis='y')

# Mostrar gráfico
st.pyplot(fig3)
st.write("*Analiza la distribución de las calificaciones (Rating) de los clientes.*")

### GRAFICO 4.Comparación del Gasto por Tipo de Cliente ###

st.subheader("Distribución del gasto total por tipo de cliente")

# Separar por tipo de cliente
members = df[df['Customer type'] == 'Member']['Total']
normals = df[df['Customer type'] == 'Normal']['Total']

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

### GRAFICO 5.Relación entre Costo y Ganancia Bruta ###

st.subheader("Gráfico 5: Relación entre COGS y Gross Income")

fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.scatter(df['cogs'], df['gross income'], alpha=0.7, color='darkcyan', edgecolors='w')
ax5.set_title('Relación entre COGS y Gross Income')
ax5.set_xlabel('Costo de bienes vendidos (COGS)')
ax5.set_ylabel('Ingreso bruto (Gross Income)')
ax5.grid(True)

st.pyplot(fig5)
st.write("*Visualiza la relación entre el costo de bienes vendidos (cogs) y el ingreso bruto (gross income).*")

### GRAFICO 6.Metodos de pago preferidos ###

st.subheader("Gráfico 6: Distribución de métodos de pago")

# Contar frecuencia de cada método de pago
payment_counts = df['Payment'].value_counts()

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

