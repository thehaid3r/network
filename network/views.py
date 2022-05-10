from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import postForm,NewEditPostForm
from .models import User , Post,Profile
from django.core.paginator import Paginator



def index(request):
    print(request.user.username)
    form=postForm()
    if request.method=='POST':
        form=postForm(request.POST)
        
        if form.is_valid():
            form1=form.save(commit=False)
            form1.username=request.user.username
            form1.user=request.user
            form1.save()
            return redirect('index')
    else:
        try:
            posts=Post.objects.all().order_by('-date_posted')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "network/index.html" , {
            'form':form,
            'posts':posts,
            'page_obj':page_obj,
            'editform':NewEditPostForm()})
        except:           
            return render(request, "network/index.html" , {'form':form,
            'editform':NewEditPostForm()})
# like session
def like(request,id):
    if  request.user.is_authenticated :
        post=Post.objects.get(id=id)
        like=post.likes.all()
        for l in like:
            if request.user.id==l.id:
                post.likes.remove(request.user)
                count=post.likes.count()
                return JsonResponse({"result": 'removed','count':count}) 
        post.likes.add(request.user.id)
        post.save()
        print(post.likes.count())
        count=post.likes.count()
        return JsonResponse({"result": 'added','count':count})
    else:
        return render(request, "network/login.html")     



# profile session
def profile(request,str):
    if request.user.is_authenticated:
        form=postForm()
        if request.method=='POST':
            form=postForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.username=request.user.username
                form1.user=request.user
                form1.save()
                return redirect('profile',request.user.username)
        result="Follow"
        follow=User.objects.get(username=str)
        p=Profile.objects.filter(follower=request.user,following=follow).count()
        total_followers=Profile.objects.filter(following=follow)
        total_following=Profile.objects.filter(follower=follow)
        print(total_followers)
        print(total_following)
        posts=Post.objects.filter(username=str).order_by('-date_posted')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if p==1:
            result="Unfollow"
            return render(request, "network/profile.html" , { 
                'prof':follow,
                'page_obj':page_obj,
                'result':result,
                'total_followers':total_followers,
                'total_following':total_following,
                'form':form,
                'editform':NewEditPostForm()
                
            })
        else:
            return render(request, "network/profile.html" , { 
                'prof':follow,
                'page_obj':page_obj,
                'result':result,
                'total_followers':total_followers,
                'total_following':total_following,
                'form':form,
                'editform':NewEditPostForm()
            })
    else:
        return render(request, "network/login.html")    
# follow
def follow(request,str):
    
    follow=User.objects.get(username=str)
    p=Profile.objects.get_or_create(follower=request.user,following=follow)
    if not p[1] :
        Profile.objects.filter(follower=request.user,following=follow).delete()
        result="Unfollow"
    else:
        result="Follow"    
    return redirect('profile',str)
# folloing session
def following(request,str):
    if request.user.is_authenticated :
        form=postForm()
        if request.method=='POST':
            form=postForm(request.POST)
            if form.is_valid():
                form1=form.save(commit=False)
                form1.username=request.user.username
                form1.user=request.user
                form1.save()
                return redirect('following')
        else:
            followers=Profile.objects.filter(follower=request.user.id)
            posts=Post.objects.filter(user_id__in= followers.values('following_id'))
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "network/following.html" , {
                    'form':form,
                    'posts':posts,
                    'page_obj':page_obj})
    else:
        return render(request, "network/login.html")                 
#edit session
def edit(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewEditPostForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data["id_post_edit_text"]
                Post.objects.filter(
                    id=id, user_id=request.user.id).update(content=text)
                return JsonResponse({"result": 'ok', 'text': text})
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": HttpResponseBadRequest("Bad Request: no like chosen")}, status=400)
    else:
        return render(request, "network/login.html")    

    



# login session
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
