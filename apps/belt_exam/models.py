# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta

NAME_REGEX = re.compile(r'^([^0-9]*)$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^(?=.*?[A-Z]).*\d')
# Create your models here.
class UserManager(models.Manager):
    def validate_register(self, postdata):
        errors = {}
        email = postdata['email']       
        user = User.objects.filter(email_id=email)
        if len(user) > 0:
            errors['email'] =  "Please try another email id"
        else:    
            if postdata['name'] == "" :
                errors['name'] = "Please enter Name"
            else:            
                if len(postdata['name']) < 2:
                    errors["name"] = "Name should not be fewer than 2 characters"
                if not NAME_REGEX.match(postdata['name']):
                    errors['name'] = "Numeric characters are not allowed in Name"
            
            if postdata['alias'] == "":
                errors['alias'] = "Please enter Alias"
            else:
                if len(postdata['alias']) < 2:
                    errors["alias"] = "Alias should not be fewer than 2 characters"
                if not NAME_REGEX.match(postdata['alias']):
                    errors['alias'] = "Numeric characters are not allowed in Alias"

            if postdata['email'] == "":
                errors['email'] = "Please enter Email Id"
            else:
                if not EMAIL_REGEX.match(postdata['email']):
                    errors["email"] = "Invalid Email Address! please follow abc@xyz.com"

            if postdata['pwd'] == "":
                errors['pwd'] = "Please enter passwod"
            else:
                if len(postdata['pwd']) < 8:
                    errors['pwd'] = " Password must be 8 characters long"
                if not PWD_REGEX.match(postdata['pwd']):
                    errors['pwd'] = "Invalid password! Password must contain atleast 1 Uppercase and 1 numeric value "
                
            if postdata['cpwd'] == "":
                errors['cpwd'] = "Please enter confirm passwod"
            else:
                if postdata['pwd'] != postdata['cpwd']:
                    errors['pwd'] = "Confirm Password does not match with Password "
            
            if postdata['bday'] != "":
                bday = datetime.strptime(postdata['bday'], "%Y-%m-%d")
                cur_date = datetime.now()
                if bday > cur_date:
                    errors['bday'] = "Birthday date can not be after today"
                else:
                    if (cur_date - bday).days/365 < 18:
                        errors['bday'] = "You are not allowed to register because under 18  "
            else:
                errors['bday'] = "Please enter Birthday date"

        if len(errors) != 0:
            return (False, errors)
        else:    
            unhash = postdata['pwd']
            pwd = bcrypt.hashpw(unhash.encode(), bcrypt.gensalt())
            user = User.objects.create(name=postdata['name'], alias= postdata['alias'],email_id = postdata['email'],birthday = postdata['bday'], password = pwd)
            return (True, user)

    def validate_login(self, postdata):
        errors = {}
        if postdata['username'] == "" or postdata['pwd'] == "":
            errors['username'] = "Please enter email and password"        
        else:
            user = User.objects.filter(email_id=postdata['username'])
            if len(user) > 0:
                hash1 = user[0].password
                if bcrypt.checkpw(postdata['pwd'].encode(), hash1.encode()):
                    return (True, user)
                else:
                    errors['username'] = "Please verify username or password"
                    return (False, errors)
        return (False, errors)

    def add_friend(self, postdata, userid):  
        errors = {}    
        friend_id = postdata['fid']  
        isuser = User.objects.filter(id =friend_id)    
        if len(isuser): 
            if friend_id ==  userid :
                errors['friends'] = " You are not allowed to be friends with yuorself"
                return (False, errors)
            else:
                user = User.objects.get(id = userid)    
                friends = user.friends.add(friend_id)         
                return (True, friends )
        else:
            errors['friend'] = "You are not allowed to add this user"
            return (False, errors)


    def isFriend(self, fid):
        errors ={}
        isuser = User.objects.filter(id =fid)       
        if len(isuser) :           
            return ( True, isuser)
        else:
            errors['friend'] = "You are not allowed to perform this operation"
            return (False, errors)

        ################# You can implement below code if you dont want to allow view profile if you are not friend
        # friend = user.friends.filter(id = fid)
        # print friend       
        # if len(friend):
        #     return (True, friend)
        # else:
        #     errors['friend'] = "You are not allowed to view this profile"
        #     return (False, errors)
    
    def validate_remove(self, fid, userid):
        errors = {}
        friendExist = User.objects.filter(id = fid) 
        if len(friendExist):
            friedshipExist = friendExist[0].friends.filter(id = userid)
            if len(friedshipExist):
                user = User.objects.get(id=userid)
                friend = User.objects.get(id=fid)
                result = user.friends.remove(friend)
                print result
                return (True, result)
            else:
                errors['friend'] = "You are not allowed to remove this person"
                return (False, errors)
        else:
            errors['friend'] = " This operation is not allowed"
            return (False, errors)



            
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(default="", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField('self')

    objects = UserManager()