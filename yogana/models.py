from yogana import db, login_manager
from yogana import bcrypt
from flask_login import UserMixin

from datetime import datetime


class BMICalculatorData(db.Model):
    __tablename__ = 'bmi_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bmi_category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DuedateData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    last_period_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.String(100), nullable=False, default="Not calculated")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PeriodData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    last_period_date = db.Column(db.Date, nullable=False)
    cycle_length = db.Column(db.Integer, nullable=False)
    next_period_date = db.Column(db.Date, nullable=False)
    fertile_days = db.Column(db.String(100), nullable=False, default="Not calculated")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class OvulationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    last_period_date = db.Column(db.Date, nullable=False)
    ovulation_date = db.Column(db.Date, nullable=False)
    fertile_days = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class HospitalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_hours = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    facebook_url = db.Column(db.String, nullable=True)
    twitter_url = db.Column(db.String, nullable=True)
    linkedin_url = db.Column(db.String, nullable=True)
    instagram_url = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<HospitalInfo {self.email}>"

# About Section Model
class WhySection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)
    button_text = db.Column(db.String, nullable=False)
    button_link = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# About Section Model
class AboutSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    features = db.Column(db.Text, nullable=False)
    button_text = db.Column(db.String, nullable=False)
    button_link = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Mission Section Model
class MissionSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    shape_image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Mission Features Model
class MissionFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feedback Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Fun Fact Model
class FunFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    optional_icon = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Vision Data Model
class VisionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon_class = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Services Area Model
class ServicesArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define the FAQ model
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CarouselItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255))
    bg_class = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    btn_primary_text = db.Column(db.String(255), nullable=False)
    btn_primary_icon = db.Column(db.String(255), nullable=False)
    btn_primary_link = db.Column(db.String(255), nullable=False)
    btn_secondary_text = db.Column(db.String(255), nullable=False)
    btn_secondary_icon = db.Column(db.String(255), nullable=False)
    btn_secondary_link = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<CarouselItem {self.title}>'
    

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    paragraph1 = db.Column(db.Text, nullable=False)
    paragraph2 = db.Column(db.Text, nullable=False)
    paragraph3 = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    icon_class = db.Column(db.String(100), nullable=False)
    bg_class = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)  # Store as comma-separated values for simplicity

    def __init__(self, slug, name, icon, description, paragraph1, paragraph2, paragraph3, image, icon_class, bg_class, details):
        self.slug = slug
        self.name = name
        self.icon = icon
        self.description = description
        self.paragraph1 = paragraph1
        self.paragraph2 = paragraph2
        self.paragraph3 = paragraph3
        self.image = image
        self.icon_class = icon_class
        self.bg_class = bg_class
        self.details = details  # Comma-separated values for details


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    social_facebook = db.Column(db.String(100), nullable=True)
    social_twitter = db.Column(db.String(100), nullable=True)
    social_linkedin = db.Column(db.String(100), nullable=True)
    social_instagram = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=False)  # Store as comma-separated values
    education = db.Column(db.Text, nullable=False)  # Store as JSON string



#blog adding section
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    date = db.Column(db.String(50))
    image = db.Column(db.String(255))
    title = db.Column(db.String(255))
    excerpt = db.Column(db.Text)
    slug = db.Column(db.String(255), unique=True)
    published_on = db.Column(db.String(50))
    published_by = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text)  # Store as a comma-separated string
    gallery_images = db.Column(db.String(255))
    tags = db.Column(db.Text)  # Store as a comma-separated string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Blog {self.title}>"

    def get_features(self):
        return self.features.split(',')

    def get_tags(self):
        return self.tags.split(',')

    def get_content(self):
        return self.content.split('\n')
    

# Appointment model
class HomePageAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    services = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.name}>'





#OG-Loaduser
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#OG-User-Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)    
    company_name = db.Column(db.String(length=125), nullable=False, unique=True)
    name = db.Column(db.String(length=30))
    cnumb = db.Column(db.Integer())
    is_admin = db.Column(db.Boolean, default=False)
    
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}#'
        else:
            return f"{self.budget}#"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

#OG-Admin-data(item)
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    phone = db.Column(db.String(length=12), nullable=False, unique=True)
    email = db.Column(db.String(length=1024), nullable=False, unique=True)
    source = db.Column(db.String(length=124), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer())#, db.ForeignKey('user.company_id'))


    def __repr__(self):
        return f'Item {self.name}'
    

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

#feedback area
class AAFeedback(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    feedback = db.Column(db.Text(), nullable=False)
    Admin_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(25), nullable=False)


    def __init__(self, id, feedback, Admin_id, user_id, date):
      
      self.id = id
      self.feedback = feedback
      self.Admin_id = Admin_id
      self.user_id = user_id
      self.date = date


#Admins area
class Adminsupdate(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    campaign = db.Column(db.Text(), nullable=False)
    Admin_id = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(25), nullable=False)
    Admintype = db.Column(db.Text)
    Adminstatus = db.Column(db.Text)
    Admincategory = db.Column(db.Text)
    Adminlocation = db.Column(db.Integer)
    date = db.Column(db.Integer)


    def __repr__(self):
        return f"Adminsupdate(id={self.id})"
    