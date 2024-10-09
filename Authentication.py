from database import DataOperations
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin

DO = DataOperations()

class LoginForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(min = 6, max = 20)], 
                           render_kw= {"placeholder" : "UserName"})
    
    password = PasswordField(validators= [InputRequired(), Length(min= 8, max= 20)],
                             render_kw= {"placeholder" : "Password"})
    
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(min = 6, max = 20)], 
                           render_kw= {"placeholder" : "UserName"})
    
    password = PasswordField(validators= [InputRequired(), Length(min= 8, max= 20)],
                             render_kw= {"placeholder" : "Password"})
    
    passkey = PasswordField(validators= [InputRequired(), Length(min= 6, max= 8)],
                             render_kw= {"placeholder" : "Passkey"})
    
    submit = SubmitField("Register")
    '''
    def validate_username(self, username):
        existing_user_username = DO.check_username(username)
        if existing_user_username:
            raise ValidationError("The username already exists. Please choose a different one.")
    '''

class User(UserMixin):
    def __init__(self, id, username, password) -> None:
        self.id = id
        self.username = username 
        self.password = password
    
    @staticmethod
    def get_by_id(DO, user_id):
        with DO.engine.connect() as conn:
            sql = "SELECT ID, User_name, Passkey FROM Users WHERE id = :ID"
            result = conn.execute(text(sql), {'ID': str(user_id)})
            result = result.all()[0]

            if result:
                # Assuming result is (id, username, password)
                return User(id=result[0], username=result[1], password=result[2])
            else:
                return None
