from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .cvmodule.cvmodule import analyze_cv

#from django.template import loader



from .models import Person

from .models import Skills

from .models import Application
from .models import PersonSkills
from .models import PersonLanguages
from .models import Characteristics

# Global variables:

error = False
change = False
app = Application.objects.get(id_application=1)
person = Person(app_id=app)
intro_response = [""]
intro_question = []

ageQ = "How old are you?"
experience_yearsQ = "How many working years experience do you have [ If you don't have any, TYPE 0]"

skillsQ = "Rate, on a scale of 10, your skills in: "
languagesQ = "How would you rate your skills on a scale of 10 in "
teamworkQ = "Which one of the following attributes do you consider to be your most relevant strength? 1)work independently, 2)work with one coworker, 3)work with a team"
last_companyQ = "Give us one major company that you worked for"
confidenceQ = "Which one of the following attributes do you consider to be your most relevant strength? 1)confident, 2)creative, 3)smart "
past_universityQ = "From what university did you get your degree"
salary_expectationQ = "Thanks Kaled. Could you provide the salary range that would match your expectations?"

suite_question = [ageQ, experience_yearsQ, languagesQ, teamworkQ, last_companyQ, confidenceQ,
                  past_universityQ, salary_expectationQ]
suite_response = ["", "age", "experience_years", "languages", "teamwork", "last_company",
                  "confidence",
                  "past_university", "salary_expectation"]


def index(request):
    context = {}
    return render(request, 'chatbot/index.html', context)


def cvmodule(request):
    global suite_question
    global suite_response
    global skillsQ

    all_skills = Skills.objects.all()
    for skill in all_skills:
        suite_question.insert(2, skillsQ)
        suite_response.insert(3, "skill_name")

    if request.method == 'POST':
        global person
        first_nameQ = "Good, let's get started. May I have your FIRST name please?"
        last_nameQ = "Good, . May I have your LAST name please?"
        sexQ = "What's your gender?"
        AdressQ = "What's your address"
        phone_numberQ = "What's your phone number?"
        dateOfBirthQ = "What's your date of birth"
        emailQ = "Please type your email address"
        ageQ = "How old are you?"

        name, last_name, sex, address, telephone, date_of_birth, email = analyze_cv()
        if not name:
            intro_question.append(first_nameQ)
            intro_response.append("first_name")
        else:
            person.first_name = name
        if not last_name:
            intro_question.append(last_nameQ)
            intro_response.append("last_name")
        else:
            person.last_name = last_name
        if not sex:
            intro_question.append(sexQ)
            intro_response.append("sex")
        else:
            person.sex = sex
        if not address:
            intro_question.append(AdressQ)
            intro_response.append("Adress")
        else:
            person.Adress = address
        if not telephone:
            intro_question.append(phone_numberQ)
            intro_response.append("phone_number")
        else:
            person.phone_number = telephone
        if not date_of_birth:
            intro_question.append(dateOfBirthQ)
            intro_response.append("dateOfBirth")
        else:
            person.dateOfBirth = date_of_birth
        if not email:
            intro_question.append(emailQ)
            intro_response.append("email")
        else:
            person.email = email

        person.save()
    return HttpResponse('')


def genresp(request):
    global person
    global intro_question
    global intro_response
    global suite_question
    global suite_response
    global change
    global app
    global error

    if request.method == 'POST':
        reptext = request.POST['rep']
        i = int(request.POST['question_id'])

        if i == 0 and change == False: #if we didn't change from intro to suite questions and it's the very first BotMessage
            if reptext == "READY":
                if(len(intro_question)>0): #Check if all info were collected
                    data = {
                        'resp': intro_question[0],
                        'question_id': i
                    }
                    return JsonResponse(data)
                else: #if all info were collected, move to suite questions
                    change = True
                    data = {
                        'resp': suite_question[0],
                        'question_id': 0
                    }
                    return JsonResponse(data)


        else:

            if i < len(intro_question) and change == False: #we are still in the intro questions

                setattr(person, intro_response[i], reptext)
                person.save()
                data = {
                    'resp': intro_question[i],
                    'question_id': i
                }
                return JsonResponse(data)
            elif not change: # all intro questions were asked
                change = True
                setattr(person, intro_response[i], reptext)
                person.save()
                data = {
                    'resp': suite_question[0], #ask age
                    'question_id': 0
                }
                return JsonResponse(data)
            else:
                #store age ask experience
                if i == 1:
                    setattr(person, suite_response[i], reptext)
                    person.save()
                    data = {
                        'resp': suite_question[i],
                        'question_id': i
                    }
                    return JsonResponse(data)
                # store experience ask skill JAVA

                elif i == 2:
                    setattr(person, suite_response[i], reptext)
                    person.save()
                    all_skills = Skills.objects.filter(app_id=app)
                    skill_name = all_skills[0].skill_name


                    data = {
                        'resp': suite_question[i] + skill_name,
                        'question_id': i
                    }
                    return JsonResponse(data)



                # store skill JAVA ask skill C++
                elif i == 3:
                    if int(reptext) not in range(11):
                        # error = True
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name = all_skills[0].skill_name
                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10."+"/n" + suite_question[i-1] + skill_name,
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:
                        setattr(person, suite_response[i], reptext)
                        person.save()
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name1 = all_skills[0].skill_name

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name1, rating=reptext)

                        skill_name = all_skills[1].skill_name

                        data = {
                            'resp': suite_question[i] + skill_name,
                            'question_id': i
                        }
                        return JsonResponse(data)

                # store skill C++ ask skill ANG
                elif i == 4:
                    if int(reptext) not in range(11):
                        # error = True
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name = all_skills[1].skill_name
                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10."+"/n" + suite_question[i-1] + skill_name,
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:

                        setattr(person, suite_response[i], reptext)
                        person.save()
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name1 = all_skills[1].skill_name

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name1, rating=reptext)

                        skill_name = all_skills[2].skill_name

                        data = {
                            'resp': suite_question[i] + skill_name,
                            'question_id': i
                        }
                        return JsonResponse(data)
                # store skill ANG ask skill NODE
                elif i == 5:
                    if int(reptext) not in range(11):
                        # error = True
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name = all_skills[2].skill_name
                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10."+"/n" + suite_question[i-1] + skill_name,
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:
                        setattr(person, suite_response[i], reptext)
                        person.save()
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name1 = all_skills[2].skill_name

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name1, rating=reptext)

                        skill_name = all_skills[3].skill_name

                        data = {
                            'resp': suite_question[i] + skill_name,
                            'question_id': i
                        }
                        return JsonResponse(data)

                ## store skill NODE ask languages question
                elif i == 6:
                    if int(reptext) not in range(11):
                        # error = True
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name = all_skills[3].skill_name
                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10."+"/n" + suite_question[i-1] + skill_name,
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:

                        setattr(person, suite_response[i], reptext)
                        person.save()
                        all_skills = Skills.objects.filter(app_id=app)
                        skill_name1 = all_skills[3].skill_name

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name1, rating=reptext)

                        rl = Characteristics.objects.get(app_id=app)
                        req_lang = rl.required_language

                        data = {
                            'resp': suite_question[i] + req_lang,
                            'question_id': i
                        }
                        return JsonResponse(data)

                # ask teamworkQ store language
                elif i == 7:
                    if int(reptext) not in range(11):
                        # error = True
                        rl = Characteristics.objects.get(app_id=app)
                        req_lang = rl.required_language
                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10."+"/n" + suite_question[i-1] + req_lang,
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:

                        req_lang = Characteristics.objects.get(app_id=app).required_language
                        p_language = PersonLanguages.objects.create(id_person=person, language=req_lang, rating=reptext)

                        data = {
                            'resp': suite_question[i],
                            'question_id': i
                        }
                        return JsonResponse(data)
                # store teamworkQ ask lastcomp
                elif i == 8:
                    if reptext == "3":
                        setattr(person, suite_response[i], 1)
                        person.save()
                    else:
                        setattr(person, suite_response[i], 0)
                        person.save()
                    data = {
                        'resp': suite_question[i],
                        'question_id': i
                    }
                    return JsonResponse(data)

                # store lastcomp ask confidence
                elif i == 9:
                    setattr(person, suite_response[i], reptext)
                    person.save()
                    data = {
                        'resp': suite_question[i],
                        'question_id': i
                    }
                    return JsonResponse(data)


                # store confidence ask past universities

                elif i == 10:
                    if reptext == "1":
                        setattr(person, suite_response[i], 1)
                        person.save()
                    else:
                        setattr(person, suite_response[i], 0)
                        person.save()

                    data = {
                        'resp': suite_question[i],
                        'question_id': i
                    }
                    return JsonResponse(data)

                # store past uni ask salary

                elif i == 11:
                    setattr(person, suite_response[i], reptext)
                    person.save()
                    data = {
                        'resp': suite_question[i],
                        'question_id': i
                    }
                    return JsonResponse(data)

                # store salary
                elif i == 12:
                    setattr(person, suite_response[i], reptext)
                    person.save()
                    data = {
                        'resp': "Thank you",
                        'question_id': i
                    }
                    return JsonResponse(data)

        # call your function here and pass reptext
        # call your function to get the response from the chatbot
        # get your response and put in data
