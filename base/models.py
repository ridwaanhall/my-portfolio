from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='static/img/projects/')
    # url = models.URLField()
    github_url = models.URLField()
    demo_url = models.URLField()
    date_start = models.CharField(max_length=255, blank=True)
    date_finish = models.CharField(max_length=255, default='now')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# user data sidebar model. name and username
class Sidebar(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='static/img/avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# create database firstname, role (such as student, web developer), based (the location of the user), shorttext (is a short description. ).
class Home(models.Model):
    firstname = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    based = models.CharField(max_length=255)
    shorttext = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname
    
# create about database. such as long text.
class About(models.Model):
    longtext = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.longtext

class Logo(models.Model):
    logo = models.ImageField(upload_to='static/img/logos/')
    logo_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.logo_name

class Education(models.Model):
    logo = models.URLField()
    css_code_label = models.CharField(max_length=255, blank=True)
    css_code_text = models.CharField(max_length=255, blank=True)
    name_education = models.CharField(max_length=255)
    level = models.CharField(max_length=255, blank=True, null=True)
    study_programs = models.CharField(max_length=255, blank=True, null=True)
    title_study = models.CharField(max_length=255, blank=True, null=True)
    date_start = models.CharField(max_length=255)
    date_end = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_education
    
class Skill(models.Model):
    # text and skill name
    text = models.CharField(max_length=255)
    name_skill = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name_skill