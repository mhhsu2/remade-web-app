import pandas as pd
from flask import Flask, redirect, render_template, request, session, url_for, flash, Response
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

from db import Database
from forms import IrAndAeForm, LuForm, NluForm, UploadForm
from plotly_figure import plotly_ir, plotly_ae, plotly_lu, plotly_nlu, plotly_xrd

from utils import naming_file

import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key values'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = Database()
    data = db.list_exp_info()

    return render_template('exp_info.html', data=data)

@app.route('/search/<nde>', methods=['GET', 'POST'])
@login_required
def search(nde):
    db = Database()
    data = db.list_exp_info()
    
    if nde == 'ir':
        # Query Forms
        form = IrAndAeForm()

        # Form choices from data
        LOADING_AMP_CHOICES = [11.7, 12.7, 14.7]
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in LOADING_AMP_CHOICES]

        if form.is_submitted():
            session['nde'] = nde

            if form.loading_amp.data != []:
                session['loading_amp'] = form.loading_amp.data
            else: 
                session['loading_amp'] = [str(v) for v in LOADING_AMP_CHOICES] 
            
            if form.exp_id.data != '':
                session['exp_id'] = form.exp_id.data
            else:
                session['exp_id'] = str(list(df['exp_id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'ae':
        # Query Forms
        form = IrAndAeForm()

        # Form choices from data
        LOADING_AMP_CHOICES = [11.7, 12.7, 14.7]
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in LOADING_AMP_CHOICES]

        if form.is_submitted():
            session['nde'] = nde

            if form.loading_amp.data != []:
                session['loading_amp'] = form.loading_amp.data
            else: 
                session['loading_amp'] = [str(v) for v in LOADING_AMP_CHOICES] 
            
            if form.exp_id.data != '':
                session['exp_id'] = form.exp_id.data
            else:
                session['exp_id'] = str(list(df['exp_id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'lu':
        # Query Forms
        form = LuForm()

        # Form choices from data
        LOADING_AMP_CHOICES = [0.0, 11.7, 12.7, 14.7]
        POSITION_CHOICES = [-90, -60, -40, -20, 0, 20, 40, 60, 90]
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in LOADING_AMP_CHOICES]
        form.dist_from_center.choices = [(v, v) for v in POSITION_CHOICES]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            if form.loading_amp.data != []:
                session['loading_amp'] = form.loading_amp.data
            else: 
                session['loading_amp'] = [str(v) for v in LOADING_AMP_CHOICES] 

            if form.dist_from_center.data != []:
                session['dist_from_center'] = form.dist_from_center.data
            else:
                session['dist_from_center'] = [str(v) for v in POSITION_CHOICES] 
            
            if form.exp_id.data != '':
                session['exp_id'] = form.exp_id.data
            else:
                session['exp_id'] = str(list(df['exp_id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'nlu':
        # Query Forms
        form = NluForm()

        # Form choices from data       
        LOADING_AMP_CHOICES = [0.0, 11.7, 12.7, 14.7]
        POSITION_CHOICES = [-90, -60, -40, -20, 0, 20, 40, 60, 90]
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in LOADING_AMP_CHOICES]
        form.dist_from_center.choices = [(v, v) for v in POSITION_CHOICES]
        form.nlu_amp.choices = [(v, v) for v in range(1,12)]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            if form.loading_amp.data != []:
                session['loading_amp'] = form.loading_amp.data
            else: 
                session['loading_amp'] = [str(v) for v in LOADING_AMP_CHOICES] 

            if form.dist_from_center.data != []:
                session['dist_from_center'] = form.dist_from_center.data
            else:
                session['dist_from_center'] = [str(v) for v in POSITION_CHOICES] 

            if form.nlu_amp.data != []:
                session['nlu_amp'] = form.nlu_amp.data
            else:
                session['nlu_amp'] = [str(v) for v in range(1,12)]

            if form.exp_id.data != '':
                session['exp_id'] = form.exp_id.data
            else:
                session['exp_id'] = str(list(df['exp_id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    elif nde == 'xrd':
        # Query Forms
        form = LuForm()

        # Form choices from data
        LOADING_AMP_CHOICES = [0.0, 11.7, 12.7, 14.7]
        POSITION_CHOICES = [0, 20, 40]
        df = pd.DataFrame(data)
        form.loading_amp.choices = [(v, v) for v in LOADING_AMP_CHOICES]
        form.dist_from_center.choices = [(v, v) for v in POSITION_CHOICES]

        if form.is_submitted():
            session['nde'] = nde
            session['loading_amp'] = form.loading_amp.data

            if form.loading_amp.data != []:
                session['loading_amp'] = form.loading_amp.data
            else: 
                session['loading_amp'] = [str(v) for v in LOADING_AMP_CHOICES] 

            if form.dist_from_center.data != []:
                session['dist_from_center'] = form.dist_from_center.data
            else:
                session['dist_from_center'] = [str(v) for v in POSITION_CHOICES] 
            
            if form.exp_id.data != '':
                session['exp_id'] = form.exp_id.data
            else:
                session['exp_id'] = str(list(df['exp_id'].dropna().unique().astype(int))).strip('[]')

            session['min_percent_fatigue_life'] = form.min_percent_fatigue_life.data
            session['max_percent_fatigue_life'] = form.max_percent_fatigue_life.data
            return redirect(url_for('result', nde=nde))

    return render_template('search.html', data=data, form=form, nde=nde)

@app.route('/result/<nde>', methods=['GET', 'POST'])
@login_required
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
        graphJSON = plotly_ir(data)

        return render_template('result.html', data=data, nde=nde, graphJSON=graphJSON)
    
    elif nde == 'ae':
        data = db.list_ae(loading_amp=loading_amp, exp_id=exp_id, 
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)

        graphJSON = plotly_ae(data)

        return render_template('result.html', data=data, nde=nde, graphJSON=graphJSON)
    
    elif nde == 'lu':
        dist_from_center = session.get('dist_from_center', None)

        data = db.list_lu(loading_amp=loading_amp, exp_id=exp_id, dist_from_center=dist_from_center,
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)

        # Plot figure with Plotly
        graphJSON = plotly_lu(data)

        return render_template('result.html', data=data, nde=nde, graphJSON=graphJSON)
    
    elif nde == 'nlu':
        dist_from_center = session.get('dist_from_center', None)
        nlu_amp = session.get('nlu_amp', None)
        
        data = db.list_nlu(loading_amp=loading_amp, exp_id=exp_id, 
                            dist_from_center=dist_from_center, nlu_amp=nlu_amp,
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)
                            
        # Plot figure with Plotly
        graphJSON = plotly_nlu(data)

        return render_template('result.html', data=data, nde=nde, graphJSON=graphJSON)

    elif nde == 'xrd':
        dist_from_center = session.get('dist_from_center', None)

        data = db.list_xrd(loading_amp=loading_amp, exp_id=exp_id, dist_from_center=dist_from_center,
                            min_percent_fatigue_life=min_percent_fatigue_life, 
                            max_percent_fatigue_life=max_percent_fatigue_life)

        # Plot figure with Plotly
        graphJSON, graphJSON2 = plotly_xrd(data)

        return render_template('result.html', data=data, nde=nde, graphJSON=graphJSON, graphJSON2=graphJSON2)

@app.route('/files', methods=['GET', 'POST'])
@login_required
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket('remade-nde')
    summaries = my_bucket.objects.all()

    form = UploadForm()

    if form.is_submitted():
        info = {'nde': form.nde.data, 'exp_id': form.exp_id.data,
                'loading_amp': form.loading_amp.data, 'percent_fatigue_life': form.percent_fatigue_life.data,
                'nlu_amp': form.nlu_amp.data, 'dist_from_center': form.dist_from_center.data}

        filename = naming_file(info)

        file = request.files['file']
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket('remade-nde')
        my_bucket.Object(filename).put(Body=file)
        data = my_bucket.Object(filename).get()['Body']

        flash('File uploaded successfully')
        return redirect(url_for('files'))

    return render_template('files.html', my_bucket=my_bucket, files=summaries, form=form)


@app.route('/download', methods=['POST'])
@login_required
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

# User login
# TODO: Move to individual file
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    db = Database()
    if user_id != db.get_user_id(user_id):
        return

    user = User()
    user.id = user_id
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    password = request.form['password']

    db = Database()
    if (user_id == db.get_user_id(user_id)) and (password == db.get_user_password(user_id)):
        user = User()
        user.id = user_id
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template("login.html")


# Miscellaneous 
@app.errorhandler(500)
def internal_error(error):
    return render_template('error_pages/500.html'), 500

@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-store"
	return response

if __name__ == '__main__':
    app.run(debug=True)
