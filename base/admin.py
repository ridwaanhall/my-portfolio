from django.contrib import admin

# Register your models here.
from .models import Project, Skills, Sidebar, Home, About, Education

admin.site.register(Project)

admin.site.register(Skills)

admin.site.register(Sidebar)

admin.site.register(Home)

admin.site.register(About)

admin.site.register(Education)