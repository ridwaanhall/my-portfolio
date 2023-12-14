from django.contrib import admin

# Register your models here.
from .models import Project, Skill, Sidebar, Home, About, Education, Logo, Certificate

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Sidebar)
admin.site.register(Home)
admin.site.register(About)
admin.site.register(Education)
admin.site.register(Logo)
admin.site.register(Certificate)