from django.contrib import admin
from .models import Course, Reference, Unit, Topic, Experiment

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name'] 
    filter_horizontal = ('prerequisites',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name']  

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['name'] 

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name'] 

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['description'] 