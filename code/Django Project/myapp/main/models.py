from django.db import models


class MissingPerson(models.Model):
    image = models.ImageField(upload_to='missing_people/')
    sex = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.name


class TempPerson(models.Model):
    personName = models.CharField(max_length=100)
    personAge = models.IntegerField()
    personGender = models.CharField(max_length=10)
    photoYear = models.IntegerField()
    personAadhar = models.CharField(max_length=20)
    personImage = models.ImageField(upload_to='temp_person_images')

    def __str__(self):
        return self.personName


class ReUniteDAO:
    @staticmethod
    def add_person(personName, personAge, personGender, photoYear, personAadhar, personImage):
        temp_person = TempPerson.objects.create(
            personName=personName,
            personAge=personAge,
            personGender=personGender,
            photoYear=photoYear,
            personAadhar=personAadhar,
            personImage=personImage
        )
        return temp_person

    @staticmethod
    def fetch_all_person():
        return TempPerson.objects.all()


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    uid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class StaffDAOImpl:
    @staticmethod
    def find_user(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def add_user(staffDTO):
        user = User.objects.create(
            username=staffDTO.username.strip(),
            email=staffDTO.email,
            phone=staffDTO.phoneNumber,
            uid=staffDTO.username.strip(),
            password=staffDTO.password
        )
        return user