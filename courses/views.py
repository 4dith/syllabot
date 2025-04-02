from django.shortcuts import render
from django.http import JsonResponse
from .models import Course
from .rag import answer_question

# Create your views here.

def index(request):
    return render(request, 'courses/index.html')

def syllabus(request, year, code=None):
    if not code:
        return render(request, "courses/syllabus.html", {
            "year": year,
            "courses": Course.objects.filter(year=year),
            "message": "Select a course to view its details"
        })
    
    course = Course.objects.get(code=code)

    return render(request, "courses/syllabus.html", {
        "year": year,
        "courses": Course.objects.filter(year=year),
        "course": course,
        "units": course.units.all(),
    })

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = answer_question(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, "courses/chat.html")
