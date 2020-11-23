from django import forms
from timetable.models import Rooms
import timetable.models as ttm

class RoomsForm(forms.ModelForm):
    class Meta:
        model=Rooms
        fields="__all__"
class InsForm(forms.ModelForm):
    class Meta:
        model=ttm.Instructor
        fields="__all__"
class MeetForm(forms.ModelForm):
    class Meta:
        model=ttm.MeetTime
        fields="__all__"
class DeptForm(forms.ModelForm):
    class Meta:
        model=ttm.Dept
        fields="__all__"
class CourseForm(forms.ModelForm):
     class Meta:
        model=ttm.Course
        fields="__all__"
class EntyForm(forms.ModelForm):
    class Meta:
        model=ttm.Enty
        fields="__all__"