import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *





def login_view(request):
     return render(request, 'login-form.html')

# dashboard maate
def login(request):
    if request.session.get("username"):
        return redirect("dashboard")
    if request.method=="POST":
        data=request.POST
        username=data.get('username')
        password=data.get('password')

        sachin=MyUser.objects.filter(username=username,password=password).first()
        
        if sachin:
            request.session["username"]=sachin.username
            request.session["password"]=sachin.password
            return redirect("dashboard")
        else:
            return render(request,"login-form.html",{"msg":"Invalid login"})
    return render(request,"login-form.html")


def dashboard(request):
    if request.session.get("username"):
        return render(request,"dashboard/dashboard.html")
    else:
        return redirect("login")

def logout(request):
    request.session.flush()
    return redirect("login")



from myapp.models import *

# category maate

from .models import CategoryMaster
from django.utils.text import slugify

from .models import CategoryMaster
from django.shortcuts import render

# def home(request):
#     # सब categories ले आएंगे, sequence number के order में
#     category = CategoryMaster.objects.all().order_by('CatSeqNo')
#     return render(request, "home.html", {"category": category})


def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        seq = request.POST.get("seq")
        image = request.FILES.get('image')

        slug = slugify(name)

        isexit= CategoryMaster.objects.filter(CatName=name)
        if isexit:
            return render(request,"category/category-form.html",{"error":"Category already exists"})
        else:
            isSeqNo = CategoryMaster.objects.filter(CatSeqNo=seq)
            if isSeqNo:
                return render(request,"category/category-form.html",{"error":"Seq_no already exists"})
            else:
                CategoryMaster.objects.create(
                CatName=name, 
                CatSeqNo=seq,
                CatImage=image, 
                CatSlug=slug, 
                CatStatus=True
            )

        return redirect("category_list")
    return render(request, "category/category-form.html")

        

def category_page(request):
    category = CategoryMaster.objects.all().order_by('CatSeqNo')
    return render(request, "category/category.html", {"category": category})


def delete_category(request, id):
    sachin = CategoryMaster.objects.get(id=id)
    sachin.delete()
    return redirect("category_list")




from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import CategoryMaster

def update_category(request, id):
    sachin1 = CategoryMaster.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        seq = request.POST.get("seq")
        slug = slugify(name)
        # status=True if request.POST.get("status")== "on" else False
        status=True
        if request.POST.get("status")==None:
            status= False


        isexit = CategoryMaster.objects.filter(CatName=name)
        if isexit and name != sachin1.CatName:
            return render(request, "category/edit_category.html", {"error": "Category already exists","sachin1": sachin1})
        else:
            isSeqNo = CategoryMaster.objects.filter(CatSeqNo=seq)
            if isSeqNo and seq != str(sachin1.CatSeqNo):
                return render(request, "category/edit_category.html", {"error": "Seq_no already exists","sachin1": sachin1})
            else:
                sachin1.CatName = name
                sachin1.CatSeqNo = seq
                sachin1.CatSlug = slug
                sachin1.CatStatus = status

                sachin1.save()

            return redirect("category_list")

    return render(request, "category/edit_category.html", context={"sachin1": sachin1})


# article maate

from django.shortcuts import render
from .models import articale_master  # ensure correct spelling

# def home_page(request):
#     latest_articles = articale_master.objects.filter(status=True).order_by('-created_at')[:3]
#     trending_articles = articale_master.objects.filter(status=True).order_by('?')[:3]  # random 3 for trending

#     return render(request, "home.html", {
#         "latest_articles": latest_articles,
#         "trending_articles": trending_articles
#     })

  
def article_page(request):
    articles = articale_master.objects.all()  
    return render(request, "articales/articales.html", {"articles": articles})


def article_category(request):
       category = CategoryMaster.objects.all()
       return render(request,"articales/artical-form.html",{"category": category})

# def articale_create(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         image = request.FILES.get("image")
#         category_name = request.POST.get("category")   
#         description = request.POST.get("description")
#         status = request.POST.get("status") == "True"
#         is_featured = True if request.POST.get("is_featured") == "on" else False

#         print("Form Submitted:", title, category_name, status)
#         # NEW: trending checkbox and order
#         is_trending = True if request.POST.get("is_trending") == "on" else False
#         try:
#             trending_order = int(request.POST.get("trending_order") or 0)
#         except ValueError:
#             trending_order = 0

#         if category_name:   # blank category allow mat karo
#             category_instance, created = CategoryMaster.objects.get_or_create(CatName=category_name)

#             new_article = articale_master.objects.create(
#                 title=title,
#                 image=image,
#                 category=category_instance,
#                 description=description,
#                 status=status,
#                 is_featured=is_featured,
#                 is_trending=is_trending,
#                 trending_order=trending_order,
#             )
            
#         else:
#             print("❌ Category not selected")

#     category_list = CategoryMaster.objects.all()
#     tag_list = TrendingTag.objects.all()   # ✅ tags list pass karna
#     return render(request, "articales/artical-form.html", {
#         "category": category_list,
#         "tags": tag_list
#     })

from django.shortcuts import render, redirect, get_object_or_404
from .models import articale_master, CategoryMaster, TrendingTag

def articale_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category_name = request.POST.get("category")   # ID lena better hai
        description = request.POST.get("description")
        status = request.POST.get("status") == "True"
        is_featured = True if request.POST.get("is_featured") == "on" else False
        # is_trending = True if request.POST.get("is_trending") == "on" else False

        # NEW: trending checkbox and order
        is_trending = True if request.POST.get("is_trending") == "on" else False
        try:
            trending_order = int(request.POST.get("trending_order") or 0)
        except ValueError:
            trending_order = 0

        # ✅ Category required check
        if category_name:
            category_instance, created = CategoryMaster.objects.get_or_create(CatName=category_name)

            new_article = articale_master.objects.create(
                title=title,
                image=image,
                category=category_instance,
                description=description,
                status=status,
                is_featured=is_featured,
                is_trending=is_trending,
                trending_order=trending_order,
                
            )

            # ✅ Handle Tags (ManyToMany)
            tags_ids = request.POST.getlist("tags")   # multiple select
            if tags_ids:
                new_article.tags.set(tags_ids)

            print("✅ Article Saved:", new_article.id)
            return redirect("article_page")  # article list ya detail page pe bhejo

        else:
            print("❌ Category not selected")

    # GET request ke liye category aur tags bhejna
    category_list = CategoryMaster.objects.all()
    tag_list = TrendingTag.objects.all()
    return render(request, "articales/artical-form.html", {
        "category": category_list,
        "tags": tag_list
    })



def delete_articale(request,id):
    result=articale_master.objects.get(id=id)
    result.delete()
    return redirect("article_page")


# def edit_articale(request,id):
#     employee=articale_master.objects.get(id=id)
#     category = category_master.objects.all()     
#     if request.method == "POST":
#         title = request.POST.get("title")
#         image = request.FILES.get("image")  # ✅ CORRECTED
#         category = request.POST.get("category")
#         description = request.POST.get("description")
#         status=True
#         if request.POST.get("status")==None:
#             status= False

        
#         category_list = category_master.objects.filter(id=category).first()
#         employee.title=title
#         if image :
#           employee.image=image
#         employee.category = category_list
#         employee.status=status
#         employee.description=description

#         employee.save()
        
#         return redirect("article_page")


#     return render(request, "articales/artical-edit.html", {"articale": employee,"category":category})
       


def edit_articale(request, id):
    employee = articale_master.objects.get(id=id)
    category_list = CategoryMaster.objects.all()  # List for dropdown

    if request.method == "POST":
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category_name = request.POST.get("category")
        description = request.POST.get("description")
        status = request.POST.get("status") == "True"

        
        category_instance = CategoryMaster.objects.get(CatName=category_name)

        employee.title = title
        if image:
            employee.image = image
        employee.category = category_instance
        employee.status = status
        employee.description = description

        employee.save()
        return redirect("article_page")

    # Final render — send actual dropdown list
    return render(request, "articales/artical-edit.html", {"articale": employee, "category": category_list})


# dashboard end

# website maate

from django.shortcuts import render
from .models import CategoryMaster, articale_master

def home_page(request):
    # ✅ Category list
    category = CategoryMaster.objects.filter(CatStatus=True).order_by("CatSeqNo")

    # ✅ Latest Articles (3 recent)
    latest_articles = articale_master.objects.filter(status=True).order_by('-id')[:3]

    # ✅ Trending Articles (3 random)
    trending_articles = articale_master.objects.filter(is_trending=True, status=True).order_by('trending_order', '-created_at')[:3]
    for article in trending_articles:
        article.views = (article.views or 0) + 1
        article.save(update_fields=["views"])

    # ✅ Navbar menu items
    menu_items = NavMenu.objects.all().order_by('order')

    # featured_articles
    featured_articles = articale_master.objects.filter(is_featured=True, status=True).order_by('-created_at')[:1]

    # ✅ Trending Tags (latest 6 tags)
    trending_tags = TrendingTag.objects.all().order_by('-created_at')[:6]

    # ✅ Single return with all context
    context = {
        "category": category,
        "latest_articles": latest_articles,
        "trending_articles": trending_articles,
        "menu_items": menu_items,
        "featured_articles": featured_articles,
        "trending_tags": trending_tags,
    }

    return render(request, "web-site/home.html", context)


# feature detail 

def feature_article_detail(request, slug):
    feature_article = get_object_or_404(articale_master, slug=slug)

    # views count बढ़ाने के लिए
    feature_article.views += 1
    feature_article.save(update_fields=["views"])

    return render(request, "web-site/feature_details.html", {"article1": feature_article})

#Article detail
# def article_detail(request, slug):
#     article2 = get_object_or_404(articale_master, slug=slug)
#     context = {
#         'article2': article2
#     }
#     return render(request, 'web-site/article_detail.html', context)
# app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import articale_master, Comment, CategoryMaster
from .forms import CommentForm

def article_detail(request, slug):
    article2 = get_object_or_404(articale_master, slug=slug)
    comments = article2.comments.filter(parent__isnull=True).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'login_required'})

        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = Comment.objects.get(id=parent_id) if parent_id else None

            comment = form.save(commit=False)
            comment.article = article2
            comment.user = request.user
            comment.parent = parent
            comment.save()

            return JsonResponse({
                'success': True,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%B %d, %Y %H:%M'),
                'parent_id': parent.id if parent else None,
            })
    else:
        form = CommentForm()

    # ✅ Sidebar के लिए डेटा
    categories = CategoryMaster.objects.filter(CatStatus=True)
    recent_articles = articale_master.objects.filter(status=True).order_by('-created_at')[:5]

    context = {
        'article': article2,
        'comments': comments,
        'form': form,
        'categories': categories,          # ← सभी categories भेजी गई
        'recent_articles': recent_articles # ← हाल के 5 article भेजे गए
    }
    return render(request, 'web-site/article_detail.html', context)







def tag_detail(request, slug):
    tag = get_object_or_404(TrendingTag, slug=slug)
    articles3 = tag.articles.all()
    
    return render(request, "web-site/tag_detail.html", {"tag": tag, "articles3": articles3})


#Category Detail  maate
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import CategoryMaster, articale_master, TrendingTag

def category_detail(request, slug):
    category = get_object_or_404(CategoryMaster, CatSlug=slug)

    articles = articale_master.objects.filter(category=category, status=True).order_by("-id")

    paginator = Paginator(articles, 4)  # 6 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Sidebar data
    latest_articles = articale_master.objects.filter(status=True).order_by("-id")[:5]
    trending_articles = articale_master.objects.filter(is_trending=True, status=True).order_by("trending_order")[:5]
    trending_tags = TrendingTag.objects.all()[:15]

    return render(request, "web-site/category_detail.html", {
        "category": category,
        "articles": articles,
        "page_obj": page_obj,
        "latest_articles": latest_articles,
        "trending_articles": trending_articles,
        "trending_tags": trending_tags,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# ==========================
# Signup View
# ==========================
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "❌ Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Username already taken!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "⚠️ Email already registered!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "✅ Account created successfully! Please login now.")
            return redirect('login_user')  

    return render(request, 'web-site/signup.html')



# ==========================
# Login View
# ==========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home_page')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'web-site/login.html')


# ==========================
# Logout View
# ==========================
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('root_home')


# ==========================
# Forgot Password View
# ==========================
def forgot_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.success(request, "Password reset link sent to your email!")
            # 🔹 Real email sending can be added here
        else:
            messages.error(request, "Email not found.")
    return render(request, 'web-site/forgot_page.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='login_user')  # login_user URL पर redirect करेगा
def profile_view(request):
    user = request.user
    return render(request, 'web-site/profile.html', {'user': user})




@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'web-site/edit_profile.html', {'user': user})







from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

@login_required
def profile_view(request):
    return render(request, 'web-site/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if 'image' in request.FILES:
            profile = user.profile
            profile.image = request.FILES['image']
            profile.save()

        user.save()
        messages.success(request, "✅ Profile updated successfully!")
        return redirect('profile')

    return render(request, 'web-site/edit_profile.html')
