from django.shortcuts import render, redirect
from trained_model import PretrainedFacialRecognitionModel


class ReUniteController:
    def __init__(self):
        self.tempPerson = None
        self.reUniteDAO = None
        self.staffDAOImpl = None
        self.staffValidation = None
        self.servletContextPath = None
        self.pretrained_model = PretrainedFacialRecognitionModel('face_recognition.dat')

    def get_registration(self, request):
        return render(request, 'reunite-registration.html')

    def submit_registration(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            phoneNumber = request.POST.get('phoneNumber')
            userId = request.POST.get('userId')
            password = request.POST.get('password')
            return redirect('/registration')

    def get_home_page(self, request):
        if request.user.is_authenticated:
            return redirect('/user')
        return redirect('/login')

    def get_user_page(self, request):
        if request.user.is_authenticated:
            return render(request, 'reunite-home.html', {'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def get_service(self, request):
        if request.user.is_authenticated:
            return render(request, 'reunite-services.html', {'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def get_found_page(self, request):
        if request.user.is_authenticated:
            return render(request, 'reunite-found.html', {'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def submit_found(self, request):
        if request.method == 'POST':
            personImage = request.FILES['myimage']
            confidence = self.pretrained_model.predict(personImage.read(), personImage.read())
            return render(request, 'reunite-found-result.html', {'personName': personImage.getPersonName(), 'personAge': personImage.getPersonAge(), 'personGender': personImage.getPersonGender(), 'personImage': personImage.getPersonImage(), 'personAadhar': personImage.getPersonAadhar(), 'confidence': confidence, 'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def get_report(self, request):
        if request.user.is_authenticated:
            return render(request, 'reunite-report.html', {'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def submit_report(self, request, imageBase64=None):
        if request.method == 'POST':
            personAadhar = request.POST.get('personAadhar')
            personName = request.POST.get('personName')
            personAge = int(request.POST.get('personAge'))
            personGender = request.POST.get('personGender')
            photoYear = int(request.POST.get('photoYear'))
            personImage = request.FILES['myimage']
            # Handle image processing and adding person to database
            return render(request, 'reunite-report-result.html', {'personName': personName, 'personAge': personAge, 'personGender': personGender, 'photoYear': photoYear, 'personAadhar': personAadhar, 'imageBase64': imageBase64, 'username': request.user.username, 'path': self.servletContextPath})
        return redirect('/login')

    def submit_report_success(self, request):
        if request.user.is_authenticated:
            self.reUniteDAO.add_person(self.tempPerson.getPersonName(), self.tempPerson.getPersonAge(), self.tempPerson.getPersonGender(), self.tempPerson.getPhotoYear(), self.tempPerson.getPersonAadhar(), self.tempPerson.getPersonImage())
            return redirect('/user')
        return redirect('/login')
