from django.db import models

# Create your models here.

class Course(models.Model):
    CREDIT_CHOICES = [(i, str(i)) for i in range(1, 5)]
    YEAR_CHOICES = [(i, str(i)) for i in range(1, 5)]
    SEMESTER_CHOICES = [(i, str(i)) for i in range(1, 3)]
    
    code = models.CharField(max_length=6, unique=True, null=False)
    name = models.CharField(max_length=128, null=False)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="dependent_courses")
    credits = models.PositiveSmallIntegerField(choices=CREDIT_CHOICES, default=3, null=False)
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=1, null=False)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.code
    
class Reference(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="references")

    def __str__(self):
        return f"({self.course}) {self.name}"

class Unit(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')

    def __str__(self):
        return f"({self.course}) {self.name}"

class Topic(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=256)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return f"({self.unit.course}) - {self.name}"

class Experiment(models.Model):
    number = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=512)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="experiments")

    def __str__(self):
        return f"({self.course}) - {self.description}"

