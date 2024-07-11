from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import requests, os, json
from .models import Sidebar, Home, Project, Education, About, Skill, Message, Credential, Quote
from datetime import datetime, timedelta
from statistics import mean
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def github_activity(request):
    username = "ridwaanhall"
    access_token = "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"
    #print(access_token)
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
    if response.status_code == 200:
        response_data = response.json()
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch GitHub data'},
                            status=response.status_code)


def download_resume(request):
    download_resume = "https://docs.google.com/document/d/1Sv2VQ95fDn-0a_8lOZxBuFAZ--gJrw7u5EQ-_SLUfpo/edit"
    return redirect(download_resume)


def home(request):
    sidebar_data = Sidebar.objects.first()
    home_data = Home.objects.first()
    latest_projects = Project.objects.order_by('-created_at')[:3]
    latest_educations = Education.objects.order_by('-created_at')[:1]
    quote_of_the_day = Quote.objects.order_by('?')[:1]
    all_quotes = Quote.objects.all()

    context = {
        'sidebar_data': sidebar_data,
        'home_data': home_data,
        'latest_projects': latest_projects,
        'latest_educations': latest_educations,
        'quote_of_the_day': quote_of_the_day,
        'all_quotes': all_quotes,
    }

    return render(request, 'base/home.html', context)


def format_date(date_str):
    if date_str is not None:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b, %d %Y')
    else:
        return 'Invalid Date'


def format_date_current(date_str):
    if date_str is not None:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%b, %d %Y')
    else:
        return datetime.now().strftime('%b, %d %Y')


def dashboard(request):
    sidebar_data = Sidebar.objects.first()
    response = requests.get(
        "https://aaff0b3f-edba-4302-84e4-4c21fe434e72-00-18ppstrxi56pp.worf.replit.dev/github-activity/"
    )
    data = json.loads(response.text)

    first_day_of_first_week = None
    for week in data['data']['user']['contributionsCollection'][
            'contributionCalendar']['weeks']:
        if week['firstDay']:
            first_day_of_first_week = week['firstDay']
            break

    last_day_of_last_week = None
    for week in reversed(data['data']['user']['contributionsCollection']
                         ['contributionCalendar']['weeks']):
        if week['contributionDays']:
            last_day_of_last_week = week['contributionDays'][-1]['date']
            break

    daily_contributions = []

    for week in data['data']['user']['contributionsCollection'][
            'contributionCalendar']['weeks']:
        for day in week['contributionDays']:
            date_str = day['date']

            daily_contributions.append({
                "date":
                date_str,
                "contributionCount":
                day['contributionCount']
            })

    # Sorting the daily_contributions by date
    sorted_daily_contributions = sorted(daily_contributions,
                                        key=lambda x: x["date"])

    # Extracting dates and contribution counts into separate lists
    dates = [day["date"] for day in sorted_daily_contributions]
    daily_counts = [
        day["contributionCount"] for day in sorted_daily_contributions
    ]

    total_contributions = data['data']['user']['contributionsCollection'][
        'contributionCalendar']['totalContributions']

    # Calculate contributions for this week
    this_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    this_week_contributions = sum(
        day['contributionCount'] for week in data['data']['user']
        ['contributionsCollection']['contributionCalendar']['weeks']
        for day in week['contributionDays']
        if datetime.strptime(day['date'], '%Y-%m-%d') >= this_week_start)

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
            current_date = (datetime.strptime(current_date, '%Y-%m-%d') -
                            timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            break

    if current_streak > 0:
        current_streak_start = (
            datetime.strptime(current_streak_end, '%Y-%m-%d') -
            timedelta(days=current_streak - 1)).strftime('%Y-%m-%d')

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
        'current_streak_start': format_date_current(current_streak_start),
        'current_streak_end': format_date_current(current_streak_end),
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
    credentials = Credential.objects.all().values()
    credentials_list = list(credentials)
    sidebar_data = Sidebar.objects.first()

    data = [{
        "id": credential["id"],
        "company_logo": credential["company_logo"],
        "company_name": credential["company_name"],
        "issued_date": credential["issued_date"],
        "name": credential["name"],
        "skills": credential["skills"],
        "url_credential": credential["url_credential"],
        "type": credential["type"],
    } for credential in credentials_list]

    context = {
        'sidebar_data': sidebar_data,
        'credentials': data,
    }

    return render(request, 'base/certificate.html', context)


def about(request):
    sidebar_data = Sidebar.objects.first()
    abouts = About.objects.first()
    latest_educations = Education.objects.order_by('-created_at')[:2]
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


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request, 'base/login.html')


def logoutPage(request):
    logout(request)
    return redirect('home')


def comingSoon(request):
    return render(request, 'base/comingsoon.html')


def errorPage(request):
    return render(request, 'base/error.html', status=500)
