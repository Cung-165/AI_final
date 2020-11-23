from django.db import models

# Create your models here.

class Rooms(models.Model):
    number=models.CharField(max_length=10)
    seatingCapacity=models.IntegerField()
    def __str__(self):
        return self.number

    
class Instructor(models.Model):
    name=models.CharField(max_length=70)


    def __str__(self):
        return self.name
class Course(models.Model):
    name_C=models.CharField(max_length=1000)
    maxStd=models.IntegerField()
    ins=models.ManyToManyField(Instructor)
    def __str__(self):
        return self.name_C
class Dept(models.Model):
    name_D=models.CharField(max_length=1000)
    course=models.ManyToManyField(Course)
    def __str__(self):
        return self.name_D
class MeetTime(models.Model):
    time=models.CharField(max_length=1000)
    def __str__(self):
        return self.time
class Enty(models.Model):
    name_C=models.CharField(max_length=1000)
    name_I=models.CharField(max_length=70)
    Romm_number=models.CharField(max_length=10)
    Thu=models.CharField(max_length=10)
    Ca=models.CharField(max_length=10)

class Meta:
    db_table="AI_f"