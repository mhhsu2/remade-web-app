import pandas as pd
import plotly
import plotly.express as px
import json

def plotly_ir(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Change columns type for plotting
    numerical_cols = ['temperature', 'cycles', 'percent_fatigue_life']
    for col in df.columns:
        if col not in numerical_cols:
            print(col)
            df[col] = df[col].astype('category')


    # Plotly plot
    fig = px.scatter(data_frame=df, 
                 x='cycles', y='temperature', 
                 color='loading_amp', symbol='exp_id')
    
    fig.update_traces(marker=dict(size=1,
                                line=dict(width=1)),
                    mode='lines+markers')
    fig.update_layout(title_text = 'Temperature')
    fig.update_xaxes(title_text='Cycle')
    fig.update_yaxes(title_text='Temperature (C)')

    # Convert the figures to JSON
    graphJSON = fig.to_json()

    return graphJSON

def plotly_ae(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Change columns type for plotting
    numerical_cols = ['ae_hits', 'cycles', 'percent_fatigue_life']
    for col in df.columns:
        if col not in numerical_cols:
            print(col)
            df[col] = df[col].astype('category')


    # Plotly plot
    fig = px.scatter(data_frame=df, 
                 x='cycles', y='ae_hits', 
                 color='loading_amp', symbol='exp_id')
    
    fig.update_traces(marker=dict(size=1,
                                line=dict(width=1)),
                    mode='lines+markers')
    fig.update_layout(title_text = 'Average AE Hits (per 100 sec)')
    fig.update_xaxes(title_text='Cycle')
    fig.update_yaxes(title_text='Average AE Hits (per 100 sec)')

    # Convert the figures to JSON
    graphJSON = fig.to_json()

    return graphJSON

def plotly_lu(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Change columns type for plotting
    numerical_cols = ['wave_speed', 'percent_fatigue_life']
    for col in df.columns:
        if col not in numerical_cols:
            df[col] = df[col].astype('category')

    mean_df = (df.groupby(['loading_amp', 'percent_fatigue_life', 'dist_from_center'])
               .mean()
               .reset_index()
               .dropna())

    # Plotly plot
    fig = px.scatter(data_frame=mean_df, 
                 x='dist_from_center', y='wave_speed', 
                 color='loading_amp', symbol='percent_fatigue_life')
    fig.update_traces(mode='markers+lines')
    fig.update_layout(title_text='Wave Speed')
    fig.update_xaxes(title_text='Dist from Center (mm)')
    fig.update_yaxes(title_text='Wave Speed (m/s)')

    # Convert the figures to JSON
    graphJSON = fig.to_json()

    return graphJSON

def plotly_nlu(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Change columns type for plotting
    numerical_cols = ['acoustic_parameter', 'percent_fatigue_life']
    for col in df.columns:
        if col not in numerical_cols:
            df[col] = df[col].astype('category')

    mean_df = (df.groupby(['loading_amp', 'percent_fatigue_life', 'dist_from_center'])
               .mean()
               .reset_index()
               .dropna())

    # Plotly plot
    fig = px.scatter(data_frame=mean_df, 
                 x='dist_from_center', y='acoustic_parameter', 
                 color='loading_amp', symbol='percent_fatigue_life')

    fig.update_traces(mode='markers+lines')
    fig.update_layout(title_text='Acoustic Nonlinearity Parameter')
    fig.update_xaxes(title_text='Dist from Center (mm)')
    fig.update_yaxes(title_text='Acoustic Nonlinearity Parameter')

    # Convert the figures to JSON
    graphJSON = fig.to_json()

    return graphJSON

def plotly_xrd(data):
    
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Change columns type for plotting
    numerical_cols = ['residual_stress', 'fwhm', 'percent_fatigue_life']
    for col in df.columns:
        if col not in numerical_cols:
            df[col] = df[col].astype('category')

    mean_df = (df.groupby(['loading_amp', 'percent_fatigue_life', 'dist_from_center'])
               .mean()
               .reset_index()
               .dropna())

    # Plotly plot
    fig = px.scatter(data_frame=mean_df, 
                 x='dist_from_center', y='residual_stress', 
                 color='loading_amp', symbol='percent_fatigue_life')

    fig.update_traces(mode='markers+lines')
    fig.update_layout(title_text='Residual Stress')
    fig.update_xaxes(title_text='Dist from Center (mm)')
    fig.update_yaxes(title_text='Residual Stress (MPa)')

    # Convert the figures to JSON
    graphJSON = fig.to_json()

    # Plotly plot (for FWHM)
    fig = px.scatter(data_frame=mean_df, 
                 x='dist_from_center', y='fwhm', 
                 color='loading_amp', symbol='percent_fatigue_life')

    fig.update_traces(mode='markers+lines')
    fig.update_layout(title_text='Full Width at Half Maximum')
    fig.update_xaxes(title_text='Dist from Center (mm)')
    fig.update_yaxes(title_text='Full Width at Half Maximum')

    # Convert the figures to JSON
    graphJSON2 = fig.to_json()

    return graphJSON, graphJSON2