import pandas as pd
from flask import Flask, redirect, render_template, request, session, url_for, flash, Response

from db import Database
from forms import IrAndAeForm, LuForm, NluForm
from figure import plot_ir, plot_ae, plot_lu, plot_nlu

import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key values'


@app.route('/', methods=['GET', 'POST'])
def index():
    db = Database()
    data = db.list_exp_info()

    return render_template('exp_info.html', data=data)

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_pages/500.html'), 500

@app.route('/search/<nde>', methods=['GET', 'POST'])
def search(nde):
    db = Database()
    data = db.list_exp_info()
    
    if nde == 'ir':
        # Query Forms
        form = IrAndAeForm()

        # Form choices from data
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in list(df['loading_amp'].unique())]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            session['exp_id'] = form.exp_id.data
            if session['exp_id'] == '':
                session['exp_id'] = str(list(df['id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'ae':
        # Query Forms
        form = IrAndAeForm()

        # Form choices from data
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in list(df['loading_amp'].unique())]


        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            session['exp_id'] = form.exp_id.data
            if session['exp_id'] == '':
                session['exp_id'] = str(list(df['id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'lu':
        # Query Forms
        form = LuForm()

        # Form choices from data
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in list(df['loading_amp'].unique())]
        form.position.choices = [(v, v) for v in range(1,6)]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            session['exp_id'] = form.exp_id.data
            if session['exp_id'] == '':
                session['exp_id'] = str(list(df['id'].dropna().unique().astype(int))).strip('[]')
            
            session['position'] = form.position.data
            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'nlu':
        # Query Forms
        form = NluForm()

        # Form choices from data
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in list(df['loading_amp'].unique())]
        form.position.choices = [(v, v) for v in range(1,6)]
        form.nlu_amp.choices = [(v, v) for v in range(1,12)]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            session['exp_id'] = form.exp_id.data
            if session['exp_id'] == '':
                session['exp_id'] = str(list(df['id'].dropna().unique().astype(int))).strip('[]')
            
            session['position'] = form.position.data
            session['nlu_amp'] = form.nlu_amp.data
            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    return render_template('search.html', data=data, form=form, nde=nde)

@app.route('/result/<nde>', methods=['GET', 'POST'])
def result(nde):
    loading_amp = session.get('loading_amp', None)
    exp_id = session.get('exp_id', None)
    min_percent_fatigue_life = session.get('min_percent_fatigue_life', None)
    max_percent_fatigue_life = session.get('max_percent_fatigue_life', None)
    
    db = Database()

    # Get data from submitted form
    if nde == 'ir':
        data = db.list_ir(loading_amp=loading_amp, exp_id=exp_id, 
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)
        
        # Plot figure
        fig_url = plot_ir(data)

        return render_template('result.html', data=data, nde=nde, fig_url=fig_url)
    
    elif nde == 'ae':
        data = db.list_ae(loading_amp=loading_amp, exp_id=exp_id, 
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)

        fig_url = plot_ae(data)

        return render_template('result.html', data=data, nde=nde, fig_url=fig_url)
    
    elif nde == 'lu':
        position = session.get('position', None)

        data = db.list_lu(loading_amp=loading_amp, exp_id=exp_id, position=position,
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)

        fig_url = plot_lu(data)

        return render_template('result.html', data=data, nde=nde, fig_url=fig_url)
    
    elif nde == 'nlu':
        position = session.get('position', None)
        nlu_amp = session.get('nlu_amp', None)
        
        data = db.list_nlu(loading_amp=loading_amp, exp_id=exp_id, 
                            position=position, nlu_amp=nlu_amp,
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)
        fig_url = plot_nlu(data)
        return render_template('result.html', data=data, nde=nde, fig_url=fig_url)

@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-store"
	return response

@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket('remade-nde')
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket('remade-nde')
    my_bucket.Object('test').put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket('remade-nde')

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == '__main__':
    app.run(debug=True)
