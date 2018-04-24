from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .cvmodule.cvmodule import analyze_cv
import requests
import nltk
# from django.template import loader


from .models import Person

from .models import Skills

from .models import Application
from .models import PersonSkills
from .models import PersonLanguages
from .models import Characteristics
from .models import Company
from .models import University

from nltk.corpus import wordnet
from word2number import w2n


# def correspond():

def get_word_synonyms_from_sent(word, sent):
    word_synonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemma_names():
            if lemma in sent:
                word_synonyms.append(lemma)
    if len(word_synonyms) > 0:
        return True
    else:
        return False


# Global variables:

error = False
change = False
app = Application.objects.get(id_application=1)
person = Person(app_id=app)
intro_response = [""]
intro_question = []
age = 0
ageQ = "How old are you?"
experience_yearsQ = "How many working years experience do you have?"

skillsQ = "Rate, on a scale of 10, your skills in: "
languagesQ = "How would you rate your skills on a scale of 10 in "
teamworkQ = "Which one of the following attributes do you consider to be your most relevant strength?" + "\n" + "1)work independently" + "\n" + "2)work with one coworker" + "\n" + " 3)work with a team"
last_companyQ = "Please give us one major company that you've worked for"
confidenceQ = "Which one of the following attributes do you consider to be your most relevant strength? 1)confident, 2)creative, 3)smart "
past_universityQ = "Please give us the university from which you got your degree"
salary_expectationQ = "Thanks. What is your salary expectation in dollars?"

suite_question = [ageQ, experience_yearsQ, languagesQ, teamworkQ, last_companyQ, confidenceQ,
                  past_universityQ, salary_expectationQ]
suite_response = ["", "age", "experience_years", "languages", "teamwork", "last_company",
                  "confidence",
                  "past_university", "salary_expectation"]
#Collect all company names
companies = Company.objects.all()
company_names = []
for company in companies:
    company_names.append(company.company_name)


stored_company = False
#Collect all university names and abbreviations
universities = University.objects.all()

university_names = []
university_abbreviations = []

for university in universities:
    university_names.append(university.university_name)
    print(university.university_name)
    university_abbreviations.append(university.university_abbreviation)
    print(university.university_abbreviation)

stored_university = False


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
    global age
    global company_names
    global university_names
    global university_abbreviations
    global stored_university
    global stored_company

    if request.method == 'POST':

        reptext = request.POST['rep']
        i = int(request.POST['question_id'])

        if i == 0 and change == False:  # if we didn't change from intro to suite questions and it's the very first BotMessage
            r = requests.post('http://text-processing.com/api/sentiment/', data={'text': reptext})
            response = r.json()['label']

            if response == "pos" or response == "neutral":
                if (len(intro_question) > 0):  # Check if all info were collected
                    data = {
                        'resp': 'Great. Let\'s begin.' + '\n' + intro_question[0],
                        'question_id': i
                    }
                    return JsonResponse(data)
                else:  # if all info were collected, move to suite questions
                    change = True
                    data = {
                        'resp': 'Great ' + person.first_name + '. Let\'s begin.' + '\n' + suite_question[0],
                        'question_id': 0
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'resp': "Okay, let me know when you're ready",
                    'question_id': i - 1
                }
                return JsonResponse(data)



        else:

            if i < len(intro_question) and change == False:  # we are still in the intro questions

                setattr(person, intro_response[i], reptext)
                person.save()
                data = {
                    'resp': intro_question[i],
                    'question_id': i
                }
                return JsonResponse(data)
            elif not change:  # all intro questions were asked
                change = True
                setattr(person, intro_response[i], reptext)
                person.save()
                data = {
                    'resp': suite_question[0],  # ask age
                    'question_id': 0
                }
                return JsonResponse(data)
            else:
                # store age ask experience

                if i == 1:

                    if len([int(s) for s in reptext.split() if s.isdigit()]) > 0:
                        age = [int(s) for s in reptext.split() if s.isdigit()][0]
                    else:
                        try:
                            age = int(w2n.word_to_num(reptext))

                        except ValueError:
                            data = {
                                'resp': 'Please enter an age (number or words)' + '\n' + suite_question[i - 1],
                                'question_id': i - 1
                            }
                            return JsonResponse(data)

                    if age == 0:  # error
                        data = {
                            'resp': 'Please enter an age (number or words)' + '\n' + suite_question[i-1],
                            'question_id': i-1
                        }
                        return JsonResponse(data)
                    else:
                        setattr(person, suite_response[i], age)
                        person.save()
                        data = {
                            'resp': suite_question[i],
                            'question_id': i
                        }
                        return JsonResponse(data)
                # store experience ask skill JAVA

                elif i == 2:
                    if len([int(s) for s in reptext.split() if s.isdigit()]) > 0:
                        experience = [int(s) for s in reptext.split() if s.isdigit()][0]

                    else:
                        try:
                            experience = int(w2n.word_to_num(reptext))

                        except ValueError:
                            data = {
                                'resp': 'Please enter a number of years (number or words)' + '\n' + suite_question[i - 1],
                                'question_id': i - 1
                            }
                            return JsonResponse(data)

                    setattr(person, suite_response[i], experience)
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
                    all_skills = Skills.objects.filter(app_id=app)
                    skill_name_old = all_skills[0].skill_name
                    skill_name_new = all_skills[1].skill_name
                    try:
                        rating = int(reptext)

                    except ValueError:
                        try:
                            rating = int(w2n.word_to_num(reptext))
                        except ValueError:
                            data = {
                                'resp': 'Please enter a number between 1 and 10' + '\n' + suite_question[i - 1]+skill_name_old,
                                'question_id': i - 1
                            }
                            return JsonResponse(data)

                    if rating not in range(11):
                        # error = True

                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10." + "\n" +
                                    suite_question[i - 1] + skill_name_old,
                            'question_id': i - 1
                        }
                        return JsonResponse(data)
                    else:
                        #setattr(person, suite_response[i], reptext)
                        #person.save()

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name_old, rating=rating)

                        data = {
                            'resp': suite_question[i] + skill_name_new,
                            'question_id': i
                        }
                        return JsonResponse(data)

                # store skill C++ ask skill ANG
                elif i == 4:
                    all_skills = Skills.objects.filter(app_id=app)
                    skill_name_old = all_skills[1].skill_name
                    skill_name_new = all_skills[2].skill_name
                    try:
                        rating = int(reptext)
                    except ValueError:
                        try:
                            rating = int(w2n.word_to_num(reptext))
                        except ValueError:
                            data = {
                                'resp': 'Please enter a number between 1 and 10' + '\n' + suite_question[
                                    i - 1] + skill_name_old,

                                'question_id': i - 1
                            }
                            return JsonResponse(data)

                    if rating not in range(11):
                        # error = True

                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10." + "\n" +
                                    suite_question[i - 1] + skill_name_old,
                            'question_id': i - 1
                        }
                        return JsonResponse(data)
                    else:
                        # setattr(person, suite_response[i], reptext)
                        # person.save()

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name_old,
                                                               rating=rating)

                        data = {
                            'resp': suite_question[i] + skill_name_new,
                            'question_id': i
                        }
                        return JsonResponse(data)
                # store skill ANG ask skill NODE
                elif i == 5:
                    all_skills = Skills.objects.filter(app_id=app)
                    skill_name_old = all_skills[2].skill_name
                    skill_name_new = all_skills[3].skill_name
                    try:
                        rating = int(reptext)


                    except ValueError:

                        try:

                            rating = int(w2n.word_to_num(reptext))

                        except ValueError:

                            data = {

                                'resp': 'Please enter a number between 1 and 10' + '\n' + suite_question[
                                    i - 1] + skill_name_old,

                                'question_id': i - 1

                            }

                            return JsonResponse(data)

                    if rating not in range(11):
                        # error = True

                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10." + "\n" +
                                    suite_question[i - 1] + skill_name_old,
                            'question_id': i - 1
                        }
                        return JsonResponse(data)
                    else:
                        # setattr(person, suite_response[i], reptext)
                        # person.save()

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name_old,
                                                               rating=rating)

                        data = {
                            'resp': suite_question[i] + skill_name_new,
                            'question_id': i
                        }
                        return JsonResponse(data)

                ## store skill NODE ask languages question
                elif i == 6:
                    all_skills = Skills.objects.filter(app_id=app)
                    skill_name_old = all_skills[3].skill_name
                    rl = Characteristics.objects.get(app_id=app)
                    req_lang = rl.required_language
                    try:
                        rating = int(reptext)


                    except ValueError:

                        try:

                            rating = int(w2n.word_to_num(reptext))

                        except ValueError:

                            data = {

                                'resp': 'Please enter a number between 1 and 10' + '\n' + suite_question[
                                    i - 1] + skill_name_old,

                                'question_id': i - 1

                            }

                            return JsonResponse(data)

                    if rating not in range(11):
                        # error = True

                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10." + "\n" +
                                    suite_question[i - 1] + skill_name_old,
                            'question_id': i - 1
                        }
                        return JsonResponse(data)
                    else:
                        # setattr(person, suite_response[i], reptext)
                        # person.save()

                        p_skills = PersonSkills.objects.create(id_person=person, skill_name=skill_name_old,
                                                               rating=rating)

                        data = {
                            'resp': suite_question[i] + req_lang,
                            'question_id': i
                        }
                        return JsonResponse(data)

                # ask teamworkQ store language
                elif i == 7:
                    rl = Characteristics.objects.get(app_id=app)
                    req_lang = rl.required_language
                    try:
                        rating = int(reptext)
                    except ValueError:
                        try:
                            rating = int(w2n.word_to_num(reptext))
                        except ValueError:
                            data = {
                                'resp': 'Please enter a number between 1 and 10' + '\n' + suite_question[i - 1] + req_lang,
                                'question_id': i - 1
                            }
                            return JsonResponse(data)

                    if rating not in range(11):
                        # error = True

                        data = {
                            'resp': "The rating must be a POSITIVE Integer less or equal than 10." + "\n" +
                                    suite_question[i - 1] + req_lang,
                            'question_id': i - 1
                        }
                        return JsonResponse(data)

                    else:  # store language ask teamworkQ
                        p_language = PersonLanguages.objects.create(id_person=person, language=req_lang, rating=rating)
                        data = {
                            'resp': suite_question[i],
                            'question_id': i
                        }
                        return JsonResponse(data)

                # store teamworkQ ask lastcomp
                elif i == 8:
                    if ("3"in reptext) or ("team"in reptext) or ("group"in reptext) or ("three" in reptext) or get_word_synonyms_from_sent('group',reptext) or get_word_synonyms_from_sent('team', reptext):
                        print(get_word_synonyms_from_sent('group',reptext))
                        print(get_word_synonyms_from_sent('team', reptext))
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
                    words = nltk.word_tokenize(reptext)


                    for word in words:
                        if word.upper() in company_names:

                            stored_company = True
                            break

                    if not stored_company:
                        setattr(person, suite_response[i], "None")
                        person.save()
                        data = {
                            'resp': "No Company Given. "+suite_question[i],
                            'question_id': i

                        }
                        return JsonResponse(data)
                    else:
                        setattr(person, suite_response[i], word.upper())
                        person.save()
                        data = {
                            'resp': suite_question[i],
                            'question_id': i

                        }
                        return JsonResponse(data)
                # store confidence ask past universities

                elif i == 10:

                    if get_word_synonyms_from_sent('confident',reptext) or ("1"in reptext) or ("confidence"in reptext) or ("one" in reptext):
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
                    words = nltk.word_tokenize(reptext)

                    for word in words:
                        if (word.upper() in university_names) or (word.upper() in university_abbreviations):
                            stored_university = True
                            setattr(person, suite_response[i], word.upper())
                            person.save()
                            break

                    for university_name in university_names:
                        if (university_name in reptext.upper()) or stored_company:
                            stored_university = True
                            setattr(person, suite_response[i], university_name)
                            person.save()
                            break
                    for university_abbreviation in university_abbreviations:
                        if (university_abbreviation in reptext.upper()) or stored_company:
                            stored_university = True
                            setattr(person, suite_response[i], university_abbreviation)
                            person.save()
                            break
                    if not stored_university:
                        setattr(person, suite_response[i], "None")
                        person.save()
                        data = {
                            'resp': "No University Given" + suite_question[i],
                            'question_id': i

                        }
                        return JsonResponse(data)
                    else:
                        data = {
                            'resp': suite_question[i],
                            'question_id': i

                        }
                        return JsonResponse(data)
                # store salary
                elif i == 12:
                    if len([int(s) for s in reptext.split() if s.isdigit()]) > 0:
                        salary = [int(s) for s in reptext.split() if s.isdigit()][0]

                    else:
                        try:
                            salary = int(w2n.word_to_num(reptext))

                        except ValueError:
                            data = {
                                'resp': 'Please enter a number' + '\n' + suite_question[i - 1],
                                'question_id': i - 1
                            }
                            return JsonResponse(data)
                    setattr(person, suite_response[i], salary)
                    person.save()
                    if person.sex=='male':
                        data = {
                            'resp': "Thank you Mr."+ person.last_name,
                            'question_id': i
                        }
                    else:
                        data = {
                            'resp': "Thank you Mrs." + person.last_name,
                            'question_id': i
                        }
                    return JsonResponse(data)
                elif i == 13:
                    data = {
                        'resp': '',
                        'question_id': i
                    }
                    return JsonResponse(data)



