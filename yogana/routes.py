from yogana import app
from functools import wraps
from flask import Blueprint, g, abort, render_template, redirect, url_for, flash, request, jsonify, session
from yogana.models import Adminsupdate, Item, User, Feedback
from yogana.forms import AdminsupdateForm, AdminTypeOptionForm, ChangePasswordForm, RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, ItemForm, FeedbackForm, ProfileForm
from yogana import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

from yogana.models import Blog
from yogana.forms import BlogForm

from .models import FAQ, CarouselItem, HomePageAppointment, Doctor,Service, FunFact, MissionFeature, MissionSection, AboutSection , WhySection, VisionData

from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# Define a function to determine if a menu item should be active
def is_active(endpoint):
    return request.endpoint == endpoint

#Define to verify the current user is_admin = True(1) or Flase(0)
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print("Current User ID:", current_user.id)
        print("Is Authenticated:", current_user.is_authenticated)
        print("Is Admin:", current_user.is_admin)

        if not current_user.is_authenticated or not current_user.is_admin:
            print("Access Denied!")
            abort(403)  # Forbidden

        print("access")


        return func(*args, **kwargs)

    return decorated_view

@app.before_request
def before_request():
    # Create the appservices list
    dservices = Service.query.all()
    g.appservices = [{"name": service.name, "slug": service.slug} for service in dservices]

@app.context_processor
def inject_services():
    # This will make g.appservices available globally in all templates
    return dict(appservices=g.appservices)

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        g.user = user  # Store the user object in g
    else:
        g.user = None  # No user logged in


#=====================================================
#============= Admin Account Starts Here =============

# Views - Profile
@app.route('/admin/account/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = RegisterForm()

    form.name.data = current_user.name 
    form.username.data = current_user.username
    form.cnumb.data = current_user.cnumb
    form.email_address.data = current_user.email_address
    form.company_name.data = current_user.company_name
    
    if form.validate_on_submit():

        user_update = User(name=form.name.data,
                            cnumb=form.cnumb.data)
        
        db.session.add(user_update)
        db.session.commit()
        flash('Profile Saved successfully!', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Old password is incorrect. Please try again.', 'danger')

    return render_template('/account/profile.html', form=form, profile_active=is_active('profile'))

#changing password for the user
@app.route('/admin/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Old password is incorrect. Please try again.', 'danger')

    return render_template('/account/change_password.html', form=form, change_password_active=is_active('change_password'))

#User Register page
@app.route('/admin/account/user_register', methods=['GET', 'POST'])
@login_required
@admin_required 
def users_register():
    user_company_name = current_user.company_name

    form = RegisterForm()
    form.company_name.data = user_company_name
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              company_name= user_company_name,
                              name=form.name.data,
                              cnumb=form.cnumb.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('view_Admins'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('/account/user_register.html', form=form, users_register_active=is_active('users_register'))

#View Register page
@app.route('/admin/account/view_users', methods=['GET', 'POST'])
@login_required
@admin_required
def view_users():
    if request.method == "GET":
        items = User.query.filter_by(company_name=current_user.company_name)
        
        return render_template('/account/view_users.html', users=items, view_users_active=is_active('view_users'))
    
    return render_template('/account/view_users.html', users=items, view_users_active=is_active('view_users'))

#Admin Register page
@app.route('/admin/account/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              company_name=form.company_name.data,
                              name=form.name.data,
                              cnumb=form.cnumb.data,
                              is_admin = True)

        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('get_Admins'))
    if form.errors != {}: #If there are not errors from the validations
        print("errorhere", form.data)
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form, register_active=is_active('register'))

#OG-Login page
@app.route('/admin/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('admin_home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

#Admin-OG-Homepage
@app.route('/admin/home')
@login_required
def admin_home_page():
    form = ProfileForm()
    return render_template('dashboard.html', form=form, home_active=is_active('home'))

#OG-Logout
@app.route('/admin/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("admin_home_page"))
#===================  SECTION ENDS   =============================



#==================================================
#============= Error Works Starts Here=============
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error_control/404.html'), 404

# Handle 404 errors
@app.errorhandler(403)
def page_not_found(error):
    return render_template('/error_control/403.html'), 404
#===================  SECTION ENDS   =============================


#============= Error Works Ends Here===============

#================================================
#============= Redirect Instruction Here ================
@app.route('/index')
def redirect_to_home():
    return redirect(url_for('index'))

@app.route('/admin')
def redirect_to_admin():
    return redirect(url_for('admin_home_page'))
#===================  SECTION ENDS   =============================


#================================================
#============== Data's Starts Here ================


#======================================================

#================================================
#============== Home Starts Here ================
feedback_data = [
        {
            "name": "John Lucy",
            "role": "Founding Partner",
            "feedback": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Risus commodo viverra maecenas accumsan lacus vel facilisis.",
            "image": "static/site/img/client-image/2.jpg"
        }
    ]

#HomePage Area
@app.route('/')
def index():
    # Carousel data
    carousel_items = CarouselItem.query.all()
    mservices = WhySection.query.all()
    about_sections = AboutSection.query.all()
    mission_section = MissionSection.query.all()
    vision_data = VisionData.query.all()
    hfaqs  = FAQ.query.order_by(FAQ.created_at.desc()).limit(5).all()
    homedoctors = Doctor.query.order_by(Doctor.id.desc()).limit(4).all()
    sservices = Service.query.order_by(Service.id.desc()).limit(5).all()
    fun_facts = FunFact.query.order_by(FunFact.created_at.desc()).limit(5).all()
    mission_feature = MissionFeature.query.all()
    
    title = "YOGANA HOSPTIAL"



    success = request.args.get('success') == 'true'

    return render_template('/www/index.html', title=title, carousel_items=carousel_items,
                           mission_section=mission_section, fun_facts=fun_facts, mservices=mservices,
                           mission_feature=mission_feature, vision_data=vision_data, 
                           about_section=about_sections, services = sservices, homedoctors=homedoctors, 
                           feedbacks=feedback_data, faqs=hfaqs, success=success)






# Admin panel to view, add, edit, and delete FunFacts
@app.route("/admin/funfacts", methods=["GET", "POST"])
@login_required
def manage_funfacts():
    if request.method == "POST":
        # Add a new FunFact
        icon = request.form.get("icon")
        count = request.form.get("count")
        optional_icon = request.form.get("optional_icon")
        text = request.form.get("text")

        new_funfact = FunFact(
            icon=icon,
            count=int(count),  # Ensure count is integer
            optional_icon=optional_icon,
            text=text,
        )
        db.session.add(new_funfact)
        db.session.commit()
        flash("FunFact added successfully!", "success")

    # View all FunFacts
    funfacts = FunFact.query.all()
    return render_template("admin/manage_funfacts.html", funfacts=funfacts)


# Edit a FunFact
@app.route("/admin/funfacts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_funfact(id):
    funfact = FunFact.query.get_or_404(id)
    
    if request.method == "POST":
        # Update the FunFact
        funfact.icon = request.form.get("icon")
        funfact.count = request.form.get("count")
        funfact.optional_icon = request.form.get("optional_icon")
        funfact.text = request.form.get("text")
        
        db.session.commit()
        flash("FunFact updated successfully!", "success")
        return redirect(url_for('manage_funfacts'))
    
    return render_template("admin/edit_funfact.html", funfact=funfact)


# Delete a FunFact
@app.route("/admin/funfacts/delete/<int:id>", methods=["POST"])
@login_required
def delete_funfact(id):
    funfact = FunFact.query.get_or_404(id)
    db.session.delete(funfact)
    db.session.commit()
    flash("FunFact deleted successfully!", "danger")
    return redirect(url_for('manage_funfacts'))





# Admin panel to view, add, edit, and delete VisionData
@app.route("/admin/visiondata", methods=["GET", "POST"])
@login_required
def manage_visiondata():
    if request.method == "POST":
        # Add a new VisionData
        icon_class = request.form.get("icon_class")
        title = request.form.get("title")
        description = request.form.get("description")

        new_visiondata = VisionData(
            icon_class=icon_class,
            title=title,
            description=description,
        )
        db.session.add(new_visiondata)
        db.session.commit()
        flash("VisionData added successfully!", "success")

    # View all VisionData
    visiondata = VisionData.query.all()
    return render_template("admin/manage_visiondata.html", visiondata=visiondata)


# Edit a VisionData
@app.route("/admin/visiondata/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_visiondata(id):
    vision = VisionData.query.get_or_404(id)
    
    if request.method == "POST":
        # Update the VisionData
        vision.icon_class = request.form.get("icon_class")
        vision.title = request.form.get("title")
        vision.description = request.form.get("description")
        
        db.session.commit()
        flash("VisionData updated successfully!", "success")
        return redirect(url_for('manage_visiondata'))
    
    return render_template("admin/edit_visiondata.html", vision=vision)


# Delete a VisionData
@app.route("/admin/visiondata/delete/<int:id>", methods=["POST"])
@login_required
def delete_visiondata(id):
    vision = VisionData.query.get_or_404(id)
    db.session.delete(vision)
    db.session.commit()
    flash("VisionData deleted successfully!", "danger")
    return redirect(url_for('manage_visiondata'))




import os
app.config["CAROUSEL_IMAGE_FOLDER"] = "static/img/carousel_images"
os.makedirs(app.config['CAROUSEL_IMAGE_FOLDER'], exist_ok=True)

# Admin panel to view, add, edit, and delete CarouselItems
@app.route("/admin/carousel", methods=["GET", "POST"])
@login_required
def manage_carousel():
    if request.method == "POST":
        # Handle the image upload
        print("fdfd")
        image = request.files.get("image")  # Get the uploaded image
        if image and allowed_file(image.filename):  # Check if the image is valid
            print("fdfd")
            print(f"File uploaded: {image.filename}")
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["CAROUSEL_IMAGE_FOLDER"], filename)
            image.save(image_path)
        else:
            image = "site/img/main-banner1.jpg"  # If no image is uploaded, set it as None or a default image path
        
        # Other form data
        bg_class = "bg-9"
        title = request.form.get("title")
        headline = request.form.get("headline")
        description = request.form.get("description")
        btn_primary_text = request.form.get("btn_primary_text")
        btn_primary_icon = request.form.get("btn_primary_icon")
        btn_primary_link = request.form.get("btn_primary_link")
        btn_secondary_text = request.form.get("btn_secondary_text")
        btn_secondary_icon = request.form.get("btn_secondary_icon")
        btn_secondary_link = request.form.get("btn_secondary_link")

        # Create the new CarouselItem with the uploaded image path
        new_carousel_item = CarouselItem(
            image_url=image,  # Save the image path, not the FileStorage object
            bg_class=bg_class,
            title=title,
            headline=headline,
            description=description,
            btn_primary_text=btn_primary_text,
            btn_primary_icon=btn_primary_icon,
            btn_primary_link=btn_primary_link,
            btn_secondary_text=btn_secondary_text,
            btn_secondary_icon=btn_secondary_icon,
            btn_secondary_link=btn_secondary_link
        )
        
        # Add the new CarouselItem to the database
        db.session.add(new_carousel_item)
        db.session.commit()

        flash("Carousel Item added successfully!", "success")

    # View all CarouselItems
    carousel_items = CarouselItem.query.all()
    return render_template("admin/manage_carousel.html", carousel_items=carousel_items)


# Edit a CarouselItem
@app.route("/admin/carousel/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_carousel_item(id):
    print("fdfd")
    carousel_item = CarouselItem.query.get_or_404(id)

    print("fdfd")

    if request.method == "POST":
        image = request.files.get("image")
        if image:
            print(f"Image file received: {image.filename}")  # Debugging line
            
            if allowed_file(image.filename):  # Check if the file is allowed
                print("Valid image file")  # Debugging line
                
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config["CAROUSEL_IMAGE_FOLDER"], filename)
                
                # Save the image to the folder
                image.save(image_path)

                # Update the image URL in the database
                carousel_item.image_url = image_path
                print(f"Image saved at {image_path}")  # Debugging line
            else:
                print(f"Invalid file type: {image.filename}")  # Debugging line
        else:
            print("No image uploaded.")  # Debugging line

        # Continue updating other fields...
        carousel_item.bg_class = "bg-9"
        carousel_item.title = request.form.get("title")
        carousel_item.headline = request.form.get("headline")
        carousel_item.description = request.form.get("description")
        carousel_item.btn_primary_text = request.form.get("btn_primary_text")
        carousel_item.btn_primary_icon = request.form.get("btn_primary_icon")
        carousel_item.btn_primary_link = request.form.get("btn_primary_link")
        carousel_item.btn_secondary_text = request.form.get("btn_secondary_text")
        carousel_item.btn_secondary_icon = request.form.get("btn_secondary_icon")
        carousel_item.btn_secondary_link = request.form.get("btn_secondary_link")

        db.session.commit()
        flash("Carousel Item updated successfully!", "success")
        return redirect(url_for('manage_carousel'))

    return render_template("admin/edit_carousel_item.html", carousel_item=carousel_item)




# Delete a CarouselItem
@app.route("/admin/carousel/delete/<int:id>", methods=["POST"])
@login_required
def delete_carousel_item(id):
    carousel_item = CarouselItem.query.get_or_404(id)
    db.session.delete(carousel_item)
    db.session.commit()
    flash("Carousel Item deleted successfully!", "danger")
    return redirect(url_for('manage_carousel'))

from .models import WhySection
@app.route("/admin/whysection", methods=["GET", "POST"])
def manage_why():
    if request.method == "POST":
        # Handle file upload
        image = request.files.get('image')
        if image:
            # Save the image
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image_filename))
        
            # Save About Section
            why_section = WhySection(
                title=request.form.get('title'),
                description=request.form.get('description'),
                image=image_filename,
                button_text=request.form.get('button_text'),
                button_link=request.form.get('button_link')
            )
            db.session.add(why_section)
            db.session.commit()
            flash("Why Section added successfully!", "success")
            return redirect(url_for('manage_why'))
    
    why_sections = WhySection.query.all()
    return render_template("admin/manage_why.html", why_sections=why_sections)

@app.route("/admin/whysection/edit/<int:id>", methods=["GET", "POST"])
def edit_why(id):
    why_section = WhySection.query.get_or_404(id)
    if request.method == "POST":
        # Check if a new image is uploaded
        image = request.files.get('image')
        if image:
            why_section.image = image

        # Update other fields
        why_section.title = request.form.get('title')
        why_section.description = request.form.get('description')
        why_section.button_text = request.form.get('button_text')
        why_section.button_link = request.form.get('button_link')

        db.session.commit()
        flash("Why Section updated successfully!", "success")
        return redirect(url_for('manage_why'))

    return render_template("admin/edit_why.html", why_section=why_section)



@app.route("/admin/aboutsection", methods=["GET", "POST"])
def manage_about():
    if request.method == "POST":
        # Handle file upload
        image = request.files.get('image')
        if image:
            # Save the image
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], image_filename))
        
            # Save About Section
            about_section = AboutSection(
                title=request.form.get('title'),
                description=request.form.get('description'),
                image=image_filename,
                button_text=request.form.get('button_text'),
                button_link=request.form.get('button_link')
            )
            db.session.add(about_section)
            db.session.commit()
            flash("About Section added successfully!", "success")
            return redirect(url_for('manage_about'))
    
    about_sections = AboutSection.query.all()
    return render_template("admin/manage_about.html", about_sections=about_sections)


@app.route("/admin/aboutsection/edit/<int:id>", methods=["GET", "POST"])
def edit_about(id):
    about_section = AboutSection.query.get_or_404(id)
    if request.method == "POST":
        # Check if a new image is uploaded
        image = request.files.get('image')
        if image:
            about_section.image = image

        # Update other fields
        about_section.title = request.form.get('title')
        about_section.description = request.form.get('description')
        about_section.features = request.form.get('features')
        about_section.button_text = request.form.get('button_text')
        about_section.button_link = request.form.get('button_link')

        db.session.commit()
        flash("About Section updated successfully!", "success")
        return redirect(url_for('manage_about'))

    return render_template("admin/edit_about.html", about_section=about_section)


@app.route("/admin/aboutsection/delete/<int:id>", methods=["POST"])
def delete_about(id):
    about_section = AboutSection.query.get_or_404(id)
    db.session.delete(about_section)
    db.session.commit()
    flash("About Section deleted successfully!", "success")
    return redirect(url_for('manage_about'))


# Admin panel to view and edit Mission Section
@app.route('/admin/mission_sections')
def view_mission_sections():
    mission_sections = MissionSection.query.all()
    return render_template('admin/mission_sections.html', mission_sections=mission_sections)

@app.route('/admin/mission_sections/edit/<int:id>', methods=["GET", "POST"])
def edit_mission_section(id):
    mission_section = MissionSection.query.get_or_404(id)
    if request.method == "POST":
        mission_section.title = request.form["title"]
        mission_section.description = request.form["description"]
        mission_section.image = request.form["image"]
        mission_section.shape_image = request.form["shape_image"]
        db.session.commit()
        flash("Mission Section updated successfully!", "success")
        return redirect(url_for('view_mission_sections'))
    return render_template('admin/edit_mission_section.html', mission_section=mission_section)

# Admin panel to view and edit Mission Features
@app.route('/admin/mission_features')
def view_mission_features():
    mission_features = MissionFeature.query.all()
    return render_template('admin/mission_features.html', mission_features=mission_features)

@app.route('/admin/mission_features/edit/<int:id>', methods=["GET", "POST"])
def edit_mission_feature(id):
    mission_feature = MissionFeature.query.get_or_404(id)
    if request.method == "POST":
        mission_feature.icon = request.form["icon"]
        mission_feature.title = request.form["title"]
        mission_feature.description = request.form["description"]
        db.session.commit()
        flash("Mission Feature updated successfully!", "success")
        return redirect(url_for('view_mission_features'))
    return render_template('admin/edit_mission_feature.html', mission_feature=mission_feature)



#===================  SECTION ENDS   =============================


#======================================================

from .models import MissionFeature
#======================================================
#============== About Page Starts Here ================
@app.route('/about')
def about():
    mservices = WhySection.query.all()
    about_section = AboutSection.query.all()
    mission_section = MissionSection.query.all()
    mission_feature = MissionFeature.query.all()
    hfaqs  = FAQ.query.order_by(FAQ.created_at.desc()).limit(5).all()
    homedoctors = Doctor.query.order_by(Doctor.id.desc()).limit(5).all()
    services = Service.query.order_by(Service.id.desc()).limit(5).all()
    fun_facts = FunFact.query.order_by(FunFact.created_at.desc()).limit(5).all()
    vision_data = VisionData.query.all()
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
        }
    success = request.args.get('success') == 'true'

    return render_template('/www/about.html', pdata=pdatas, about_section=about_section, 
                           mission_section=mission_section, mission_feature=mission_feature, vision_data=vision_data,
                           services=services, success=success, fun_facts=fun_facts,
                           feedback_data=feedback_data)
#===================  SECTION ENDS   =============================


#======================================================
#============== Contact Page Starts Here ================
@app.route('/appointment', methods=['POST'])
def appointment():
    # Get the form data
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        services = request.form.get('services')
        phone = request.form.get('text')
        # Validation (basic example)
        if not name or not email or not services or not phone:
            return 'All fields are required! Please fill in all the fields.', 400

        # Store the appointment in the database
        new_appointment = HomePageAppointment(
            name=name,
            email=email,
            services=services,
            phone=phone
            )
        db.session.add(new_appointment)
        db.session.commit()

    # Redirect to the original page with a success message
    # You can include a query parameter to indicate success
    referring_page = request.referrer or url_for('about')
    return redirect(f"{referring_page}?success=true")

@app.route('/admin/appointments', methods=['GET', 'POST'])
def admin_appointments():
    # Fetch all appointments
    appointments = HomePageAppointment.query.order_by(HomePageAppointment.id.desc()).all()

    return render_template('admin/list_appointments.html', appointments=appointments)


@app.route('/admin/appointments/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    # Find the appointment by ID
    appointment = HomePageAppointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('admin_appointments'))


@app.route('/contact')
def contact():
    pdatas = {
        "title": "Contact Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "Contact Us", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1",  # Add dynamic background class if needed
        "inheader": "Send Message",
        "inh": "Drop us message for any query",
        "intext": "If you have an idea, we would love to hear about it.",
        "address":"174/4B, GST Road, Kilambakkam, Urapakkam",
        "email":"contact@yoganahospital.com",
        "phone1":"+91 82875 82875",
        "phone2":"044 2727 2727"
    }


    success_message = None  # Initialize a variable to store success message

    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        msg_subject = request.form['msg_subject']
        message = request.form['message']

        # Process the form data here (e.g., save to database, send an email)

        success_message = "Thank you for contacting us! We have received your message and will get back to you soon."

    return render_template('www/contact.html', pdata=pdatas, success_message=success_message)
#===================  SECTION ENDS   =============================


#======================================================
#============== Feedback Page Starts Here ================

@app.route('/feedback')
def feedback():
    feedback_data = "dd"
    return render_template('www/feedback.html', feedback_data=feedback_data)
#===================  SECTION ENDS   =============================



#======================================================
#============== FAQs Page Starts Here =================



@app.route('/faqs')
def faqs():
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    page_faqs = FAQ.query.all()
    return render_template('www/faqs.html', pdata=pdatas, faqs=page_faqs)

# Admin Panel Routes
@app.route('/admin/faqs')
def admin_faqs():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    # Fetch the FAQs manually with limit and offset
    faqs = FAQ.query.offset(offset).limit(per_page).all()

    # Count total number of FAQ entries to calculate total pages
    total_faqs = FAQ.query.count()
    total_pages = (total_faqs + per_page - 1) // per_page  # Calculate total number of pages

    return render_template('admin/view_faq.html', faqs=faqs, page=page, total_pages=total_pages)

@app.route("/admin/add_faq", methods=["GET", "POST"])
def add_faq():
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        new_faq = FAQ(question=question, answer=answer)
        db.session.add(new_faq)
        db.session.commit()
        return redirect("admin_faqs")
    return render_template("admin/add_faq.html")

@app.route("/edit_faq/<int:id>", methods=["GET", "POST"])
def edit_faq(id):
    faq = FAQ.query.get_or_404(id)
    if request.method == "POST":
        faq.question = request.form["question"]
        faq.answer = request.form["answer"]
        db.session.commit()
        return redirect("/faqs")
    return render_template("admin/edit_faq.html", faq=faq)

@app.route("/delete_faq/<int:id>")
def delete_faq(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    return redirect("/faqs")

#===================  SECTION ENDS   =============================


#======================================================
#============== Departments Page Starts Here ==========

SERVICE_IMAGE_FOLDER = 'site/img/services/'
app.config['SERVICE_IMAGE_FOLDER']=SERVICE_IMAGE_FOLDER

# Admin panel to view all services
@app.route("/admin/department")
@login_required  # Ensure only logged-in users can access this
def admin_departments():
    services = Service.query.all()
    return render_template("admin/view_department.html", services=services)

# Admin panel to add a new service
@app.route("/admin/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
    if request.method == "POST":
        # Handle form data
        slug = request.form.get("slug")
        name = request.form.get("name")
        icon = request.form.get("icon")
        description = request.form.get("description")
        paragraph1 = request.form.get("paragraph1")
        paragraph2 = request.form.get("paragraph2")
        paragraph3 = request.form.get("paragraph3")
        image = request.files.get("image")
        icon_class = request.form.get("icon_class")
        bg_class = "bg-9"
        details = request.form.get("details")

       # Handle the image upload
        image = request.files["image"]
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the image folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["SERVICE_IMAGE_FOLDER"], filename)
            image.save(image_path)
            image_filename = f"{SERVICE_IMAGE_FOLDER}{filename}"
        else:
            # Use a default placeholder image if no valid image is provided
            image_filename = f"{SERVICE_IMAGE_FOLDER}default-department.jpg"

        # Add service to the database
        new_service = Service(
            slug=slug,
            name=name,
            icon=icon,
            description=description,
            paragraph1=paragraph1,
            paragraph2=paragraph2,
            paragraph3=paragraph3,
            image=image_filename,
            icon_class=icon_class,
            bg_class=bg_class,
            details=details
        )
        db.session.add(new_service)
        db.session.commit()

        flash("New service added successfully!", "success")
        return redirect(url_for('admin_departments'))
    
    return render_template("admin/add_department.html")

@app.route("/admin/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    service = Service.query.get_or_404(id)

    if request.method == "POST":
        # Handle form data
        service.slug = request.form.get("slug")
        service.name = request.form.get("name")
        service.icon = request.form.get("icon")
        service.description = request.form.get("description")
        service.paragraph1 = request.form.get("paragraph1")
        service.paragraph2 = request.form.get("paragraph2")
        service.paragraph3 = request.form.get("paragraph3")
        service.icon_class = request.form.get("icon_class")
        service.bg_class = "bg-9"
        service.details = request.form.get("details")

       # Handle the image upload
        image = request.files["image"]
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the image folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["SERVICE_IMAGE_FOLDER"], filename)
            image.save(image_path)
            image_filename = f"{SERVICE_IMAGE_FOLDER}{filename}"
        else:
            # Use a default placeholder image if no valid image is provided
            image_filename = f"{SERVICE_IMAGE_FOLDER}1.jpg"

        db.session.commit()

        flash("Service updated successfully!", "success")
        return redirect(url_for('admin_departments'))
    return render_template("admin/edit_department.html", service=service)
    

# Admin panel to delete a service
@app.route("/admin/departments/delete/<int:id>", methods=["POST"])
@login_required
def delete_department(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully!", "danger")
    return redirect(url_for('admin_departments'))


@app.route("/departments")
def department():
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    dservices = Service.query.all()
    return render_template("www/departments.html", pdata=pdatas, services=dservices)


@app.route("/departments/<slug>")
def departments_details(slug):
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }

    # Find the service with the matching slug
    # Find the service with the matching slug from the database
    service = Service.query.filter_by(slug=slug).first()
    if not service:
        return "Service not found", 404
    
    # Fetch all services for the sidebar
    dservices = Service.query.all()
    return render_template("www/departments_detail.html", pdata=pdatas, service=service, services=dservices)

#===================  SECTION ENDS   =============================


#======================================================
#============== Departments Page Starts Here ==========
import os
app.config['DOCTOR_IMAGE_FOLDER'] = os.path.join('static', 'site', 'img','doctor')
os.makedirs(app.config['DOCTOR_IMAGE_FOLDER'], exist_ok=True)
DOCTOR_IMAGE_FOLDER = "site/img/doctor/"

@app.route("/admin/doctors")
def admin_doctors():
    doctors = Doctor.query.all()
    return render_template("admin/list_doctors.html", doctors=doctors)

@app.route("/admin/doctors/new", methods=["GET", "POST"])
def new_doctor():
    if request.method == "POST":
        name = request.form["name"]
        slug = request.form["slug"]
        specialty = request.form["specialty"]
        description = request.form["description"]
        social_facebook = request.form["social_facebook"]
        social_twitter = request.form["social_twitter"]
        social_linkedin = request.form["social_linkedin"]
        social_instagram = request.form["social_instagram"]
        skills = request.form["skills"]
        education = request.form["education"]

        # Handle the image upload
        image = request.files["image"]
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["DOCTOR_IMAGE_FOLDER"], filename)
            image.save(image_path)
            doctor.image = f"{DOCTOR_IMAGE_FOLDER}{filename}"  # Update the doctor's image field
        else:
            # Use a default placeholder image if no valid image is provided
            doctor_image = f"{DOCTOR_IMAGE_FOLDER}default-doctor.jpg"

        doctor = Doctor(
            name=name,
            slug=slug,
            specialty=specialty,
            image=image,
            description=description,
            social_facebook=social_facebook,
            social_twitter=social_twitter,
            social_linkedin=social_linkedin,
            social_instagram=social_instagram,
            skills=skills,
            education=education,
        )
        db.session.add(doctor)
        db.session.commit()
        flash("Doctor added successfully!")
        return redirect(url_for("admin_doctors"))

    return render_template("admin/add_doctor.html")

@app.route("/admin/doctors/edit/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    if request.method == "POST":
        doctor.name = request.form["name"]
        doctor.slug = request.form["slug"]
        doctor.specialty = request.form["specialty"]
        doctor.description = request.form["description"]
        doctor.social_facebook = request.form["social_facebook"]
        doctor.social_twitter = request.form["social_twitter"]
        doctor.social_linkedin = request.form["social_linkedin"]
        doctor.social_instagram = request.form["social_instagram"]
        doctor.skills = request.form["skills"]
        doctor.education = request.form["education"]


        # Handle the image upload
        image = request.files["image"]
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["DOCTOR_IMAGE_FOLDER"], filename)
            image.save(image_path)
            doctor.image = f"{DOCTOR_IMAGE_FOLDER}{filename}"  # Update the doctor's image field
        else:
            # Use a default placeholder image if no valid image is provided
            doctor.image = f"{DOCTOR_IMAGE_FOLDER}default-doctor.jpg"

        db.session.commit()
        flash("Doctor updated successfully!")
        return redirect(url_for("admin_doctors"))

    return render_template("admin/edit_doctor.html", doctor=doctor)

@app.route("/admin/doctors/delete/<int:id>", methods=["POST"])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash("Doctor deleted successfully!")
    return redirect(url_for("admin_doctors"))


# Define the doctors' data
@app.route("/doctors")
def doctors():
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    doctorspage = Doctor.query.all()
    return render_template("www/doctors.html", pdata=pdatas, doctors=doctorspage)

@app.route("/doctors/<slug>")
def doctor_details(slug):
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    # Find the doctor by name
    doctor = Doctor.query.filter_by(slug=slug).first_or_404()
    
    return render_template("www/doctor_details.html", pdata=pdatas, doctor=doctor)

#===================  SECTION ENDS   =============================



#================================================
#============= Blogs Starts Here ================
import json
BLOG_IMAGE_FOLDER = "site/img/blog/"
app.config['BLOG_IMAGE_FOLDER']=BLOG_IMAGE_FOLDER
os.makedirs(app.config['BLOG_IMAGE_FOLDER'], exist_ok=True)

@app.route('/admin/blogs', methods=['GET'])
def list_blogs():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/list_blogs.html', blogs=blogs, title="Blog List")

# Add a new blog
@app.route('/admin/blogs/add', methods=['GET', 'POST'])
def add_blog():
    form = BlogForm()

    if form.validate_on_submit():
        # Handle the main blog image
        image = request.files['image']
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["BLOG_IMAGE_FOLDER"], filename)
            image.save(image_path)
        else:
            image_path = None  # Handle case where no image is uploaded

        # Handle the gallery images (if any)
        gallery_images = form.gallery_images.data
        if gallery_images and allowed_file(gallery_images.filename):
            # Secure the filename and save it to the upload folder
            gfilename = secure_filename(gallery_images.filename)
            gimage_path = os.path.join(app.config["BLOG_IMAGE_FOLDER"], gfilename)
            gallery_images.save(gimage_path)
        else:
            gimage_path = None  # Handle case where no gallery image is uploaded

        # Create the new blog entry and save it to the database
        new_blog = Blog(
            author=form.author.data,
            date=form.date.data,
            title=form.title.data,
            excerpt=form.excerpt.data,
            slug=form.slug.data,
            published_on=datetime.now(),
            published_by="admin",
            content=form.content.data,  # Use form.content.data for actual content
            features=form.features.data,
            tags=form.tags.data,

            image=image_path,  # Save the file path (not the FileStorage object)
            gallery_images=gimage_path  # Save the gallery file path (not the FileStorage object)
        )

        db.session.add(new_blog)
        db.session.commit()

        flash('Blog added successfully!', 'success')
        return redirect(url_for('list_blogs'))

    return render_template('admin/add_blog.html', form=form)

# Edit an existing blog
@app.route('/admin/blogs/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm(obj=blog)

    if form.validate_on_submit():
        # Update the fields with the form data
        blog.author = form.author.data
        blog.date = form.date.data
        blog.title = form.title.data
        blog.excerpt = form.excerpt.data
        blog.slug = form.slug.data
        blog.published_on = datetime.now()
        blog.published_by = "admin"
        blog.content = form.content.data  # Store as plain text
        blog.features = ','.join(form.features.data.split(','))
        blog.tags = ','.join(form.tags.data.split(','))

        # Handle the main image (if updated)
        image = request.files.get('image')  # Get the uploaded image file
        if image and allowed_file(image.filename):
            # Secure the filename and save it to the upload folder
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["BLOG_IMAGE_FOLDER"], filename)
            image.save(image_path)
            blog.image = image_path  # Update the blog's image with the new path

        # Handle gallery images (if updated)
        gallery_images = request.files.get('gallery_images')  # Get the uploaded gallery images
        if gallery_images and allowed_file(gallery_images.filename):
            # Secure the filename and save it to the upload folder
            gfilename = secure_filename(gallery_images.filename)
            gimage_path = os.path.join(app.config["BLOG_IMAGE_FOLDER"], gfilename)
            gallery_images.save(gimage_path)
            blog.gallery_images = gimage_path  # Update the blog's gallery_images with the new path

        db.session.commit()
        flash('Blog updated successfully!', 'success')
        return redirect(url_for('list_blogs'))
    
    return render_template('admin/edit_blog.html', form=form, blog=blog)

# Delete a blog
@app.route('/admin/blogs/delete/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog deleted successfully!', 'success')
    return redirect(url_for('list_blogs'))

# Route to view all blogs
@app.route('/blogs')
def blogs():
    pdatas = {
        "title": "About Us",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "About Us", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    all_blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('www/blogs.html', pdata=pdatas, blogs=all_blogs)

@app.route('/blogs/<slug>', methods=['GET'])
def blog_details(slug):
    # Retrieve all blogs
    all_blogs = Blog.query.order_by(Blog.created_at.desc()).all()

    # Retrieve the specific blog by its slug
    lblog = Blog.query.filter_by(slug=slug).first_or_404()

    # Convert string date to datetime object and sort by the latest
    sorted_blogs = sorted(all_blogs, key=lambda x: datetime.strptime(x.published_on, '%B %d, %Y'), reverse=True)
    latest_blogs = sorted_blogs[:5]  # Get the latest 5 posts

    # Extract and count tags from the specific blog
    #tag_counts = {}
    #for tag in lblog.tags.split(','):  # assuming tags are stored as comma-separated strings
    #    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    tag_counts = lblog.tags

    # Prepare the page data for breadcrumbs, background image, etc.
    pdatas = {
        "title": "Blog Details",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "Blog Details", "url": None}  # None for the current page
        ],
        "bg_image": "/site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }

    # Pass the relevant data to the template
    return render_template('www/blog_details.html', pdata=pdatas, 
                           blog_post=lblog, tag_counts=tag_counts, latest_blogs=latest_blogs)

@app.route('/latest-posts')
def latest_posts():
    all_blogs = Blog.query.all()
    # Convert string date to datetime object and sort by the latest
    sorted_blogs = sorted(all_blogs, key=lambda x: datetime.strptime(x['published_on'], '%B %d, %Y'), reverse=True)
    latest_blogs = sorted_blogs[:5]  # Get the latest 5 posts
    return render_template('www/components/latest_posts.html', latest_blogs=latest_blogs)

@app.route("/search", methods=["GET", "POST"])
def search():
    all_blogs = Blog.query.all()
    query = request.args.get('q', '')  # Get the search query from the URL
    results = []
    
    # If there is a search query, filter the blogs based on the title match
    if query:
        results = [blog for blog in all_blogs if query.lower() in blog["title"].lower()]
    
    return render_template("www/search_results.html", query=query, results=results)

#============= Blogs Ends Here   ===============


#====================================================================================
#=======================   HTML Editor   ==================================
#====================================================================================
import os

# Path to the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/www')


@app.route('/admin/templates', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_templates():
    # List all HTML files in the templates directory
    html_files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith('.html')]

    if request.method == 'POST':
        selected_file = request.form.get('file_name')
        if selected_file:
            # Redirect to edit the selected file
            return redirect(url_for('edit_template', file_name=selected_file))

    return render_template('admin/admin_templates.html', html_files=html_files)


@app.route('/admin/templates/edit/<file_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_template(file_name):
    file_path = os.path.join(TEMPLATES_DIR, file_name)

    if not os.path.exists(file_path):
        flash('File not found!', 'danger')
        return redirect(url_for('admin_templates'))

    if request.method == 'POST':
        # Save the updated content to the file
        updated_content = request.form.get('file_content')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        flash(f'{file_name} has been updated successfully!', 'success')
        return redirect(url_for('admin_templates'))

    # Load the content of the selected file
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    return render_template('admin/edit_template.html', file_name=file_name, file_content=file_content)

#====================================================================================
#============================   CS/JS Editor   ======================================
#====================================================================================

# Paths to specific files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(BASE_DIR, 'static', 'css', 'style1.css')
JS_FILE = os.path.join(BASE_DIR, 'static', 'js', 'main.js')

# Route to display the menu for file editing
@app.route('/admin/files', methods=['GET'])
@login_required
@admin_required
def admin_files():
    return render_template('admin/admin_files.html')

# Route to edit the CSS file
@app.route('/admin/files/css', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_css():
    if request.method == 'POST':
        # Save the updated CSS file content
        updated_content = request.form.get('file_content')
        with open(CSS_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        flash('CSS file has been updated successfully!', 'success')
        return redirect(url_for('admin_files'))

    # Load the current content of the CSS file
    with open(CSS_FILE, 'r', encoding='utf-8') as f:
        file_content = f.read()

    return render_template('admin/edit_file.html', file_name='style1.css', file_content=file_content)


# Route to edit the JS file
@app.route('/admin/files/js', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_js():
    if request.method == 'POST':
        # Save the updated JS file content
        updated_content = request.form.get('file_content')
        with open(JS_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        flash('JS file has been updated successfully!', 'success')
        return redirect(url_for('admin_files'))

    # Load the current content of the JS file
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        file_content = f.read()

    return render_template('admin/edit_file.html', file_name='main.js', file_content=file_content)



#======================================================================================
#=======================   Header Data Admin Panel   ==================================
#======================================================================================

from .models import HospitalInfo

@app.route('/admin/hospital-info', methods=['GET', 'POST'])
def manage_hospital_info():
    # Fetch the current hospital info
    hospital_info = HospitalInfo.query.first()

    if request.method == 'POST':
        # Extract data from the form
        service_hours = request.form.get('service_hours')
        phone = request.form.get('phone')
        email = request.form.get('email')
        facebook_url = request.form.get('facebook_url')
        twitter_url = request.form.get('twitter_url')
        linkedin_url = request.form.get('linkedin_url')
        instagram_url = request.form.get('instagram_url')

        # Update or create the hospital info
        if hospital_info:
            hospital_info.service_hours = service_hours
            hospital_info.phone = phone
            hospital_info.email = email
            hospital_info.facebook_url = facebook_url
            hospital_info.twitter_url = twitter_url
            hospital_info.linkedin_url = linkedin_url
            hospital_info.instagram_url = instagram_url
        else:
            hospital_info = HospitalInfo(
                service_hours=service_hours,
                phone=phone,
                email=email,
                facebook_url=facebook_url,
                twitter_url=twitter_url,
                linkedin_url=linkedin_url,
                instagram_url=instagram_url,
            )
            db.session.add(hospital_info)

        db.session.commit()
        flash('Hospital Information updated successfully!', 'success')
        return redirect(url_for('manage_hospital_info'))

    return render_template('admin/hospital_info.html', hospital_info=hospital_info)





#====================================================================================
#=======================  Calculators Start Here    =================================
#====================================================================================
from .models import PeriodData, BMICalculatorData, OvulationData, DuedateData

@app.route('/period_calculator', methods=['GET', 'POST'])
def period_calculator():
    pdatas = {
        "title": "Period Calculator",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "Period Calculator", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    
    new_entry_result = None
    previous_entry = None
    breadcrumbs = [("Home", "/"), ("Period00-00Calculator", None)]  # Example breadcrumb trail

    try:
        if request.method == 'POST':
            # Fetch form data
            name = request.form['name']
            number = request.form['number']
            email = request.form['email']
            last_period_date_str = request.form['date']
            cycle_length_str = request.form['clength']  # Get the cycle length from form

            # Parse dates and cycle length
            last_period_date = datetime.strptime(last_period_date_str, "%Y-%m-%d")
            cycle_length = int(cycle_length_str)  # Convert cycle length to an integer

            # Check for a previous entry based on email
            previous_entry = PeriodData.query.filter_by(email=email).first()

            # Calculate next period date using the provided cycle length
            next_period_date = last_period_date + timedelta(days=cycle_length)

            if previous_entry:
                flash("Previous entry found. Showing previous and current calculation results.", "info")
            else:
                # Create and save the new entry if no previous entry exists
                new_entry = PeriodData(
                    name=name,
                    number=number,
                    email=email,
                    last_period_date=last_period_date,
                    next_period_date=next_period_date,
                    cycle_length=cycle_length  # Store the cycle length if needed
                )
                db.session.add(new_entry)
                db.session.commit()

                # Display the new entry result
                new_entry_result = new_entry
                flash("New calculation completed!", "success")

        # Render the template with both previous and new entry results
        return render_template('www/period-calculator.html', pdata=pdatas, breadcrumbs=breadcrumbs, title="Period Calculator", previous_entry=previous_entry, new_entry_result=new_entry_result
        )

    except Exception as e:
        flash(f"Error in period calculator: {e}", "error")
        return render_template('www/period-calculator.html', pdata=pdatas, breadcrumbs=breadcrumbs, title="Period Calculator")


   # return render_template('www/period-calculator.html', breadcrumbs=breadcrumbs, title="Ovulation Calculator", previous_entry=previous_entry, new_entry_result=new_entry_result )

@app.route('/admin/view_period_data')
@login_required
def view_period_data():
    # Get the page number from the query string, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page

    # Query the PeriodData table with pagination
    period_data = PeriodData.query.order_by(PeriodData.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/view_period_data.html', period_data=period_data)

def calculate_ovulation_date(last_period):
    ovulation_date = last_period + timedelta(days=14)
    fertile_start = ovulation_date - timedelta(days=3)  # Day 11 to 13
    fertile_end = ovulation_date + timedelta(days=2)    # Day 15 to 16
    fertility_window = f"{fertile_start.date()} to {fertile_end.date()}"

    return ovulation_date, fertility_window

@app.route('/ovulation-calculator', methods=['GET', 'POST'])
def ovulation_calculator():
    pdatas = {
        "title": "Ovulation Calculator",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "Ovulation Calculator", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
     
    previous_entry = None
    new_entry_result = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            number = request.form['number']
            email = request.form['email']
            last_period_date = request.form['date']

            # Parse last period date and calculate ovulation data
            last_period = datetime.strptime(last_period_date, '%Y-%m-%d')
            ovulation_date = last_period + timedelta(days=14)
            fertile_start = ovulation_date - timedelta(days=5)
            fertile_end = ovulation_date + timedelta(days=1)
            fertile_days = f"{fertile_start.strftime('%Y-%m-%d')} to {fertile_end.strftime('%Y-%m-%d')}"

            # Check for previous entries based on email
            previous_entry = OvulationData.query.filter_by(email=email).first()

            # Save the new entry with the current data
            new_entry = OvulationData(
                name=name,
                number=number,
                email=email,
                last_period_date=last_period,
                ovulation_date=ovulation_date,
                fertile_days=fertile_days
            )
            db.session.add(new_entry)
            db.session.commit()

            # Store the calculated result to display
            new_entry_result = {
                'name': name,
                'number': number,
                'email': email,
                'last_period_date': last_period_date,
                'ovulation_date': ovulation_date,
                'fertile_days': fertile_days
            }

        except Exception as e:
            # Rollback the session if an error occurs
            db.session.rollback()
            flash("An error occurred while processing your request. Please try again.", "error")
            print(f"Error in ovulation calculator: {e}")

    return render_template('www/ovulation-calculator.html', pdata=pdatas, title="Ovulation Calculator", previous_entry=previous_entry, new_entry_result=new_entry_result)

@app.route('/admin/view_ovulation_data')
@login_required
def view_ovulation_data():
    # Get the page number from the query string, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page

    # Query the OvulationData table with pagination
    ovulation_data = OvulationData.query.order_by(OvulationData.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/view_ovulation_data.html', ovulation_data=ovulation_data)

@app.route('/due-date-calculator', methods=['GET', 'POST'])
def due_date_calculator():
    pdatas = {
        "title": "Due Date Calculator",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "Due Date Calculator", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }
    new_entry_result = None

    if request.method == 'POST':
        try:
            # Collect form inputs
            name = request.form['name']
            email = request.form['email']
            number = request.form['number']  # Adding phone number input
            last_period_date_str = request.form['last_period_date']
            
            # Parse last period date
            last_period_date = datetime.strptime(last_period_date_str, "%Y-%m-%d")
            
            # Calculate estimated due date (280 days from LMP)
            estimated_due_date = last_period_date + timedelta(days=280)
            
            # Create a new database entry
            new_entry = DuedateData(
                name=name,
                email=email,
                number=number,
                last_period_date=last_period_date,
                due_date=estimated_due_date.strftime("%Y-%m-%d")
            )
            
            # Add and commit to the database
            db.session.add(new_entry)
            db.session.commit()
            
            # Store current calculation result
            new_entry_result = {
                "name": name,
                "email": email,
                "number": number,
                "last_period_date": last_period_date.strftime("%Y-%m-%d"),
                "estimated_due_date": estimated_due_date.strftime("%Y-%m-%d")
            }
            
            # Flash success message
            flash("Your due date calculation has been saved successfully!", "success")
        
        except Exception as e:
            print(f"Error in Due Date Calculator: {e}")
            db.session.rollback()  # Rollback any changes if there's an error
            return render_template(
                'www/due-date-calculator.html', pdata=pdatas,
                error_message="There was an error saving your data. Please try again."
            )

    return render_template('www/due-date-calculator.html', 
                           pdata=pdatas, new_entry_result=new_entry_result)

@app.route('/admin/view_due_data')
@login_required
def view_due_data():
    # Get the page number from the query string, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page

    # Query the DuedateData table with pagination
    due_data = DuedateData.query.order_by(DuedateData.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/view_due_data.html', due_data=due_data)

@app.route('/bmi-calculator', methods=['GET', 'POST'])
def bmi_calculator():
    pdatas = {
        "title": "BMI Calculator",
        "breadcrumbs": [
            {"text": "Home", "url": "/"},
            {"text": "BMI Calculator", "url": None}  # None for the current page
        ],
        "bg_image": "site/img/yoganahospital-banner-1920_500.jpg",
        "bg_class": "page-title-bg1"  # Add dynamic background class if needed
    }

    new_entry_result = None
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            weight = float(request.form['weight'])
            height = float(request.form['height'])

            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)
            bmi_category = categorize_bmi(bmi)

            # Create a new database entry
            new_entry = BMICalculatorData(
                 name=name,
                email=email,
                weight=weight,
                height=height,
                bmi=round(bmi, 2),
                bmi_category=bmi_category
            )
            
            # Add and commit to the database
            db.session.add(new_entry)
            db.session.commit()


            new_entry_result = {
                "name": name,
                "email": email,
                "weight": weight,
                "height": height,
                "bmi": round(bmi, 2),
                "bmi_category": bmi_category,
 #               "date": datetime.now().strftime("%Y-%m-%d"),
            }
            db.session.add(new_entry_result)
            db.session.commit()



        except Exception as e:
            print(f"Error in BMI Calculator: {e}")
            return render_template('www/bmi-calculator.html', error_message=str(e), pdata = pdatas,  new_entry_result=new_entry_result)
        


        # Example BMI calculation and insertion into database

    return render_template('www/bmi-calculator.html', 
                           pdata = pdatas,  
                           new_entry_result=new_entry_result)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

@app.route('/admin/view_bmi_data')
@login_required
def view_bmi_data():
    # Get the page number from the query string, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page

    # Query the BMICalculatorData table with pagination
    bmi_data = BMICalculatorData.query.order_by(BMICalculatorData.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/view_bmi_data.html', bmi_data=bmi_data)

#============================ Calculators Ends Here   ==============================