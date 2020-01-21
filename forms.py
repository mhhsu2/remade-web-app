from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, widgets

# Create MultiCheckboxField
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class IrAndAeForm(FlaskForm):
    loading_amp = SelectMultipleField('Loading Amplidtude')
    exp_id = StringField('Exp. ID (optional)')
    min_percent_fatigue_life = StringField('Mininum Fatigue Life (%)', default='0')
    max_percent_fatigue_life = StringField('Maximum Fatigue Life (%)', default='100')
    submit = SubmitField('Submit')

class LuForm(FlaskForm):
    loading_amp = SelectMultipleField('Loading Amplidtude')
    exp_id = StringField('Exp. ID (optional)')
    position = SelectMultipleField('Measuremnet Position')
    min_percent_fatigue_life = StringField('Mininum Fatigue Life (%)', default='0')
    max_percent_fatigue_life = StringField('Maximum Fatigue Life (%)', default='100')
    submit = SubmitField('Submit')

class NluForm(FlaskForm):
    loading_amp = SelectMultipleField('Loading Amplidtude')
    exp_id = StringField('Exp. ID (optional)')
    nlu_amp = SelectMultipleField('Measurement Amplitude')
    position = SelectMultipleField('Measuremnet Position')
    min_percent_fatigue_life = StringField('Mininum Fatigue Life (%)', default='0')
    max_percent_fatigue_life = StringField('Maximum Fatigue Life (%)', default='100')
    submit = SubmitField('Submit')

    
    
    
