from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import json

class CreateProject_form(FlaskForm):
    projectName = StringField("New Project Name", validators=[DataRequired()])
    projectPath = StringField("Project Path" , validators=[DataRequired()])
    submit = SubmitField("Create Project") 

class CreateExperiment_form(FlaskForm):

    #def __init__(self, *args, **kwargs):
        #super(CreateExperiment_form, self).__init__(*args, **kwargs)
       # self.ganTypesDict = ganTypesDict
        # self.ganTypesArray = [("a", 1), ("b", 2)]

    expName = StringField("New Experiment Name", validators=[DataRequired()])
    ganType = SelectField("Select the GAN type", choices = []) # update dynamically later
    submit = SubmitField("Create Experiment") 

    #def updateGanTypesChoinces(choicesArray):
    #    self.ganType.




