from django.db import models
import re
import bcrypt

# region initializers
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PSWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')
    # Password matching expression. Password must be at least 8 characters, 
    # no more than 15 characters, and must include at least one upper case 
    # letter, one lower case letter, and one numeric digit. Howardhoward1
# endregion

class ShowManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name_error'] = "At least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name_error'] = "At least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_error'] = "Not a valid email address"
        if self.filter(email=postData['email']):
            errors['email_error'] = "Email already exists"
        if not PSWD_REGEX.match(postData['password']):
            errors['password_error'] = "Not a valid password"
        if postData['password'] != postData['conf_password']:
            errors['conf_pswd_error'] = "Confirmation Password doesn't match Password"
        return errors

    def register(self, postData):
        hashed_pswd = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        uid = self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_pswd
        ).id
        return uid

    def login(self, postData):
        errors={}
        user = self.filter(email = postData['email'])
        print(user.values())
        if len(user) == 0:
            errors['login_user_error'] = "Email you entered does not exist"
            return errors
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['login_pswd_error'] = "Password does not match"
            return errors
        else:
            user_id = user[0].id
            hashed_id = bcrypt.hashpw(str(user_id).encode(), bcrypt.gensalt())
            return
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.TextField()
    objects = ShowManager()
