# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
# Create your views here.
def index(req):
    if 'id' not in req.session:
        req.session['id'] = 0
    if 'name' not in req.session:
        req.session['name'] = ""
    return render(req, 'belt_exam/index.html')

def register(req):
    if req.method == "POST":
        results = User.objects.validate_register(req.POST)       
        if results[0]:
            req.session['name'] = req.POST['name']
            req.session['id'] = results[1].id
            print  req.session['id'] 
            messages.success(req, "Successfully registered!")
            return redirect('/friends')
        else:
            errors = results[1]
            for result in errors:
                messages.error(req, errors[result])
            return redirect('/')
    return redirect('/')        

def success(req):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')  
    else:
        friends = User.objects.filter(friends= req.session['id'])
        all_users =  User.objects.all().exclude(id=req.session['id'])         
        users = all_users.exclude(friends= req.session['id'])        
        count = len(friends)      
        context = {
            'users' : users,
            'friends' : friends,
            'count' : count
        }
        return render(req, 'belt_exam/friends.html', context)         

def login(req):
    results = User.objects.validate_login(req.POST)
    if results[0]:
        req.session['id'] = results[1][0].id
        req.session['name'] = results[1][0].alias
        messages.success(req, "Successfully logged in)!")
        return redirect('/friends')
    else:
        for result in results[1]:
            messages.error(req, results[1][result])
        return redirect('/')

def addFriend(req):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')  
    else:
        if req.method == 'POST':
            results = User.objects.add_friend(req.POST, req.session['id'])
            if results[0] :         
                return redirect('/friends')
            else:
                for result in results[1]:
                    messages.error(req, results[1][result])
                return redirect('/friends')
        else:
            messages.error(req, "Wrong operation")
            return redirect('/friends')

def viewProfile(req, id):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')  
    else:
        results = User.objects.isFriend(id)
        if results[0]:
            context = {
                'profile' : results[1][0]
            }
            return render(req, 'belt_exam/profile.html', context)
        else:
            for result in results[1]:
                messages.error(req, results[1][result])
            return redirect('/friends')   

def removeFriend(req, id):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')
    else:
        results = User.objects.validate_remove(id, req.session['id'])  
        if results[0]:
            return redirect('/friends')
        else:
            for result in results[1]:
                messages.error(req, results[1][result])
            return redirect('/friends')

       
def logout(req):
    req.session.clear()
    return redirect('/')