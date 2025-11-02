"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import*
from myapp.models import*
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from myapp.views import *

from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
   
    # dashboard maate
    path('login/',login,name="login"),
    path('dashboard/', dashboard, name='dashboard'),
    path('category_page/',category_page,name="category_list"),
    path("category_page/category_create/",category_create,name="category_create"),
    path('delete_category/<id>/',delete_category,name="delete_category"),
    path('category_page/update_category/<id>/',update_category,name="update_category"),
    path('article_page/', article_page, name='article_page'),
    path('articale_create/',articale_create,name="article_form"),
    path('article_category/',article_category),
    path('delete_articale/<id>/',delete_articale,name="delete_articale"),
    path('edit_articale/<id>/',edit_articale,name="edit_articale"),
    path('logout/',logout),
    
    path('', views.home_page, name='root_home'),
    path("home_page/", home_page, name="home_page"),
    path('featured/<slug:slug>/', feature_article_detail, name='feature_article_detail'),
    path("latest_article/<slug:slug>/", article_detail, name="article_detail"),
    path("trending_now/<slug:slug>/", tag_detail, name="tag_detail"),
    path("category/<slug:slug>/", category_detail, name="category_detail"),
    
    path('login_view/', login_view, name='login_user'),
    path('signup_view/', signup_view, name='register_user'),
    path('forgot_view/', forgot_view, name='forgot_password'),
    path('logout_view/', logout_view, name='logout_user'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile')

    
    

    # dashboard end  
    
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
