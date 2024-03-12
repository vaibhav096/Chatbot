from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import chat
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json


import os
from dotenv import load_dotenv
load_dotenv()

import textwrap
import google.generativeai as genai

from IPython.display import Markdown

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

import markdown2
import markdown2

def make_html(markdown_text):
    html_content = markdown2.markdown(markdown_text)
    print(html_content)
    html_document = f"<html><head><title>Markdown to HTML</title></head><body>{html_content}</body></html>"
    return html_content



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def ask_api(message):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(message)
    # print(to_markdown(response.text))
    return to_markdown(response.text).data

@login_required(login_url='/login')
def chatbot(request):
    chats = chat.objects.filter(user=request.user.id)
    if request.method =='POST':
        message = request.POST.get('message')
        response = ask_api(message)
        # new_res = response.data
        res=make_html(response)
        ch =chat(user=request.user,message=message,response=res,created_at=timezone.now())
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

@login_required(login_url='/login')
def logout(request):
    auth.logout(request) 
    return redirect('login')
