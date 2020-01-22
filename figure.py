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
  
    g = sns.lineplot(x='percent_fatigue_life', y='temperature', hue='loading_amp', style='exp_id',
                    markers=True, dashes=False, markeredgecolor=None, markersize=3,
                    palette=palette, data=df)

    g.set_xlim([0,100])

    g.set_title("""Infrared Camera\nLoading Amplitude: {}\nExp. ID: {}\nRange of Fatigue Life: {}~{}
                """.format(
                    ', '.join(i for i in loading_amp),
                    ', '.join(i for i in exp_id),
                    min_percent_fatigue_life,
                    max_percent_fatigue_life,
                    fontsize=24, fontweight='bold'))

    g.set_xlabel('Fatigue Life (%)', fontsize=14)
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
  
    g = sns.lineplot(x='percent_fatigue_life', y='avg_ae_hits', hue='loading_amp', style='exp_id',
                    markers=True, dashes=False, markeredgecolor=None, markersize=3,
                    palette=palette, data=df)

    g.set_xlim([0,100])

    g.set_title("""Infrared Camera\nLoading Amplitude: {}\nExp. ID: {}\nRange of Fatigue Life: {}~{}
                """.format(
                    ', '.join(i for i in loading_amp),
                    ', '.join(i for i in exp_id),
                    min_percent_fatigue_life,
                    max_percent_fatigue_life,
                    fontsize=24, fontweight='bold'))

    g.set_xlabel('Fatigue Life (%)', fontsize=14)
    g.set_ylabel('Average AE Hits (per 100 sec)', fontsize=14)

    g.legend().set_bbox_to_anchor([1.12,1])
    g.grid()

    plt.tight_layout()

    # # Save file
    nde = 'ae'
    filename = 'temp.png'
    filepath = os.path.join( 'static/fig/result', nde, filename)

    # Save result to temp.png


    plt.savefig(filepath, dpi=200)
    

    return os.path.join('fig/result', nde, filename)

# %%
# Acoustic Emission
def plot_lu(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    plt.figure(figsize=(15,6))
    g = sns.FacetGrid(data=df, hue='loading_amp', height=3)
    g.map(sns.regplot, 'percent_fatigue_life', 'avg_wave_speed',  ci=None)

    # Annotate
    for ax in g.axes.ravel():
        gax = ax

    g.add_legend(bbox_to_anchor=(1.2,0.5))
    g.set_ylabels('Wave Speed (m/s)')
    g.set_xlabels('Fatigue Life (%)')
    plt.tight_layout()

    # Save result to temp.png
    nde = 'lu'
    filename = 'temp.png'
    filepath = os.path.join( 'static/fig/result', nde, filename)
    plt.savefig(filepath, dpi=200,  bbox_inches="tight")
    

    return os.path.join('fig/result', nde, filename)


# %%
df = pd.DataFrame(data)
df = df.apply(pd.to_numeric, errors='ignore')

plt.figure(figsize=(15,6))
g = sns.FacetGrid(data=df, hue='loading_amp', height=3)
g.map(sns.regplot, 'percent_fatigue_life', 'avg_wave_speed',  ci=None)

# Annotate
for ax in g.axes.ravel():
    gax = ax

g.add_legend(bbox_to_anchor=(1.2,0.5))
g.set_ylabels('Wave Speed (m/s)')
g.set_xlabels('Fatigue Life (%)')
plt.tight_layout()

# Save result to temp.png
nde = 'lu'
filename = 'temp.png'
filepath = os.path.join( 'static/fig/result', nde, filename)
plt.savefig(filepath, dpi=200,  bbox_inches="tight")


# %%
plot_lu(data)

# %%
