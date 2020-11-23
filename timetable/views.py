from django.shortcuts import render,redirect
from timetable.forms import RoomsForm
from timetable.models import Rooms
import timetable.forms as ttf
import timetable.models as ttm


# Create your views here.
def room(request):
    if request.method == "POST":
        form=RoomsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form=RoomsForm()
    return render(request,'insert_rooms.html',{'form':form})
def view(request):
    rooms=Rooms.objects.all()
    ins=ttm.Instructor.objects.all()
    meets=ttm.MeetTime.objects.all()
    courses=ttm.Course.objects.all()
    dept=ttm.Dept.objects.all()

    return render(request,"view.html",{'rooms':rooms,'ins':ins,'meets':meets,'course':courses,'dept':dept})
def instructor(request):
    if request.method == "POST":
        form=ttf.InsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form=ttf.InsForm()
    return render(request,'insert_instructor.html',{'form':form})
def time(request):
    if request.method == "POST":
        form=ttf.MeetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form=ttf.MeetForm()
    return render(request,'insert_time.html',{'form':form})
def dept(request):
    if request.method == "POST":
        form=ttf.DeptForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form=ttf.DeptForm()
    return render(request,'insert_dept.html',{'form':form})
def course(request):
    if request.method == "POST":
        form=ttf.CourseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        form=ttf.CourseForm()
    return render(request,'insert_course.html',{'form':form})
def update_dept(request,id):
    dept=ttm.Dept.objects.get(id=id)
    form=ttf.DeptForm(instance=dept)
    if request.method=='POST':
        form=ttf.DeptForm(request.POST,instance=dept)
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass

    return render(request,'update_dept.html',{'form':form})
def delete_dept(request,id):
    dept=ttm.Dept.objects.get(id=id)
    dept.delete()
    return redirect('/view')
def index(request):
    return redirect('/view')