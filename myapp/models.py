
from django.db import models

# Create your models here.






# caregory maate
class CategoryMaster(models.Model):
    CatName = models.CharField(max_length=100, unique=True)
    CatSeqNo = models.IntegerField()
    CatSlug = models.SlugField(unique=True, blank=True, null=True)  # ✅ SlugField use karo
    CatStatus = models.BooleanField(default=True)
    CatImage = models.ImageField(upload_to='category/')

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.CatSlug:
            base_slug = slugify(self.CatName)
            slug = base_slug
            counter = 1
            while CategoryMaster.objects.filter(CatSlug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.CatSlug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.CatName



    # def __str__(self):
    #     return self.CatName   # अब id की जगह हमेशा नाम दिखेगा

    
#trending

from django.db import models
from django.utils.text import slugify
import uuid

class TrendingTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            # पहले name से slug बनाओ
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # अगर slug पहले से exist करता है तो unique बनाने के लिए number जोड़ो
            while TrendingTag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



from django.contrib.auth.models import User
# aricale mate
class articale_master(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)   # ✅ Slug added
    image = models.ImageField(upload_to="image/")
    status = models.BooleanField(default=True)
    description = models.TextField(max_length=10000)
    category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(TrendingTag, related_name='articles')
    is_trending = models.BooleanField(default=False)                # mark an article as trending
    trending_order = models.PositiveIntegerField(default=0) 
    highlight = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while articale_master.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(articale_master, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Add this line for replies (parent comment)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        ordering = ['-created_at']  # latest first

    def __str__(self):
        return f"{self.user.username} on {self.article.title}"



# header dynamic

# models.py
class HeaderSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Article Hub")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)

    def __str__(self):
        return self.site_name


class NavMenu(models.Model):
    name = models.CharField(max_length=50)       # e.g. "Featured"
    link = models.CharField(max_length=100)      # e.g. "#featured"
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/user1.jpg')

    def __str__(self):
        return self.user.username


class MyUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

