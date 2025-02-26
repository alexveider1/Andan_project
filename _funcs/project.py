import requests
import os
import sys
from time import sleep

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib_inline
import seaborn as sns
import scipy.stats as sts
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, confusion_matrix

sns.set_theme()
matplotlib_inline.backend_inline.set_matplotlib_formats('svg')

"""
Модуль для основной части проекта, для построения разного рода визуализаций с помощью библиотек `matplotlib`, `seaborn`, `plotly` и `plotly dash`. 
"""


def draw_player(ID: int, players: pd.DataFrame, game=None) -> None:
    """
    Функция для отрисовки фото игрока с ID = `ID` для игры `game` по данным из `players`.
    """
    rows = players[players['ID'] == ID].sort_values(by='game', ascending=False)
    assert rows.shape[0] > 0, print('Укажите верный ID')
    if game is None:
        rows = rows.iloc[0]
        game = rows['game']
    else:
        game = game
        rows = rows[rows['game'] == game].iloc[0]
    ID = str(ID).rjust(6, '0')
    if not os.path.isfile(f'cache\\FIFA{game}-player-{ID}.png'):
        ref = f"https://cdn.sofifa.net/players/{ID[:3]}/{ID[3:]}/{str(game).rjust(2, '0')}_360.png"
        photo = requests.get(ref, stream=True)
        if photo.status_code == 200:
            with open(f'cache\\FIFA{game}-player-{ID}.png', mode='wb') as file:
                file.write(photo.content)
            image = mpimg.imread(f'cache\\FIFA{game}-player-{ID}.png')
            plt.figure(figsize=(12, 5))
            plt.imshow(image)
            plt.title(
                f'Player: {rows['Name']} \n Game: FIFA{rows['game']} \n Team: {rows['Team']} \n Age: {rows['Age']} \n Position: {rows['Best position']} \n Overall rating: {rows['Overall rating']}')
            plt.axis('off')
            plt.plot()
        else:
            image = mpimg.imread(f'cache\\player-0.png')
            plt.figure(figsize=(12, 5))
            plt.imshow(image)
            plt.title(
                f'Player: {rows['Name']} \n Game: FIFA{rows['game']} \n Team: {rows['Team']} \n Age: {rows['Age']} \n Position: {rows['Best position']} \n Overall rating: {rows['Overall rating']}')
            plt.axis('off')
            plt.plot()
    else:
        image = mpimg.imread(f'cache\\FIFA{game}-player-{ID}.png')
        plt.figure(figsize=(12, 5))
        plt.imshow(image)
        plt.title(
            f'Player: {rows['Name']} \n Game: FIFA{rows['game']} \n Team: {rows['Team']} \n Age: {rows['Age']} \n Position: {rows['Best position']} \n Overall rating: {rows['Overall rating']}')
        plt.axis('off')
        plt.plot()


def draw_player_history(ID: int, players: pd.DataFrame) -> None:
    """
    Функция для отрисовки фото игрока из всех игр, в которых он представлен по данным из `players`
    """
    rows = players[players['ID'] == ID].sort_values(by='game', ascending=True)
    assert rows.shape[0] > 0, print('Укажите верный ID')
    ID = str(ID).rjust(6, '0')
    images = []
    games = rows['game']
    for i in range(len(games)):
        game = rows['game'].iloc[i]
        if not os.path.isfile(f'cache\\FIFA{game}-player-{ID}.png'):
            ref = f"https://cdn.sofifa.net/players/{ID[:3]}/{ID[3:]}/{str(game).rjust(2, '0')}_360.png"
            photo = requests.get(ref, stream=True)
            if photo.status_code == 200:
                with open(f'cache\\FIFA{game}-player-{ID}.png', mode='wb') as file:
                    file.write(photo.content)
                sleep(1)
                image = mpimg.imread(f'cache\\FIFA{game}-player-{ID}.png')
                images.append(image)
            else:
                image = mpimg.imread(f'cache\\player-0.png')
                images.append(image)
        else:
            image = mpimg.imread(f'cache\\FIFA{game}-player-{ID}.png')
            images.append(image)

    num_graphs = len(images)
    fig, axs = plt.subplots(1, num_graphs, figsize=(5 * num_graphs, 4))
    if num_graphs == 1:
        axs = [axs]
    i = 0
    for ax, im in zip(axs, images):
        ax.imshow(im)
        ax.axis('off')
        ax.set_title(f'Player: {rows['Name'].iloc[i]} \n Game: FIFA{rows['game'].iloc[i]} \n Team: {rows['Team'].iloc[i]} \n Age: {rows['Age'].iloc[i]} \n Position: {rows['Best position'].iloc[i]} \n Overall rating: {rows['Overall rating'].iloc[i]}')
        i += 1
    for ax in axs[num_graphs:]:
        ax.remove()
    plt.show()


def draw_player_stat(IDs: int | list, players: pd.DataFrame, stat: str) -> None:
    """
    Функция для отрисовки графика с метрикой `stat` для игрока/игроков в `IDs` по данным из `players`
    """
    if isinstance(IDs, int):
        IDs = [IDs]
    data = {i: [] for i in IDs}
    for ID in IDs:
        rows = players[players['ID'] == ID].sort_values(
            by='game', ascending=True)
        assert rows.shape[0] > 0, print('Укажите верный ID')
        data[ID].append(rows['game'].values)
        data[ID].append(rows[stat].values)
    plt.figure(figsize=(12, 5))
    for key, (x, y) in data.items():
        x = [f'FIFA{i}' for i in x]
        plt.plot(
            x, y, label=f'{players[players['ID'] == key]['Name'].iloc[0]}')
    plt.xlabel('Game')
    plt.ylabel('Rating')
    plt.title(f'Dynamic of "{stat}"')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()


def draw_general_visualization(df: pd.DataFrame) -> None:
    """
    Функция для построения визуализации с гистограммами по различным признакам, доступным в `df`
    """
    visualize_df = df[['Overall rating', 'Potential', 'Total attacking', 'Crossing', 'Finishing',
                       'Heading accuracy', 'Short passing', 'Volleys', 'Total skill',
                       'Dribbling', 'Curve', 'FK Accuracy', 'Long passing', 'Ball control',
                       'Total movement', 'Acceleration', 'Sprint speed', 'Agility',
                       'Reactions', 'Balance', 'Total power', 'Shot power', 'Jumping',
                       'Stamina', 'Strength', 'Long shots', 'Total mentality', 'Aggression',
                       'Tactical Awareness', 'Positioning', 'Vision', 'Penalties', 'Composure',
                       'Total defending', 'Marking', 'Tackling', 'Sliding tackle',
                       'Total goalkeeping', 'GK Diving', 'GK Handling', 'GK Kicking',
                       'GK Positioning', 'GK Reflexes', 'Total stats', 'Base stats', 'Weak foot', 'Skill moves', 'Attacking work rate',
                       'Defensive work rate', 'International reputation', 'Real face',
                       'Pace / Diving', 'Shooting / Handling', 'Passing / Kicking',
                       'Dribbling / Reflexes', 'Defending / Pace', 'Physical / Positioning', 'Standing tackle', 'Interceptions', 'Att. Position',
                       'Defensive awareness', 'game']]
    visualize_df['game'] = pd.to_numeric(df['game'], errors='coerce')
    visualize_df = visualize_df.dropna(subset=['game'])
    visualize_df['game'] = visualize_df['game'].astype(int)

    app = dash.Dash()

    numeric_columns = visualize_df[['Overall rating', 'Potential', 'Total attacking', 'Crossing', 'Finishing',
                                    'Heading accuracy', 'Short passing', 'Volleys', 'Total skill',
                                    'Dribbling', 'Curve', 'FK Accuracy', 'Long passing', 'Ball control',
                                    'Total movement', 'Acceleration', 'Sprint speed', 'Agility',
                                    'Reactions', 'Balance', 'Total power', 'Shot power', 'Jumping',
                                    'Stamina', 'Strength', 'Long shots', 'Total mentality', 'Aggression',
                                    'Tactical Awareness', 'Positioning', 'Vision', 'Penalties', 'Composure',
                                    'Total defending', 'Marking', 'Tackling', 'Sliding tackle',
                                    'Total goalkeeping', 'GK Diving', 'GK Handling', 'GK Kicking',
                                    'GK Positioning', 'GK Reflexes', 'Total stats', 'Base stats', 'Weak foot', 'Skill moves', 'Attacking work rate',
                                    'Defensive work rate', 'International reputation', 'Real face',
                                    'Pace / Diving', 'Shooting / Handling', 'Passing / Kicking',
                                    'Dribbling / Reflexes', 'Defending / Pace', 'Physical / Positioning', 'Standing tackle', 'Interceptions', 'Att. Position',
                                    'Defensive awareness']].columns.tolist()
    default_metric = 'Overall rating' if 'Overall rating' in numeric_columns else numeric_columns[
        0]

    app.layout = html.Div([
        html.H1("Player Stats Histogram", style={'textAlign': 'center'}),

        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': col, 'value': col} for col in numeric_columns],
            value=default_metric,
            clearable=False
        ),

        dcc.Slider(
            id='game-slider',
            min=df['game'].min(),
            max=df['game'].max(),
            step=1,
            value=visualize_df['game'].min(),
            marks={i: str(i) for i in range(visualize_df['game'].min(), visualize_df['game'].max(
            ) + 1, max(1, (visualize_df['game'].max() - visualize_df['game'].min()) // 10))}
        ),

        dcc.Graph(id='histogram-graph')
    ])

    @app.callback(
        Output('histogram-graph', 'figure'),
        [Input('metric-dropdown', 'value'),
         Input('game-slider', 'value')]
    )
    def update_plot(metric, game):
        filtered_df = visualize_df[visualize_df['game'] == game]
        fig = px.histogram(filtered_df, x=metric, title=f'{metric} Distribution for Game {game}', color_discrete_sequence=[
                           'purple'], histnorm="probability density",)
        fig.update_layout(bargap=0.1)
        return fig

    app.run_server()
