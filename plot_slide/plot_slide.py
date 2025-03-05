import plotly.graph_objects as go
import numpy as np

# Данные для всех точек (код точек остается тем же)
points = {
    'Традиционное литье': {
        'temp': 800,
        'trl': 9,
        'size': 45,
        'color': '#787878',
        'symbol': 'square'
    },
    'Направленная кристаллизация': {
        'temp': 850,
        'trl': 9,
        'size': 45,
        'color': '#505050',
        'symbol': 'square'
    },
    'GE Aviation': {
        'temp': 1000,
        'trl': 9,
        'size': 45,
        'color': '#1E88E5',
        'symbol': 'circle'
    },
    'Pratt & Whitney': {
        'temp': 850,
        'trl': 8,
        'size': 45,
        'color': '#43A047',
        'symbol': 'circle'
    },
    'Siemens': {
        'temp': 900,
        'trl': 7,
        'size': 45,
        'color': '#8E24AA',
        'symbol': 'circle'
    },
    'Текущее положение': {
        'temp': 1200,
        'trl': 5,
        'size': 55,
        'color': '#FFD700',
        'symbol': 'circle'
    },
    'Целевое положение': {
        'temp': 1200,
        'trl': 8,
        'size': 55,
        'color': '#FFD700',
        'symbol': 'circle'
    }
}

# Создание фигуры
fig = go.Figure()

# Добавление точек
for name, data in points.items():
    fig.add_trace(go.Scatter(
        x=[data['temp']],
        y=[data['trl']],
        mode='markers',
        name=name,
        marker=dict(
            size=data['size'],
            color=data['color'],
            symbol=data['symbol'],
            line=dict(color='white', width=2)
        ),
        hoverinfo='skip'
    ))

# Настройка макета с прозрачным фоном
fig.update_layout(
    xaxis=dict(
        title=dict(
            text='Температура работы турбины, °C',
            font=dict(size=50)
        ),
        gridcolor='lightgray',
        showgrid=True,
        showline=True,
        linewidth=2,
        linecolor='black',
        range=[700, 1300],
        tickfont=dict(size=40)
    ),
    yaxis=dict(
        title=dict(
            text='Уровень технологической готовности (TRL)',
            font=dict(size=50)
        ),
        gridcolor='lightgray',
        showgrid=True,
        showline=True,
        linewidth=2,
        linecolor='black',
        range=[4, 10],
        tickfont=dict(size=40)
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Прозрачный фон графика
    paper_bgcolor='rgba(0,0,0,0)',  # Прозрачный фон всего изображения
    showlegend=False,
    width=2000,
    height=1400,
    margin=dict(t=100, l=200, r=200, b=100),
)

# Сохранение графика
fig.write_html("technology_frontier.html")
fig.write_image("technology_frontier.png", scale=2)

# Показать график
fig.show()