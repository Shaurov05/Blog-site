from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='',blank=True)
    members = models.ManyToManyField(User, through="CategoryMember")
    category_pic = models.ImageField(upload_to = 'category_pics', blank=True)

    def __str__(self):
        return self.name

    # WE are saving the model. But before that we are converting
    # the name using slugify and description using misaka.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    #get_absolute_url is used because it tell the template
    # CreateView to go to the page it is directing.
    # for this example it is directing to go to single page of a category.
    def get_absolute_url(self):
        return reverse("categories:single", kwargs={"slug":self.slug})

    class Meta:
        ordering = ['name']


class CategoryMember(models.Model):
    category = models.ForeignKey(Category, related_name = "memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_categories", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together= ("category", "user")
