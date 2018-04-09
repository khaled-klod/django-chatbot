# import PyPDF2
# pdfFileObj = open('/home/medsteph/Downloads/Example One Page CV.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# for num in range(0,20):
#  pageObj = pdfReader.getPage(num)
#  print(pageObj.extractText())

import os
import re
from tkinter import filedialog
from tkinter import *
from xml.dom import minidom
from datetime import datetime

def analyze_cv ():
    root = Tk()
    root.fileName = filedialog.askopenfilename()
    f_url = root.fileName
    cmd = 'pdftohtml -xml ' + f_url
    os.system(cmd)
    name = ''
    last_name = ''
    date_of_birth = ''
    sex = ''
    email = ''
    telephone = ''
    address = ''
    languages = list()
    skills = list()
    xmldoc = minidom.parse(f_url.replace('pdf', 'xml'))
    itemlist = xmldoc.getElementsByTagName('text')

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild
        my_path = os.path.abspath(os.path.dirname(__file__))
        path= my_path+"/names_final.txt"
        myfile = open(path, "r")
        st = str(s.nodeValue)
        st = st.lower()
        test = 0
        for line in myfile:
            ch = line.lower()
            ch = ch.strip()
            if st.find(ch) != -1 and st.find(ch) == 0 and len(ch) > 2 and ch != "work":
                name = st.split()[0]
                last_name = st.split()[1]
                print(st)
                test = 1

        if (test):
            break

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild

        st = str(s.nodeValue)
        dob = re.search(
            r'\d\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}',
            st)
        if dob:
            print(dob.group(0))
            date_of_birth1 = dob.group(0)
            date_of_birth = datetime.strptime(date_of_birth1, "%d %B %Y").strftime('%Y-%m-%d')
            break
        dob = re.search(r'\d\d\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}', st)
        if dob:
            print(dob.group(0))
            date_of_birth1 = dob.group(0)
            date_of_birth = datetime.strptime(date_of_birth1, "%d %b %Y").strftime('%Y-%m-%d')
            break
        dob = re.search(r'\d\d-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}', st)
        if dob:
            print(dob.group(0))
            date_of_birth1 = dob.group(0)
            date_of_birth = datetime.strptime(date_of_birth1, "%d-%b-%Y").strftime('%Y-%m-%d')
            break
        dob = re.search(
            r'\d\d-(?:January|February|March|April|May|June|July|August|September|October|November|December)-\d{4}',
            st)
        if dob:
            print(dob.group(0))
            date_of_birth1 = dob.group(0)
            date_of_birth = datetime.strptime(date_of_birth1, "%d-%B-%Y").strftime('%Y-%m-%d')

            break

        dob = re.search(r'(\d+ / \d+ / \d+)', st)
        if dob:
            print(dob.group(0))
            date_of_birth1 = dob.group(0)
            date_of_birth = datetime.strptime(date_of_birth1, "%d/%m/%Y").strftime('%Y-%m-%d')
            break

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild

        st = str(s.nodeValue)
        sexe = re.search(r'.*[M-m]ale.*', st)
        if sexe:
            print(sexe.group(0))
            sex = sexe.group(0)
            break
        sexe = re.search(r'.*[F-f]emale.*', st)
        if sexe:
            print(sexe.group(0))
            sex = sexe.group(0)
            break

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild
        st = str(s.nodeValue)
        mail = re.search(r'.*@.*', st)
        if mail:
            print(mail.group(0))
            email = mail.group(0)
            break

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild
        st = str(s.nodeValue)
        tel = re.search(r'\d{7,14}', st)
        if tel:
            print(tel.group(0))
            telephone = tel.group(0)
            break

    for s in itemlist:
        s = s.firstChild
        while True:
            if (s.firstChild == None):
                break
            else:
                s = s.firstChild
        st = str(s.nodeValue)
        adr = re.search(r'^[A-Z,a-z]*\s*\d{1,3}.*', st)
        if adr:
            print(adr.group(0))
            address = adr.group(0)
            break


    return name,last_name,sex,address,telephone,date_of_birth,email
