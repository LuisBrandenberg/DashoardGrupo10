# Importamos las bibliotecas necesarias
import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Se setea la pantalla del dashboard para que este se vea mas amplio
st.set_page_config(layout="wide")

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

# Filtros
sucursal = st.multiselect("Selecciona sucursal:", df['Branch'].unique())
linea = st.multiselect("Selecciona línea de producto:", df['Product line'].unique())

# Texto dinámico para filtros
texto_sucursal = ", ".join(sucursal) if sucursal else "Todas las sucursales"
texto_linea = ", ".join(linea) if linea else "Todas las líneas de producto"

# Título principal del dashboard
st.title('📊 Dashboard de Análisis de Ventas')
st.write(f"Comportamiento de las ventas en: **{texto_sucursal}** | Línea de producto: **{texto_linea}**")

# Filtros
# Ambos
df_filter_full = df.copy()
if sucursal:
    df_filter_full = df_filter_full[df_filter_full['Branch'].isin(sucursal)]
if linea:
    df_filter_full = df_filter_full[df_filter_full['Product line'].isin(linea)]

# Sólo sucursal
# Se establece un filtro que solamente segmenta los datos por la variable sucursal
df_filter_sucursal = df.copy()
if sucursal:
    df_filter_sucursal = df_filter_sucursal[df_filter_sucursal['Branch'].isin(sucursal)]

# Sólo línea
# Se establece un filtro que solamente segmenta los datos por la variable línea de producto
df_filter_linea = df.copy()
if linea:
    df_filter_linea = df_filter_linea[df_filter_linea['Product line'].isin(linea)]

# Columnas para categorías
# Se crean 3 columnas para mostrar en cada una un tipo de grafico según el filtro que se le aplica
col_ambos, col_uno, col_nofiltro = st.columns(3)

# Títulos de sección
with col_ambos:
    st.markdown("### Filtrados por sucursal *y* línea de producto")
    st.markdown("---")  # Línea divisoria
with col_uno:
    st.markdown("### Filtrados solo por *una* dimensión")
    st.markdown("---")  # Línea divisoria
with col_nofiltro:
    st.markdown("### Sin filtros aplicados (no cambiarán si se filtran)")
    st.markdown("---")  # Línea divisoria

# === GRAFICOS FILTRADOS POR AMBOS FILTROS ===
with col_ambos:
    ## El gráfico de Total de ventas a través del tiempo se filtra tanto por sucursal como por linea de producto
    st.subheader("Total de Ventas a Través del Tiempo")
    daily_total = df_filter_full.groupby('Date')['Total'].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_total.index, daily_total.values, marker='o')
    ax.set_title('Total diario')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("*Muestra cómo han variado las ventas totales (Total) a lo largo del tiempo (Date).*")
    
    ## El gráfico que compara el gasto por tipo de cliente también se filtra por sucursal y línea de producto
    st.subheader("Comparación del Gasto por Tipo de Cliente")
    df_filtered_clients = df_filter_full.copy()
    members = df_filtered_clients[df_filtered_clients['Customer type'] == 'Member']['Total']
    normals = df_filtered_clients[df_filtered_clients['Customer type'] == 'Normal']['Total']
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.hist(members, bins=15, alpha=0.6, label='Member', color='cornflowerblue', edgecolor='black')
    ax4.hist(normals, bins=15, alpha=0.6, label='Normal', color='salmon', edgecolor='black')
    ax4.set_title('Distribución del gasto total por tipo de cliente')
    ax4.set_xlabel('Total gastado')
    ax4.set_ylabel('Número de clientes')
    ax4.legend()
    ax4.grid(axis='y')
    st.pyplot(fig4)
    st.write("*Compara la distribución del gasto total (Total) entre clientes Member y Normal.*")

    ## El gráfico que muestra la disrtuibución por método de pago también se filtra por sucursal y línea de producto
    st.subheader("Distribución de métodos de pago")
    payment_counts = df_filter_full['Payment'].value_counts()
    fig6, ax6 = plt.subplots(figsize=(7, 7))
    ax6.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=90,
            colors=plt.cm.Pastel1.colors, wedgeprops={'edgecolor': 'white'})
    ax6.set_title('Proporción de métodos de pago')
    st.pyplot(fig6)
    st.write("*Identifica los métodos de pago (Payment) más frecuentes.*")

# === GRAFICOS FILTRADOS POR UNA DIMENSIÓN ===
with col_uno:
    ## En este caso no tiene sentido filtrar por línea de producto, por lo que el grafico de ingreso solo se filtra por sucursal
    st.subheader("Ingresos por Línea de Producto")
    ## Se crea una nueva variable con el data frame filtrado solo por la sucursal
    product_totals = df_filter_sucursal.groupby('Product line')['Total'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    product_totals.plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_title('Total de ingresos por línea de producto')
    ax2.set_xlabel('Línea de producto')
    ax2.set_ylabel('Total de ingresos')
    ax2.grid(axis='y')
    st.pyplot(fig2)
    st.write("*Compara los ingresos (Total) generados por cada Product line.*")
    
    ## En este caso no tiene sentido filtrar por línea de producto, por lo que el 
    ## grafico de calificación de clientes solo se filtra por sucursal
    st.subheader("Distribución de la Calificación de Clientes")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.hist(df_filter_sucursal['Rating'], bins=10, color='mediumseagreen', edgecolor='black')
    ax3.set_title('Distribución de calificaciones')
    ax3.set_xlabel('Calificación')
    ax3.set_ylabel('Número de clientes')
    ax3.grid(axis='y')
    st.pyplot(fig3)
    st.write("*Analiza la distribución de las calificaciones (Rating) de los clientes.*")

    ## En este caso no tiene sentido filtrar por sucursal ya que se habla de ingreso bruto, por lo que el 
    ## grafico de calificación de clientes solo se filtra por la línea de producto
    st.subheader("Relación entre COGS y Gross Income")
    x = df_filter_linea['cogs']
    y = df_filter_linea['gross income']
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    ax5.scatter(x, y, alpha=0.7, color='darkcyan', edgecolors='w', label='Datos')
    if not x.empty and not y.empty:
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ax5.plot(x, y_pred, color='red', linewidth=2, label='Línea de tendencia')
    ax5.set_title('Relación entre COGS y Gross Income')
    ax5.set_xlabel('Costo de bienes vendidos (COGS)')
    ax5.set_ylabel('Ingreso bruto (Gross Income)')
    ax5.grid(True)
    ax5.legend()
    st.pyplot(fig5)
    st.write("*Visualiza la relación entre el costo de bienes vendidos (COGS) y el ingreso bruto (Gross Income), incluyendo una línea de tendencia.*")

# === GRAFICOS SIN FILTRO ===
with col_nofiltro:
    ## Para el grafico que establece la correlación entre variables no se realiza filtro
    st.subheader("Relaciones lineales entre variables numéricas")
    numeric_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    corr_matrix = df[numeric_cols].corr()
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax7)
    ax7.set_title('Matriz de correlación entre variables numéricas')
    st.pyplot(fig7)
    st.write("*Explora relaciones lineales entre variables numéricas.*")

    ## El siguiente gráfico no se puede filtrar pues establece una comparación entre la línea y la sucursal
    st.subheader("Proporción (%) de Product line en el gross income por Branch")
    contrib_raw = df.groupby(['Branch', 'Product line'])['gross income'].sum().unstack(fill_value=0)
    contrib_percent = contrib_raw.div(contrib_raw.sum(axis=1), axis=0) * 100
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

