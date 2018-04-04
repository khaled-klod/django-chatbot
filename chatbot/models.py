from django.db import models


# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=50, primary_key=True)
    rating = models.IntegerField


class University(models.Model):
    university_abbreviation = models.CharField(max_length=20, primary_key=True)
    university_name = models.CharField(max_length=80)
    university_rating = models.IntegerField()




class Application(models.Model):
    id_application = models.AutoField(primary_key=True)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    datedeb = models.DateField()
    datefin = models.DateField()
    category = models.CharField(max_length=30)

class Skills(models.Model):
    skill_name = models.CharField(max_length=30)
    app_id = models.ForeignKey(Application, on_delete=models.CASCADE)


class Characteristics(models.Model):
    app_id = models.ForeignKey(Application, on_delete=models.CASCADE)
    required_language = models.CharField(max_length=30, blank=True, null=True)
    experience_years = models.IntegerField()



class Person(models.Model):
    id_person = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    Adress = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    experience_years = models.IntegerField(blank=True, null=True)
    confidence = models.IntegerField(blank=True, null=True)
    teamwork = models.IntegerField(blank=True, null=True)

    last_company = models.CharField(max_length=50, blank=True, null=True)
    past_university = models.CharField(max_length=50, blank=True, null=True)
    salary_expectation = models.CharField(max_length=50, blank=True, null=True)
    app_id = models.ForeignKey(Application, on_delete=models.CASCADE, blank=True, null=True)


class PersonSkills(models.Model):
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField()


class PersonLanguages(models.Model):
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField()


class FinalView(models.Model):
    id = models.ForeignKey(Person, primary_key=True, on_delete=models.CASCADE)
    desired_skills = models.IntegerField()
    other_skills = models.IntegerField()
    university = models.IntegerField()
    language = models.IntegerField()
    experience_years = models.IntegerField()
    company = models.IntegerField()
    confidence = models.IntegerField()
    teamwork = models.IntegerField()
    final_rating = models.IntegerField()
