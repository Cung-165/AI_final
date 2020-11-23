"""AI_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from timetable import views
from timetable import handle
urlpatterns = [
    path('admin/', admin.site.urls),
    path('insert_rooms/',views.room),
    path('view/',views.view),
    path('test/',handle.test),
    path('insert_instructor/',views.instructor),
    path('insert_time/',views.time),
    path('insert_dept/',views.dept),
    path('insert_course/',views.course ),
    path('update_dept/<int:id>',views.update_dept ),
    path('delete_dept/<int:id>',views.delete_dept ),
    path('',views.index)
  
]

