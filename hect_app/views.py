from django.shortcuts import render,redirect
from . import models
from .forms import UserForm,RegisterForm
import hashlib
from django.core.files.storage import default_storage
from django.http import FileResponse
import os

def hash_code(s,salt = 'cgu'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    return render(request,'index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name']=user.name
                    return redirect('/index/')
                else:
                    message = 'wrong username or password'
            except:
                message = 'wrong username or password'
        return render(request,'login.html',locals())
    login_form = UserForm()
    return render(request,'login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = 'he password should be same'
                return render(request,'register.html',locals())
            else:
                is_same_user = models.User.objects.filter(name = username)
                if is_same_user:
                    message = 'username exist'
                    return render(request,'register.html',locals())
                is_same_email = models.User.objects.filter(email = email)
                if is_same_email:
                    message = 'email has been registered'
                    return render(request,'register.html',locals())
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def images(request):
    currentuser = request.session.get('user_name')
    if request.method == 'POST':
        image = request.FILES.get('img')
        print(image.size)
        print(image.name)
        if image.size > 2500000:
            message = 'image is too big, try smaller one'
            return render(request,'images.html',locals())
        title = image.name
        is_same_img = models.Img.objects.filter(img_name=title)
        if is_same_img:
            message = 'image already exist'
            return render(request,'images.html',locals())
        new_image = models.Img.objects.create()
        new_image.img_name = title
        new_image.user_name = currentuser
        new_image.img_url = image
        par1 = 'media\\img\\'+ str(new_image.img_url)
        par2 = 'media\\output'
        new_image.save()
        os.system('Tesseract-OCR\\tesseract.exe %s %s' % (par1, par2))

        text_path = par2 + '.txt'
        text = open(text_path)
        text_trans = text.read()

        text_image = models.Text.objects.create()
        text_image.img_name = title
        text_image.img_url = new_image.img_url
        text_image.user_name = currentuser
        text_image.text_content = text_trans
        text_image.save()
        text.close()
    try:
        imgs = models.Img.objects.filter(user_name=currentuser)
        text = models.Text.objects.filter(user_name=currentuser)
        context = {
            'imgs': imgs,
            'text':text
        }
    except:
        context = {}
    return render(request,'images.html',context)

def delimgs(request,id):
    url=models.Img.objects.get(id=id).img_url
    default_storage.delete(url)
    models.Img.objects.get(id=id).delete()
    models.Text.objects.get(img_url=url).delete()
    return redirect('/images/')

def downloadimgs(request,id):
    url ='media/'+ str(models.Img.objects.get(id=id).img_url)
    file = open(url,'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] =  'attachment;filename="{0}"'.format(models.Img.objects.get(id=id).img_name)
    return response

