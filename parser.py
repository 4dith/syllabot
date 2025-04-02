import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'syllabot.settings'
django.setup()

from courses.models import *

FILE_PATH = "courses\static\courses\data.md"
course = unit = None
mode = ""
code=""
unitNum = topicNum = 1

# Delete existing records
Unit.objects.all().delete()
Reference.objects.all().delete()
Topic.objects.all().delete()
Experiment.objects.all().delete()

with open(FILE_PATH, encoding='utf8') as file:
    for line in file:
        if line[0:3] == '## ':
            code = line[3:].strip()
            unitNum = 1
            try:
                course = Course.objects.get(code=code)
            except:
                print(code, "", end='')
        
        elif (line[0:4] == "### "):
            if "text" in line.lower():
                print(code, "has text References")
                mode = "reference"
            elif "exp" in line.lower():
                print(code, "has experiments")
                mode = "experiment"        
        elif line.split() and line.split()[0].strip('.').isdigit():
            if mode == "reference":
                refNum = int(line.split()[0].strip('.'))
                refName = line[len(str(refNum)) + 2:].strip()
                reference = Reference(number=refNum, name=refName, course=course)
                reference.save()
            elif mode == "experiment":
                expNum = int(line.split()[0].strip('.'))
                expDesc = line[len(str(refNum)) + 2:].strip()
                experiment = Experiment(number=expNum, description=expDesc, course=course)
                experiment.save()
                # print(expNum, expDesc)
        elif line[:2] == "- ":
            if mode == "topic":
                topicName = line[2:].strip()
                # print(topicNum, topicName)
                topic = Topic(number=topicNum, name=topicName, unit=unit)
                topic.save()
                topicNum += 1
        elif len(line.strip()) > 0 and line[0].isalnum():
            unitName = line.strip().strip(':')
            # print(code, ": ", unitNum, ".", unitName)
            unit = Unit(number=unitNum, name=unitName, course=course)
            unit.save()
            unitNum += 1
            mode = "topic"
            topicNum = 1
    

