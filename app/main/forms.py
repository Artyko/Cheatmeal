from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.date)
            if user is not None:
                raise ValidationError('Please use a different username')


class RecipeForm(FlaskForm):
    title = StringField(_l('Recipe name'), validators=[DataRequired()])
    ingredients = TextAreaField(_l('Ingredient name'))
    description = TextAreaField(_l('Describe your recipe'))
    submit = SubmitField(_l('Submit'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
