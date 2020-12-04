from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from categories.models import Category
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, related_name="user_of_post_model", on_delete=models.CASCADE)
    created_at =  models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    category = models.ForeignKey(Category, related_name="posts",on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username":self.user.username, "pk":self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'message')


class Comment(models.Model):
    post = models.ForeignKey('posts.Post',on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approve_comment = models.BooleanField(default=False)

    def approve(self):
        self.approve_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("all")

    def __str__(self):
        return self.text
