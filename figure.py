#%%
import os

from flask import url_for, current_app

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from decimal import Decimal

# Solve matplotlib error when using flask app
plt.switch_backend('Agg')

# Create more seaborn markers and styles
dash_styles = ["",
               (4, 1.5),
               (1, 1),
               (3, 1, 1.5, 1),
               (5, 1, 1, 1),
               (5, 1, 2, 1, 2, 1),
               (2, 2, 3, 1.5),
               (1, 2.5, 3, 1.2),
               (3, 2, 4, 1.0),
               (1, 2, 3.5, 1.1),
               (4, 1, 1, 1),
               (4, 2, 1, 1),
               (4, 2, 2, 1),
               (4, 3, 3, 1.1),
               (5, 1, 4, 2, 3, 1),
               (5, 2, 3, 2, 2, 1.1)]
markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')

# Infrared Camera
def plot_ir(data):
    

    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Search parameter
    loading_amp = list(df['loading_amp'].unique().astype(str))
    exp_id = list(df['exp_id'].unique().astype(str))
    min_percent_fatigue_life = df['percent_fatigue_life'].min()
    max_percent_fatigue_life = df['percent_fatigue_life'].max()


    plt.figure(figsize=(15,6))
    palette = sns.color_palette("bright", len(df['loading_amp'].unique()))
  
    g = sns.lineplot(x='cycles', y='temperature', hue='loading_amp', style='exp_id',
                    markers=markers, dashes=dash_styles, markeredgecolor=None, markersize=3,
                    palette=palette, data=df)

    # g.set_xlim([0,100])

    g.set_title("""Infrared Camera\nLoading Amplitude: {}\nExp. ID: {}\nRange of Fatigue Life: {}~{}
                """.format(
                    ', '.join(i for i in loading_amp),
                    ', '.join(i for i in exp_id),
                    min_percent_fatigue_life,
                    max_percent_fatigue_life,
                    fontsize=24, fontweight='bold'))

    g.set_xlabel('Cycle', fontsize=14)
    g.set_ylabel('Temperature (ºC)', fontsize=14)

    g.legend().set_bbox_to_anchor([1.12,1])
    g.grid()

    plt.tight_layout()

    # # Save file
    nde = 'ir'
    filename = 'temp.png'
    # filename = '{}_{}_{}.png'.format(nde,
    #                     '-'.join(i for i in loading_amp),
    #                     '-'.join(i for i in exp_id),
                            # min_percent_fatigue_life,
                            # max_percent_faitgue_life)

    filepath = os.path.join(current_app.root_path, 'static/fig/result', nde, filename)

    # Save result to temp.png


    plt.savefig(filepath, dpi=200)
    plt.close()

    return os.path.join('fig/result', nde, filename)

# %%
# Acoustic Emission
def plot_ae(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Search parameter
    loading_amp = list(df['loading_amp'].unique().astype(str))
    exp_id = list(df['exp_id'].unique().astype(str))
    min_percent_fatigue_life = df['percent_fatigue_life'].min()
    max_percent_fatigue_life = df['percent_fatigue_life'].max()


    plt.figure(figsize=(15,6))
    palette = sns.color_palette("bright", len(df['loading_amp'].unique()))
  
    g = sns.lineplot(x='cycles', y='ae_hits', hue='loading_amp', style='exp_id',
                    markers=True, dashes=False, markeredgecolor=None, markersize=3,
                    palette=palette, data=df)

    # g.set_xlim([0,100])

    g.set_title("""Infrared Camera\nLoading Amplitude: {}\nExp. ID: {}\nRange of Fatigue Life: {}~{}
                """.format(
                    ', '.join(i for i in loading_amp),
                    ', '.join(i for i in exp_id),
                    min_percent_fatigue_life,
                    max_percent_fatigue_life,
                    fontsize=24, fontweight='bold'))

    g.set_xlabel('Cycle', fontsize=14)
    g.set_ylabel('Average AE Hits (per 100 sec)', fontsize=14)

    g.legend().set_bbox_to_anchor([1.12,1])
    g.grid()

    plt.tight_layout()

    # # Save file
    nde = 'ae'
    filename = 'temp.png'
    filepath = os.path.join(current_app.root_path, 'static/fig/result', nde, filename)

    # Save result to temp.png


    plt.savefig(filepath, dpi=200)
    

    return os.path.join('fig/result', nde, filename)

# %%
# Linear Ultrasound
def plot_lu(data):
    
    df = pd.DataFrame(data)

    # Change columns type for plotting
    df = df.apply(pd.to_numeric, errors='ignore')

    # TODO: Not working. data type not understood
    # numerical_cols = ['wave_speed', 'percent_fatigue_life']
    # for col in df.columns:
    #     if col not in numerical_cols:
    #         df[col] = df[col].astype('category')

    # Plot
    _, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(data=df, x='dist_from_center', y='wave_speed',
                 hue='loading_amp', style='percent_fatigue_life',
                 markers=True, ax=ax)

    ax.legend(bbox_to_anchor=(1.2,1))
    ax.set_ylabel('Wave Speed (m/s)')
    ax.set_xlabel('Distance from Center (mm)')
    plt.tight_layout()

    # Save result to temp.png
    nde = 'lu'
    filename = 'temp.png'
    filepath = os.path.join(current_app.root_path, 'static/fig/result', nde, filename)
    plt.savefig(filepath, dpi=200,  bbox_inches="tight")
    

    return os.path.join('fig/result', nde, filename)


# %%
# Nonlinear Ultrasound
def plot_nlu(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Plot
    _, ax = plt.subplots(figsize=(16, 10))
    sns.lineplot(data=df, x='dist_from_center', y='acoustic_parameter',
                 hue='loading_amp', style='percent_fatigue_life',
                 markers=True, ax=ax)

    ax.legend(bbox_to_anchor=(1.2,1))
    ax.set_ylabel('Wave Speed (m/s)')
    ax.set_xlabel('Distance from Center (mm)')
    plt.tight_layout()

    # Save result to temp.png
    nde = 'nlu'
    filename = 'temp.png'
    filepath = os.path.join(current_app.root_path, 'static/fig/result', nde, filename)
    plt.savefig(filepath, dpi=200,  bbox_inches="tight")

    return os.path.join('fig/result', nde, filename)