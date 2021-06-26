from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def basic_validations(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name']='Name should be at least 2 characters'
        if len(postData['last_name'])<2:
            errors['last_name']='Name should be at least 2 characters'
        if len(postData['password'])<4:
            errors['password']='Password should be at least 4 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirmation'] = 'Passwords do not match'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']= "Email is not valid"
        else:
            user=User.objects.filter(email=postData['email'])
            if len(user)>1:
                errors['email_registered']='Email already registered. Please try another one'
        
        return errors

    def login_validations(self, postData):
        errors ={}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']= "Email is not valid"
        else:
            email_register= User.objects.filter(email=postData['email'])
            if len(email_register)==0:
                errors['email_register'] = 'This email is not registered'
                print('***'*50)
                return errors
            else:
                user=email_register[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password']='Wrong password'
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
