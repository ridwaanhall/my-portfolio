from django.shortcuts import render
from django.http import JsonResponse
import requests, os, json
from .models import Sidebar, Home
from datetime import datetime, timedelta


# Create your views here.
abouts = [
    {
        'id': 1,
        'name': 'Ridwan Halim',
        'title': 'Python Developer',
        'description': 'I am a developer who loves to solve problems and create beautiful and functional applications. I am a student at University of Technology Yogyakarta and I am currently learning Python.'
    }
]

# def github_activity(request):
#     github_username = 'ridwaanhall'
#     github_token = os.getenv('GITHUB_TOKEN')
#     api_url = f'https://api.github.com/users/{github_username}/events'

#     headers = {
#         'Authorization': f'Bearer {github_token}',
#         'Accept': 'application/vnd.github.v3+json',
#     }

#     response = requests.get(api_url, headers=headers)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Convert the response data to JSON
#         data = response.json()
#         # Return a JsonResponse with the fetched data
#         return JsonResponse(data, safe=False)
#     else:
#         # If the request was not successful, return an error response
#         return JsonResponse({'error': 'Failed to fetch GitHub data'}, status=response.status_code)


def github_activity(request):
    username = "ridwaanhall"
    access_token = os.getenv("GITHUB_SECRET")
    api_url = "https://api.github.com/graphql"

    query = """
      query {
        user(login: "%s") {
          contributionsCollection {
            contributionCalendar {
              colors
              totalContributions
              months {
                firstDay
                name
                totalWeeks
              }
              weeks {
                firstDay
                contributionDays {
                  color
                  contributionCount
                  date
                }
              }
            }
          }
        }
      }
    """ % username

    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    # mMBj-1pt0BagssdPKWNJvT_-jFeb5DuSD8a7iSM2Rdw
    data = json.dumps({"query": query})

    print(os.getenv("GITHUB_SECRET"))

    response = requests.post(api_url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        response_data = response.json()
        # Return a JsonResponse with the fetched data
        return JsonResponse(response_data, safe=False)
    else:
        # If the request was not successful, return an error response
        return JsonResponse({'error': 'Failed to fetch GitHub data'}, status=response.status_code)


def fetch_github_activity(username):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    api_url = "https://api.github.com/graphql"

    query = """
      query {
        user(login: "%s") {
          contributionsCollection {
            contributionCalendar {
              colors
              totalContributions
              months {
                firstDay
                name
                totalWeeks
              }
              weeks {
                firstDay
                contributionDays {
                  color
                  contributionCount
                  date
                }
              }
            }
          }
        }
      }
    """ % username

    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    data = json.dumps({"query": query})

    response = requests.post(api_url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {'error': 'Failed to fetch GitHub data!'}
    

def home(request):
    sidebar_data = Sidebar.objects.first()
    home_data = Home.objects.first()
    
    context = {
        'sidebar_data': sidebar_data,
        'home_data': home_data,
    }
    
    return render(request, 'base/home.html', context)

def dashboard_ahehe(request):
    # about = None
    # for i in abouts:
    #     if i['id'] == int(pk):
    #         about = i
    # context = {'about': about}

    response = requests.get("https://my-portfolio.ridwaanhall.repl.co/github-activity/")

    # Get JSON data
    data = json.loads(response.text)
    monthly_counts = {}
    for month in data['data']['user']['contributionsCollection']['contributionCalendar']['months']:
        year_month = f"{month['firstDay'][:7]}"
        total_for_month = 0

        for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
            if week['firstDay'].startswith(year_month):
                for day in week['contributionDays']:
                    total_for_month += day['contributionCount']

        monthly_counts[year_month] = total_for_month
    
    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
        'monthly_counts': monthly_counts,
        'monthly_contributions': list(monthly_counts.keys())[::-1],
        'total_contributions': list(monthly_counts.values())[::-1],
    }
    return render(request, 'base/dashboard.html', context)

def dashboard(request):
    response = requests.get("https://my-portfolio.ridwaanhall.repl.co/github-activity/")
    data = json.loads(response.text)

    daily_contributions = []

    for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
        for day in week['contributionDays']:
            date_str = day['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

            daily_contributions.append({
                "date": date_str,
                "contributionCount": day['contributionCount']
            })

    # Sorting the daily_contributions by date
    sorted_daily_contributions = sorted(daily_contributions, key=lambda x: x["date"])

    # Extracting dates and contribution counts into separate lists
    dates = [day["date"] for day in sorted_daily_contributions]
    daily_counts = [day["contributionCount"] for day in sorted_daily_contributions]

    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
        'dates': dates,
        'daily_counts': daily_counts,
    }

    return render(request, 'base/dashboard.html', context)

def project(request):

    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/project.html', context)

def certificate(request):
    
    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/certificate.html', context)

def about(request):

    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/about.html', context)

def contact(request):

    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/contact.html', context)

def playground(request):
    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/playground.html', context)