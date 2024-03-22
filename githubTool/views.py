from django.shortcuts import render,redirect, HttpResponseRedirect
from django.urls import reverse
from .forms import ProjectForm
from .models import Project

import requests
import shutil
import subprocess

# Create your views here.

def home(request):
    form = ProjectForm()
    return render(request, 'index.html', {'form': form})

def try_test(request):
    template_name = "tryTest.html"
    return render(request, template_name)


def create_project(request):
    if request.method == "POST":
        repo_name = request.POST.get("repo_name")
        is_private = request.POST.get("is_private") == "True"
        description = request.POST.get("description")
        access_token = request.POST.get("access_token")

        repo = Project(name=repo_name, description=description, is_public=not is_private, access_token=access_token)
        repo.save()
        
        # Call the function to create GitHub repository and handle the response
        print(create_github_repo(repo_name, is_private, description, access_token))
        print("Repository Name: ", repo_name)
        print("Is Private: ", is_private)
        print("Description: ", description)
        print("Access Token: ", access_token)
        print("Creating repository...")
        
        # Redirect to project_created view
        return HttpResponseRedirect(reverse('home') + '?visible=visible')
    else:
        redirect('home')

def create_github_repo(repo_name, is_private, description, access_token):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": repo_name,
        "private": is_private,
        "description": description
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Repository created successfully!")
        return response.json()["clone_url"]
    else:
        print("Failed to create repository. Status code:", response.status_code)
        return None