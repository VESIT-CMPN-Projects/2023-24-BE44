import numpy as np
from tensorflow.keras.models import load_model
from sklearn.decomposition import PCA
import cv2
from django.views.decorators.csrf import csrf_exempt
import os
import logging
from datetime import datetime
from django.http import HttpResponse
from .models import User
import base64
from .models import TempPerson, StaffDAOImpl, ReUniteDAO
from .validations import StaffValidation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid
import subprocess

# Configure logging
log_file_path = '/log_file.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@csrf_exempt
def init_logging(request):
    try:
        # Create or open the log file
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w'):
                pass
        logger.info('Logging initialized')
        return HttpResponse('Logging initialized successfully')
    except Exception as e:
        logger.error(f'Error initializing logging: {e}')
        return HttpResponse('Error initializing logging', status=500)


@csrf_exempt
def close_logging(request):
    try:
        # Close the log file
        logger.info('Logging closed')
        return HttpResponse('Logging closed successfully')
    except Exception as e:
        logger.error(f'Error closing logging: {e}')
        return HttpResponse('Error closing logging', status=500)


logger = logging.getLogger(__name__)


def get_registration(request):
    return render(request, 'reunite-registration.html')


def submit_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        user_id = request.POST.get('userId')
        password = request.POST.get('password')

        print("Username:", username)
        print("Email:", email)
        print("Phone Number:", phone_number)
        print("User ID:", user_id)
        print("Password:", password)

        # Create a User object
        user = User(username=username, email=email, phone_number=phone_number, user_id=user_id, password=password)

        # Perform validation and database operations
        message = StaffValidation.is_the_user_approved(user)
        if message:
            return redirect('/registration/?error=' + message)
        if StaffDAOImpl.find_user(user.username.strip()):
            return redirect('/registration/?errorunae')
        if StaffDAOImpl.add_user(user) == 1:
            if ReUniteDAO.add_person(username, email, phone_number, user_id, password):
                try:
                    log_message = f"\nAt [{get_current_timestamp()}] a new user was registered with username: {username}."
                    logger.info(log_message)
                except Exception as e:
                    print("Error in writing into the file.")
                    print(e)
                return redirect('/user')
            else:
                return redirect('/registration?error')
        return redirect('/registration?error')

    return HttpResponse("Method not allowed", status=405)


@login_required
def get_home_page(request):
    try:
        log_message = f"\nAt [{get_current_timestamp()}] "
        logger.info(log_message)
    except Exception as e:
        print("Error in writing into the file.")
        print(e)
    return redirect('/user')


@login_required
def get_user_page(request):
    username = request.user.username
    return render(request, 'reunite-home.html', {'username': username, 'path': '/servletContextPath'})


@login_required
def get_service(request):
    username = request.user.username
    return render(request, 'reunite-services.html', {'username': username, 'path': '/servletContextPath'})


def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@login_required
def get_found_page(request):
    username = request.user.username
    return render(request, 'reunite-found.html', {'username': username, 'path': '/servletContextPath'})


def match_images(image1_path, image2_path):
    model = load_model('keras_model.h5')

    image1 = preprocess_image(image1_path)
    image2 = preprocess_image(image2_path)

    prediction1 = model.predict(image1)
    prediction2 = model.predict(image2)

    similarity = calculate_similarity(prediction1, prediction2)

    return similarity > 0.85


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (64, 64))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = image.flatten()
    pca = PCA(n_components=90, whiten=True)
    pca_model = np.load('pca_model.npy', allow_pickle=True)
    pca.components_ = pca_model
    image_pca = pca.transform([image])
    image_pca = image_pca.reshape((1, -1))
    return image_pca


def calculate_similarity(prediction1, prediction2):
    similarity = np.dot(prediction1, prediction2.T) / (np.linalg.norm(prediction1) * np.linalg.norm(prediction2))

    return similarity


@login_required
def submit_found(request):
    if request.method == 'POST':
        person_image = request.FILES['myimage']
        matched_person = TempPerson()
        list_of_temp_person = TempPerson.objects.all()

        for temp_person in list_of_temp_person:
            temp_person.person_url = person_image

        confidence = 0.0
        flag = False

        try:
            for temp_person in list_of_temp_person:
                result = match_images(person_image, temp_person)
                if result:
                    print(temp_person.person_name + " has a match percentage of " + str(confidence) + "%.")
                else:
                    print("There was an issue processing the image for " + temp_person.person_name)
        except Exception as e:
            print(e)

        return render(request, 'reunite-found-result.html', {
            'person_name': matched_person.person_name,
            'person_age': matched_person.person_age,
            'person_gender': matched_person.person_gender,
            'person_aadhar': matched_person.person_aadhar,
            'confidence': confidence,
            'username': request.user.username,
            'path': '/servletContextPath',
        })

    return HttpResponse("Method not allowed", status=405)


@login_required
def get_report(request):
    username = request.user.username
    return render(request, 'reunite-report.html', {'username': username, 'path': '/servletContextPath'})


@login_required
def submit_report(request):
    if request.method == 'POST':
        person_aadhar = request.POST['personAadhar']
        person_name = request.POST['personName']
        person_age = int(request.POST['personAge'])
        person_gender = request.POST['personGender']
        photo_year = int(request.POST['photoYear'])
        person_image = request.FILES['myimage']

        image_base64 = base64.b64encode(person_image.read()).decode()

        temp_person = TempPerson.objects.create(
            person_name=person_name,
            person_age=person_age,
            person_gender=person_gender,
            photo_year=photo_year,
            person_aadhar=person_aadhar,
            person_image=person_image
        )

        return render(request, 'reunite-report-result.html', {
            'imageBase64': image_base64,
            'personName': person_name,
            'personAge': person_age,
            'personGender': person_gender,
            'photoYear': photo_year,
            'personAadhar': person_aadhar,
            'path': '/servletContextPath',
            'username': request.user.username
        })

    return HttpResponse("Method not allowed", status=405)


@login_required
def submit_report_success(request):
    if request.method == 'GET':
        temp_person = TempPerson.objects.last()  # Assuming TempPerson has an auto-generated ID field
        temp_person.person_uploaded_by = request.user.username
        temp_person.save()
        return redirect('/user')

    return HttpResponse("Method not allowed", status=405)


@login_required
def get_age_progression(request):
    username = request.user.username
    return render(request, 'reunite-age-progression.html',
                  {'username': username, 'path': '/servletContextPath'})


@login_required
def progress_age(request):
    if request.method == 'POST':
        person_image = request.FILES['image']
        target_age = int(request.POST['personAge'])

        person_filename = str(uuid.uuid4()) + ".jpg"

        try:
            url = get_testing(person_filename, target_age)
            return render(request, 'reunite-age-progression-success.html',
                          {'url1': person_filename, 'url2': url, 'username': request.user.username,
                           'path': '/servletContextPath'})
        except Exception as e:
            print(e)
            return render(request, 'reunite-age-progression-failure.html')

    return HttpResponse("Method not allowed", status=405)


def get_testing(input_string, input_integer):
    try:
        python_script_path = "/script.py"
        command = ["python", python_script_path, input_string, str(input_integer)]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        exit_code = process.returncode

        if exit_code != 0:
            print("Error executing Python script:")
            print(error.decode())  # Log error messages
            return "error1"

        return output.decode()
    except Exception as e:
        print(e)
        return "error2"


@login_required
def get_about(request):
    username = request.user.username
    return render(request, 'reunite-about.html', {'username': username, 'path': '/servletContextPath'})


@login_required
def get_contact(request):
    username = request.user.username
    return render(request, 'reunite-contact.html', {'username': username, 'path': '/servletContextPath'})

