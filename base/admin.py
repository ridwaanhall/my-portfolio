from django.contrib import admin

# Register your models here.
from .models import Project, Skill, Sidebar, Home, About, Education, Logo, Certificate, Message, Credential, Quote, Career, Responsibility, CareerSkill

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Sidebar)
admin.site.register(Home)
admin.site.register(About)
admin.site.register(Education)
admin.site.register(Logo)
admin.site.register(Certificate)
admin.site.register(Message)
admin.site.register(Credential)
admin.site.register(Quote)

# @admin.register(Career)
# class CareerAdmin(admin.ModelAdmin):
#     list_display = ('position', 'company_name', 'location', 'start_date', 'end_date', 'current', 'employment_type', 'location_type')
#     search_fields = ('company_name', 'position', 'location')
#     list_filter = ('employment_type', 'location_type', 'start_date', 'end_date', 'current')


class ResponsibilityInline(admin.TabularInline):
    model = Responsibility
    extra = 1

class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1

class CareerAdmin(admin.ModelAdmin):
    inlines = [ResponsibilityInline, CareerSkillInline]
    list_display = ('position', 'company_name', 'location', 'start_date', 'end_date', 'current', 'employment_type', 'location_type')
    search_fields = ('company_name', 'position', 'location')
    list_filter = ('employment_type', 'location_type', 'start_date', 'end_date', 'current')

admin.site.register(Career, CareerAdmin)
admin.site.register(Responsibility)