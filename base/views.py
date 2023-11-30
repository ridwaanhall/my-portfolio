from django.shortcuts import render
import requests, os

# Create your views here.
abouts = [
    {
        'id': 1,
        'name': 'Ridwan Halim',
        'title': 'Python Developer',
        'description': 'I am a developer who loves to solve problems and create beautiful and functional applications. I am a student at University of Technology Yogyakarta and I am currently learning Python.'
    }
]

def github_activity(request):
    github_username = 'ridwaanhall'

    github_token = os.getenv('GITHUB_TOKEN')

    api_url = f'https://api.github.com/users/{github_username}/events'

    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return render(request, 'base/github-activity.html', {'github_data': data})

def home(request):
    context = {'abouts': abouts}
    return render(request, 'base/home.html', context)

def dashboard(request):
    # about = None
    # for i in abouts:
    #     if i['id'] == int(pk):
    #         about = i
    # context = {'about': about}
    return render(request, 'base/dashboard.html')