from django.db import models
import re
from django.http import request

# Create your models here.
def validaremail(email = None):
    try:
        if email:
            match_email = users.objects.get(email=email)
    except:
        match_email = None
    return match_email

class usersManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["fname"] = "El nombre debe tener mas de 2 caractares"
        if len(postData['lname']) < 2:
            errors["lname"] = "El apellido debe tener mas de 2 caractares"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "El correo es invalido"
        if postData['password'] != postData['co-password']:
            errors["password"] = "El password no concide"
        if len(postData['password']) <8:
            errors["password"] = "La password debe tener mas de 8 digitos"
        if postData["email"]:
            email = validaremail(email=postData["email"])
            if email:
                errors['email'] = "El correo ya existe"
        print(errors)
        return errors

class users(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = usersManager()

class messages(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(users,related_name="all_messages", on_delete=models.CASCADE)

class comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(messages,related_name="all_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(users,related_name="all_users", on_delete=models.CASCADE)
