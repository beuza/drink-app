"""
WTF forms
"""
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired

class VoteForm(FlaskForm):
    # choices = VoteForm.getChoices()
    # vote = RadioField('Label', choices=choices)
    vote = RadioField(choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Submit')

"""
    def __init__(self, userID, userName, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.userID = userID
        self.userName = userName

    def getChoices(self):
        choices = []
        for i in range(len(self.userID)):
            choices.append((str(self.userID[i]), str(self.userName[i])))
        return choices
"""