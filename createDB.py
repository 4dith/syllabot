from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os, shutil
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'syllabot.settings'
django.setup()

from courses.models import *
CHROMA_PATH = "chroma"

def createIndexDocument():
    f = open("index.txt")
    text = f.read()
    f.close()
    return text

def createDocument(course : Course):
    s = f"{course.name} (Code {course.code})\n"
    if course.semester:
        s += f"Year {course.year}, Semester {course.year * 2 - 2 + course.semester}\n"
    else:
        s += f"Year {course.year}, Semester 1 or 2\n"
    
    s += f"Credits: {course.credits}\n"
    
    if len(course.prerequisites.all()) == 0:
        s += "This course has no prerequisites.\n"
    else:
        s += f"\nPrerequisites: \n"
        for i, prereq in enumerate(course.prerequisites.all(), start=1):
            s += f"{i}. {prereq.name} ({prereq.code})\n"
    
    if len(course.units.all()) > 0:
        s += "\nUnits:\n"

        for unit in course.units.all():
            s += f"Unit {unit.number}: {unit.name}\n"
            for topic in unit.topics.all():
                s += f"- {topic.name}\n"
    
    if len(course.experiments.all()) > 0:
        s += "\nExperiments:\n"

        for exp in course.experiments.all():
            s += f"{exp.number}. {exp.description}\n"

    
    if len(course.references.all()) > 0:
        s += "\nReference Texts: \n"
        for reference in course.references.all():
            s += f"{reference.number}. {reference.name}\n"
    
    return s

def main():
    generate_data_store()

def generate_data_store():
    documents = createDocuments()
    print("Created documents from database.")
    save_to_chroma(documents)

def createDocuments():
    documents = []
    documents.append(createIndexDocument())
    for course in Course.objects.all():
        documents.append(createDocument(course))
    return documents

def save_to_chroma(documents):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    db = Chroma.from_texts(documents, OllamaEmbeddings(model="nomic-embed-text"), persist_directory=CHROMA_PATH)
    
    print(f"Saved {len(documents)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()