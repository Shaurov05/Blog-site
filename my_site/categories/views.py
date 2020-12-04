from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(TemplateView,ListView,
                                DetailView, CreateView,
                                UpdateView, DeleteView,
                                RedirectView,
                                )

from . models import CategoryMember, Category
from . forms import CategoryForm
from sorl.thumbnail import  get_thumbnail
from resizeimage import resizeimage
from accounts.models import UserProfileInfo
from my_site import settings
# Create your views here.

class CreateCategory(CreateView, LoginRequiredMixin):
    fields = ("name", "description", "category_pic")
    widgets = {
            'description':{'class': 'editable medium-editor-textarea postcontent'},
        }
    # template_name = 'categories/category_form.html'
    # After creating Category it will redirect user to that category.
    model = Category


from django import template
register=template.Library()
# nested_to_flat


class SingleCategory(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.this_category = get_object_or_404(Category, category.pk==pk)
        category_picture = False

        current_category = Category.objects.filter(
            slug__iexact = self.kwargs.get("slug")
        ).get()

        if current_category.category_pic:
            category_picture = True
            picture = current_category.category_pic
            edited_picture = get_thumbnail(picture, '550x450', quality=99, format='PNG')
        else:
            profile_pic = False
            root = settings.MEDIA_ROOT
            import os
            root1 = os.path.join(root, 'profile_pics/no-image.png')
            picture = root1
            edited_picture = get_thumbnail(picture, '350x350', quality=99, format='PNG')
            # resizeimage.resize_cover(picture, [200, 100], validate=False)
            # rescale_image(picture,width=100,height=100)

        posts = []
        info = []
        continue_reading = False
        for post in current_category.posts.all():
            info.clear()
            info.append(post.user.username)
            info.append(post.pk)
            info.append(post.title)
            info.append(post.created_at)
            info.append(post.category.slug)
            info.append(post.category.name)

            if(len(post.message_html) >300 ):
                continue_reading = True
            else:
                continue_reading = False
            info.append(post.message_html[3:300])
            info.append(continue_reading)

            posts.append(info[:])

        print('\n last info \n',info[:])
        print('\n posts \n',posts[:])

        print(current_category.category_pic)
        category_info = {
            'picture':edited_picture,
            'category_picture':category_picture,
            'posts':posts
        }
        context['category_info'] = category_info
        return context


class ListCategory(ListView):
    model = Category


class JoinCategory(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("categories:single", kwargs={'slug':self.kwargs.get("slug")})

    def get(self,request, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get("slug"))

        try:
            CategoryMember.objects.create(user=self.request.user, category=category)
        except IntegrityError:
            messages.warning(self.request, ("Warning already a member of {}".format(category.name)))
        else:
            messages.success(self.request, "You are now a member of the {} Category.".format(category.name))

        return super().get(request, *args, **kwargs)


class LeaveCategory(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self,*args, **kwargs):
        return reverse("categories:single", kwargs={'slug':self.kwargs.get("slug")})

    def get(self,request, *args, **kwargs):

        try:
            membership = CategoryMember.objects.filter(
                user=self.request.user,
                category__slug = self.kwargs.get("slug")
            )
        except CategoryMember.DoesNotExist:
            messages.warning(self.request, "You can't leave as you didn't join this category.")
        else:
            membership.delete()
            messages.success(self.request, "You have left this group")

        return super().get(request,*args,**kwargs)
