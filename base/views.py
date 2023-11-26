from django.shortcuts import render

# Create your views here.
abouts = [
    {
        'id': 1,
        'name': 'Ridwan Halim',
        'title': 'Python Developer',
        'description': 'I am a developer who loves to solve problems and create beautiful and functional applications. I am a student at University of Technology Yogyakarta and I am currently learning Python.'
    },
    {
        'id': 2,
        'name': 'hafidhah Afkariana',
        'title': 'Law',
        'description': 'I am a lawyer who loves to solve problems and create beautiful and functional applications.'
    },
    {
        'id': 3,
        'name': 'hapidoo',
        'title': 'Web Developer',
        'description': 'I am a web developer who loves to solve problems and create beautiful and functional applications'
    }
]

def home(request):
    context = {'abouts': abouts}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')