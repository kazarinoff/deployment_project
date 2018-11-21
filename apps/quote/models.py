from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

class USER(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return ("USER: {}".format(self.first_name))

class RegistrationManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (not NAME_REGEX.match(postData['first_name'])):
            errors["first_name"] = "Please enter your first name, using only letters."
        if (len(postData['last_name']) < 1) or (not NAME_REGEX.match(postData['last_name'])):
            errors["last_name"] = "Please enter your last name, using only letters."
        if (len(postData['email'])< 1) or (not EMAIL_REGEX.match(postData['email'])):
            errors['email'] ="Please enter a valid email address"    
        if (len(USER.objects.filter(email=postData['email'])))>0:
            errors['email'] = "This email is already in database. Please try again."
        if postData['password']!=postData['confirmpw']:
            errors['confirmpw']="Your passwords did not match. Please try again."
        if len(postData['password'])<8:
            errors['password']="Please choose a password with at least 8 characters."
        return errors
    def validateupdate(self,postData):
        errors = {}
        if (len(postData['first_name']) < 1) or (not NAME_REGEX.match(postData['first_name'])):
            errors["first_name"] = "Please enter your first name, using only letters (sorry artist formally known as Prince)"
        if (len(postData['last_name']) < 1) or (not NAME_REGEX.match(postData['last_name'])):
            errors["last_name"] = "Please enter your last name, using only letters (sorry artist formally known as Prince)"
        if (len(postData['email'])< 1) or (not EMAIL_REGEX.match(postData['email'])):
            errors['email'] ="Please enter a valid email address" 
        if (len(USER.objects.filter(email=postData['email'])))>1:
            errors['email'] = "This email is already in database. Please try again."

        return errors
    def validatelogin(self,postData):
        errors={}

class QUOTE(models.Model):
    author=models.CharField(max_length=100)
    text=models.TextField()
    writer=models.ForeignKey(USER,on_delete="CASCADE",related_name='quotes')    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(USER,related_name='likedquotes')
    def __repr__(self):
        return ("MESSAGE: {}".format(self.author))

