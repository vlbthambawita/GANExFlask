from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateProject_form(FlaskForm):
    projectName = StringField("New Project Name", validators=[DataRequired()])
    projectPath = StringField("Project Path" , validators=[DataRequired()])
    submit = SubmitField("Create Project") 

class CreateExperiment_form(FlaskForm):
    expName = StringField("New Experiment Name", validators=[DataRequired()])
    submit = SubmitField("Create Experiment") 
