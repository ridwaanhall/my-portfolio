from django.shortcuts import render
from django.http import JsonResponse
import requests, os, json

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
        return {'error': 'Failed to fetch GitHub data'}
    

def home(request):
    return render(request, 'base/home.html')

def dashboard(request):
    # about = None
    # for i in abouts:
    #     if i['id'] == int(pk):
    #         about = i
    # context = {'about': about}
    github_data = fetch_github_activity(username="ridwaanhall")
    return render(request, 'base/dashboard.html', {'github_data': github_data})