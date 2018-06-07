from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Points, Report
import bcrypt

# main login/registration
def index(request):
    return render(request, 'timecard_app_templates/index.html')

# any other route that someone types in the url will redirect them back to home
def home(request):
    if "id" not in request.session:
        return redirect('/index')
    return render(request, 'timecard_app_templates/home.html')

def points(request):
    return render(request, 'timecard_app_templates/points.html')

def user(request, user_id):
    return render(request, 'timecard_app_templates/user.html')

# registration route to process errors/validation and storage of new user
def registration(request):
    if request.method == 'POST':
        errors = User.objects.validate_user(request.POST)

        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect('/index')

        messages.success(request, "you successfully registered!!!")
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        date_joined = request.POST['date_joined']
        role = request.POST['role']
        hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, date_joined=date_joined, password=hash_password, role=role)
        user = User.objects.get(first_name=first_name, last_name=last_name, email=email, password=hash_password, role=role)
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
    return redirect('/home')

# login route to check vallidations and make sure user is in database
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
    
        get_user = User.objects.filter(email=email)
        if (get_user):
            user_password = get_user[0].password
            check = bcrypt.checkpw(password.encode(), user_password.encode())
            if check == True:
                request.session['id'] = get_user[0].id
                request.session['name'] = get_user[0].name
                messages.success(request, "you successfully logged in!!!")
                return redirect('/home')
            else:
                messages.error(request, "Incorrect Password.")
        else:
            messages.error(request, "Email is not in our database.")
    return redirect('/index')

# logs user out
def logout(request):
    messages.success(request, "you successfully logged out!")
    request.session.clear()
    return redirect('/index')
