from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv
from .models import chat
from django.utils import timezone
import json

load_dotenv()


import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)


import textwrap
from markdown import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    md = Markdown()
    return md.convert(textwrap.indent(text, '> ', predicate=lambda _: True))


def ask_api(message):
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(message)
    print(type(response.text))
    ans = to_markdown(response.text)
    
    return str(ans)
    # return response.text

# if request.user.is_authenticated:
#             # Filter the queryset using the user's ID
#             chats = chat.objects.filter(user=request.user.id)

def chatbot(request):
    chats = chat.objects.filter(user=request.user.id)
    if request.method =='POST':
        message = request.POST.get('message')
        response = ask_api(message)
        ch =chat(user=request.user,message=message,response=response,created_at=timezone.now())
        ch.save()
        return JsonResponse({'meaasge':message, 'response':response})
        
    return render(request,'chatbot.html',{'chats':chats})


def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message='Invalid user'
            return render(request,'login.html',{'error_message':error_message})
    else:  
        return render(request,'login.html')


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if(password1==password2):
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message='erroe created in account'
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message='password does not  match'
            return render(request,'register.html',{'error_message':error_message})

    return render(request,'register.html')

def logout(request):
    auth.logout(request) 
    return redirect('login')
