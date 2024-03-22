from django.urls import path
from . import views

app_name = "githubTool"

urlpatterns = [
    path('try/', views.try_test, name="try_test"),
    path('create/', views.create_project, name="create_project"),
]