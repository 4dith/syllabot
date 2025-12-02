import os
import django
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'syllabot.settings'
django.setup()

from courses.models import *

courses = Course.objects.all()
year1 = {}
year2 = {}
year3 = {}
year4 = {}

for course in courses:
    info = {
        "code": course.code,
        "name": course.name,
        "prerequisites": [p.code for p in course.prerequisites.all()],
        "credits": course.credits,
        "year": course.year,
        "semester": course.semester,
        "references": [r.name for r in course.references.all()],
        "experiments": [e.description for e in course.experiments.all()]
    }

    units = {}
    for unit in course.units.all():
        units[unit.name] = [t.name for t in unit.topics.all()]
    info["units"] = units  

    if int(course.year) == 1:
        year1[course.code] = course.name
    elif int(course.year) == 2:
        year2[course.code] = course.name
    elif int(course.year) == 3:
        year3[course.code] = course.name
    elif int(course.year) == 4:
        year4[course.code] = course.name


    # with open(f"jsons\\Y{course.year}\\{course.code}.json", "w") as f:
    #     json.dump(info, f, indent=4)

with open("jsons\\Y1.json", "w") as f:
    json.dump(year1, f, indent=4)

with open("jsons\\Y2.json", "w") as f:
    json.dump(year2, f, indent=4)

with open("jsons\\Y3.json", "w") as f:
    json.dump(year3, f, indent=4)

with open("jsons\\Y4.json", "w") as f:
    json.dump(year4, f, indent=4)