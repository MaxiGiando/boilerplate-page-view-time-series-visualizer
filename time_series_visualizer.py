import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Importar y preparar los datos
df = pd.read_csv(
    'fcc-forum-pageviews.csv', 
    parse_dates=['date'], 
    index_col='date'
)

# 2. Limpiar los datos
# CORRECCIÓN: Reasignar a 'df' para que los cambios se apliquen globalmente.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # 3. Dibujar el gráfico de líneas
    
    # Usar una copia para no modificar el DataFrame original
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Guardar y devolver la imagen
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 4. Dibujar el gráfico de barras

    # Usar una copia y extraer año/mes
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupar y preparar los datos
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Dibujar el gráfico
    fig = df_bar.plot(kind='bar', figsize=(10, 6), legend=True).get_figure()
    
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(
        title='Months',
        labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    )

    # Guardar y devolver la imagen
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # 5. Dibujar los diagramas de caja

    # Preparar los datos
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Crear la figura con dos subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    # Gráfico 1: Year-wise Box Plot
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Gráfico 2: Month-wise Box Plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(data=df_box, x='month', y='value', order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Guardar y devolver la imagen
    fig.savefig('box_plot.png')
    return fig