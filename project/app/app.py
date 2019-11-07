from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, SelectField, validators, StringField, SubmitField
from wtforms.widgets import TextArea
import os

from summarize import summarize
from model_selector import get_best_model

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

def get_models():
    path = '../model/saved_model/'
    models = [x for x in os.walk(path)][0][1]
    models.sort()
    models = ['Choose Automaticaly'] + models
    # removes the Gigaword from list. The Gigaword model will be used if any of the models Science, Politics, Sports is selected
    models.remove('Gigaword')
    return [(x,x) for x in models]

class ReusableForm(Form):
    input_to_summarize = TextAreaField('Name:', validators=[validators.required()], widget=TextArea())
    result_to_render = TextAreaField(widget=TextArea())
    pretrained_model   = SelectField(u'Pretrained Model', choices=get_models())

@app.route("/form", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    result = ''
    model = ''
    valid = 0
    similarity = 0
    if request.method == 'POST' and form.validate():
        valid = 1

        if form.pretrained_model.data == 'Choose Automaticaly':
            model,similarity = get_best_model(form.input_to_summarize.data)
            print('\nSELECTED MODEL: '+model+'\n')
            result = summarize(form.input_to_summarize.data, model)
            model_message = model + " - %.2f %% of similarity with input text" % (similarity*100)

        else:
            model = form.pretrained_model.data
            result = summarize(form.input_to_summarize.data, model)
            model_message = model

        form.result_to_render = result

        return render_template('form.html', form=form, result=form.result_to_render, model_message=model_message, similarity=similarity)
    else:
        flash('Please include some text to be summarized.')
        
    return render_template('form.html', form=form, result=result, model=model)   
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)