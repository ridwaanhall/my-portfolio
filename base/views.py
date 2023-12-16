from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, os, json
from .models import Sidebar, Home, Project, Education, About, Skill, Message, Credential
from datetime import datetime, timedelta
from statistics import mean


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

    # print(os.getenv("GITHUB_SECRET"))

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
    latest_projects = Project.objects.order_by('-created_at')[:3]
    latest_educations = Education.objects.order_by('-created_at')[:1]
    
    context = {
        'sidebar_data': sidebar_data,
        'home_data': home_data,
        'latest_projects': latest_projects,
        'latest_educations': latest_educations,
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


def format_date(date_str):
    if date_str is not None:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b, %d %Y')
    else:
        # Handle the case where date_str is None
        return 'Invalid Date'  # or any other appropriate default value

def dashboard(request):
    sidebar_data = Sidebar.objects.first()
    response = requests.get("https://my-portfolio.ridwaanhall.repl.co/github-activity/")
    data = json.loads(response.text)

    first_day_of_first_week = None
    for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
        if week['firstDay']:
            first_day_of_first_week = week['firstDay']
            break

    last_day_of_last_week = None
    for week in reversed(data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']):
        if week['contributionDays']:
            last_day_of_last_week = week['contributionDays'][-1]['date']
            break

    daily_contributions = []
    
    for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']:
        for day in week['contributionDays']:
            date_str = day['date']
            # date_obj = datetime.strptime(date_str, '%Y-%m-%d')

            daily_contributions.append({
                "date": date_str,
                "contributionCount": day['contributionCount']
            })

    # Sorting the daily_contributions by date
    sorted_daily_contributions = sorted(daily_contributions, key=lambda x: x["date"])

    # Extracting dates and contribution counts into separate lists
    dates = [day["date"] for day in sorted_daily_contributions]
    daily_counts = [day["contributionCount"] for day in sorted_daily_contributions]

    total_contributions = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']

    # Calculate contributions for this week
    this_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    this_week_contributions = sum(day['contributionCount'] for week in data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
                                  for day in week['contributionDays'] if datetime.strptime(day['date'], '%Y-%m-%d') >= this_week_start)

    # Calculate best day
    best_day = max(daily_counts)

    # Calculate average contributions per day
    average_contributions = mean(daily_counts)
    rounded_average = round(average_contributions)

    # Calculate current streak
    current_streak = 0
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_streak_start = None
    current_streak_end = None

    for day in sorted_daily_contributions[::-1]:
        if day['date'] == current_date and day['contributionCount'] > 0:
            if current_streak == 0:
                current_streak_end = current_date
            current_streak += 1
            current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            break

    if current_streak > 0:
        current_streak_start = (datetime.strptime(current_streak_end, '%Y-%m-%d') - timedelta(days=current_streak - 1)).strftime('%Y-%m-%d')

    # Calculate longest streak
    longest_streak = 0
    current_streak = 0
    longest_streak_start = None
    longest_streak_end = None

    for day in sorted_daily_contributions:
        if day['contributionCount'] > 0:
            current_streak += 1
            if current_streak == 1:
                longest_streak_start = day['date']
            longest_streak_end = day['date']
        else:
            current_streak = 0

        if current_streak > longest_streak:
            longest_streak = current_streak

    context = {
        'sidebar_data': sidebar_data,
        'dates': dates,
        'daily_counts': daily_counts,

        'total_contributions': total_contributions,
        'this_week_contributions': this_week_contributions,
        'best_day': best_day,
        'average_contributions': rounded_average,
        
        'current_streak': current_streak,
        'current_streak_start': format_date(current_streak_start),
        'current_streak_end': format_date(current_streak_end),
        
        'longest_streak': longest_streak,
        'longest_streak_start': longest_streak_start,
        'longest_streak_end': longest_streak_end,

        'first_day': first_day_of_first_week,
        'last_day': last_day_of_last_week,
        'first_day_format': format_date(first_day_of_first_week),
        'last_day_format': format_date(last_day_of_last_week),
    }

    return render(request, 'base/dashboard.html', context)

def project(request):

    sidebar_data = Sidebar.objects.first()
    projects = Project.objects.order_by('-created_at')
    total_projects = Project.objects.count()
    
    context = {
        'sidebar_data': sidebar_data,
        'projects': projects,
        'total_projects': total_projects,
    }
    
    return render(request, 'base/project.html', context)

def certificate(request):
    # credentials = Credential.objects.order_by('-created_at')
    credentials = Credential.objects.all().values()
    credentials_list = list(credentials)
    sidebar_data = Sidebar.objects.first()

    data = [
        {
            "id": credential["id"],
            "company_logo": credential["company_logo"],
            "company_name": credential["company_name"],
            "issued_date": credential["issued_date"],
            "name": credential["name"],
            "skills": credential["skills"],
            "url_credential": credential["url_credential"],
            "type": credential["type"],
        }
        for credential in credentials_list
    ]
    
    context = {
        'sidebar_data': sidebar_data,
        'credentials': data,
    }
    
    return render(request, 'base/certificate.html', context)

def about(request):
    sidebar_data = Sidebar.objects.first()
    abouts = About.objects.first()
    latest_educations = Education.objects.order_by('-created_at')[:2]
    # skills = Skill.objects.order_by('-created_at')
    skills_1 = Skill.objects.all().order_by('?')
    skills_2 = Skill.objects.all().order_by('?')
    skills_3 = Skill.objects.all().order_by('?')

    context = {
        'sidebar_data': sidebar_data,
        'latest_educations': latest_educations,
        'abouts': abouts,
        'skills': skills_1,
        'skills_2': skills_2,
        'skills_3': skills_3,
        
    }
    
    return render(request, 'base/about.html', context)

# def contact(request):

#     sidebar_data = Sidebar.objects.first()

#     context = {
#         'sidebar_data': sidebar_data,
#     }
    
#     return render(request, 'base/contact.html', context)
def contact(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        message = Message(name=name, email=email, message=message_text)
        message.save()

        success_message = f'Message sent successfully! with name {name} and email {email}'
        
        return redirect('contact')


    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
        'success_message': success_message,
    }

    return render(request, 'base/contact.html', context)


def playground(request):
    sidebar_data = Sidebar.objects.first()

    context = {
        'sidebar_data': sidebar_data,
    }
    
    return render(request, 'base/playground.html', context)