from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, DateTimeField, StringField, PasswordField, SubmitField, HiddenField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, InputRequired, Optional
from yogana.models import User, Item, Feedback, Adminsupdate
from flask_login import current_user

#blog section
class BlogForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    date = StringField('Date (e.g., June 19, 2024)', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    excerpt = TextAreaField('Excerpt', validators=[Optional()])
    slug = StringField('Slug (unique)', validators=[DataRequired()])
    published_on = StringField('Published On (e.g., September 3, 2024)', validators=[Optional()])
    published_by = StringField('Published By', validators=[Optional()])
    content = TextAreaField('Content (separate paragraphs by line breaks)', validators=[DataRequired()])
    features = TextAreaField('Features (separate by commas)', validators=[Optional()])
    gallery_images = StringField('Gallery Image URL', validators=[Optional()])
    tags = StringField('Tags (separate by commas)', validators=[Optional()])
    submit = SubmitField('Submit')


#AdminType option for Admins form
class AdminTypeOptionForm(FlaskForm):
    name = StringField(label='AdminType Options', validators=[DataRequired()])
    submit_add = SubmitField(label='Add Option')
    #submit_remove = SubmitField(label='Remove Option')



#OG-Registerform
class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        
    company_name = StringField(label='Company Name:', validators=[Length(min=2, max=30), DataRequired()])
    name = StringField(label='Name:', validators=[Length(min=2, max=30)])
    cnumb = StringField(label='Number:', validators=[Length(min=10, max=12)])
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    
    submit = SubmitField(label='Create Account')

class ProfileForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30)])
    cnumb = StringField(label='Number:', validators=[Length(min=10, max=12)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    company_name = StringField(label='Company Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Profile')

    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Incorrect current password')

#Password Changing Form
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Change Password')

# Form for Item Registration
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    source = SelectField('Source', choices=[], validators=[DataRequired()])
    #source = SelectField('Source', choices=[('source1', 'Source 1'), ('source2', 'Source 2')])

#OG-Login-form
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

#OG-purchase-Admins
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

#OG-purchase-Admins
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')

#Feedback-Form
class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(min=2)])
    Admin_id = StringField('Admin ID', validators=[DataRequired()])
    user_id = StringField('User ID', validators=[DataRequired()])



class AdminsupdateForm(FlaskForm):
    Admin_id = StringField(label='Admin ID', validators=[DataRequired()])
    user_id = StringField(label='User ID', validators=[DataRequired()])
    campaign = SelectField(label='Campaign',choices=[], validators=[InputRequired()])
    Admintype = SelectField(label='Admin Type',choices=[], validators=[InputRequired()])
    Adminstatus = SelectField(label='Admin Status',choices=[], validators=[InputRequired()])
    Admincategory = SelectField(label='Admin Category',choices=[], validators=[InputRequired()])
    Adminlocation = StringField(label='Admin Location', validators=[InputRequired()])
    date = StringField(label='Date', validators=[InputRequired()])


