from django.shortcuts import render, HttpResponse, redirect
from apps.quote.models import *
from datetime import datetime
import bcrypt

def index(request):
    if 'loggedid' in request.session:
        return redirect('/quotes/')
    if 'errors' in request.session:
        context=request.session['errors']
    else:
        context={}
    return render(request,'login.html',context)

def regval(request):
    validator= RegistrationManager()
    if request.method=='POST':
        request.session.clear()
        errors= validator.validate(request.POST)
        if not len(errors):
            pwd=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            password=pwd.decode('utf-8')
            USER.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=password)
            request.session['loggedid']=USER.objects.last().id
            return redirect('/quotes/')
        else:
            request.session['errors']=errors
            return redirect('/')
    return redirect('/')

def loginval(request):
    if request.method=='POST':
        request.session.clear()
        x=USER.objects.get(email=request.POST['email'])
        print(x,'###########')
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), x.password.encode()):
            request.session['loggedid']=x.id
            return redirect('/quotes/')
        else:
            request.session['errors']={'loginpassword':"Your password did not match your account. Please try again."}
            return redirect('/')
    return redirect('/')

def quotes(request):
    if 'errors' not in request.session:
        request.session['errors']={}
    if 'loggedid' in request.session:
        loggedinuser=USER.objects.get(id=request.session['loggedid'])
        quotes=QUOTE.objects.all()
        context= {"userinfo":loggedinuser,"quotes":quotes, 'errors':request.session['errors']}
        return render(request,'quotewall.html',context)
    return redirect('/')

def postquote(request):
    if request.method=='POST':
        request.session['errors']={}
        if len(request.POST['author'])<4:
            request.session['errors']['author']="What author's name is that short?!? Try again."
            return redirect('/quotes/')
        if len(request.POST['quotetext'])<11:
            request.session['errors']['quote']='This quote is too short. Try again.'
            return redirect('/quotes/')
        x=USER.objects.get(id=request.session['loggedid'])
        QUOTE.objects.create(author=request.POST['author'],text=request.POST['quotetext'],writer=x)
    return redirect('/quotes/')

def logout(request):
    request.session.clear()
    return redirect('/')

def edituser(request):
    if 'errors' not in request.session:
        request.session['errors']={}
    x=USER.objects.get(id=request.session['loggedid'])
    return render(request, 'useredit.html', {'first_name':x.first_name,'last_name':x.last_name,'email':x.email,'id':x.id, 'errors':request.session['errors']})

def updateuser(request):
    validator= RegistrationManager()
    if request.method=='POST':
        request.session['errors']={}
        errors= validator.validateupdate(request.POST)
        request.session['errors']=errors
        if len(errors)>0:
            return redirect('/myaccount/')
        x=USER.objects.get(id=request.session['loggedid'])
        x.first_name=request.POST['first_name']
        x.last_name=request.POST['last_name']
        x.email=request.POST['email']
        x.save()
        return redirect('/quotes/')
    return redirect('/')

def like(request):
    if request.method=='POST':
        x=QUOTE.objects.get(id=request.POST['quoteid'])
        x.likes.add(USER.objects.get(id=request.session['loggedid']))
    return redirect('/quotes/')

def userview(request,userid):
    x=USER.objects.get(id=userid)
    quotes=QUOTE.objects.filter(writer=x)
    return render(request, 'userpage.html',{'first_name':x.first_name,'last_name':x.last_name, 'quotes':quotes})

def deletequote(request):
    if request.method=='POST':
        x=QUOTE.objects.get(id=request.POST['quoteid'])
        x.delete()
    return redirect('/quotes/')
