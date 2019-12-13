"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from venue.views import EventView, EventTeamView, VueEventView
from protocol.views import AttendanceView
from .routers import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('календарь/', EventView.as_view(), name='event_view'),
    path('cal/', VueEventView.as_view(), name='vue_event_view'),
    path('календарь/<str:id>/', EventTeamView.as_view(), name='event_view'),
    path('состав/', AttendanceView.as_view(), name='new_attendance'),
    path('состав/<str:id>/<str:id>/', AttendanceView.as_view(), name='new_attendance'),
    path('api/', include(router.urls)),
]
