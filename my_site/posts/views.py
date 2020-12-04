from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
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
from braces.views import SelectRelatedMixin

from . forms import PostForm, CommentForm
from . models import Post, Comment
from categories import models

from sorl.thumbnail import  get_thumbnail
from resizeimage import resizeimage
from accounts.models import UserProfileInfo
from my_site import settings
from django.contrib.auth.models import User
# Create your views here.

class CreatePost(LoginRequiredMixin, CreateView):
    redirect_field_name = 'posts/post_detail.html'
    form_class = PostForm
    model = Post
    import misaka

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            all_members = models.CategoryMember.objects.filter(
                user=self.request.user,
                category__slug=self.object.category.slug).get()
        except models.CategoryMember.DoesNotExist:
            self.warning="Join the category first!"
            return redirect("categories:single",self.object.category.slug)
        else:
            print('1 username %s post_pk %s' % (self.request.user.username, self.object.pk))
            self.object.user=self.request.user
            print('2 username %s post_pk %s' % (self.request.user.username, self.object.pk))
            self.object.save()
            print('3 username %s post_pk %s' % (self.request.user.username, self.object.pk))
            return super().form_valid(form)


def post_detail(request, username, pk):
    post = get_object_or_404(Post, pk=pk)
    new_comment = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create Comment object but don't save to database yet
            comment = form.save(commit=False)
            # Assign the current post to the comment
            comment.post = post
            # Save the comment to the database
            comment.save()
            new_comment = True

            if new_comment == True:
                form = CommentForm()
            return render(request, 'posts/post_detail.html', {'post':post,
                                                        'new_comment':new_comment,
                                                             'comment_form':form})
    if request.method != 'POST':
        form = CommentForm()
        new_comment = False
        # request.session['new_comment'] = "False"
    return render(request, 'posts/post_detail.html', {'post':post,
                                                'new_comment':new_comment,
                                                     'comment_form':form})


class PostList(ListView, SelectRelatedMixin):
    model = Post
    select_related = ("user", "category")



from django.contrib.auth.models import User
from categories.models import CategoryMember, Category
class UserPosts(ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("user_of_post_model").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.user_of_post_model.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = UserProfileInfo.objects.filter(
            user__id__iexact = self.post_user.id
        ).get()

        post_of_user = self.post_user.user_of_post_model.all()
        single_post = []

        for post in post_of_user:
            single_post.clear()
            single_post.append(str(post))

        single_post = post_of_user[0]
        print('first 2 posts\n',str(single_post)[3:10])

        user_categories= []
        category_list = []
        single_list = []

        for member in CategoryMember.objects.all():
            if member.user == self.post_user:
                category_list.clear()
                category_list.append(member.category.name)
                category_list.append(member.category.slug)

                user_categories.append(category_list[:])
            else:
                print('not found')

        print('user categories\n',user_categories)

        if current_user.profile_pic:
            profile_pic = True
            picture = current_user.profile_pic
            edited_picture = get_thumbnail(picture, '350x350', quality=99, format='PNG')
        else:
            profile_pic = False
            root = settings.MEDIA_ROOT
            import os
            root1 = os.path.join(root, 'profile_pics/no-image.png')
            picture = root1
            edited_picture = get_thumbnail(picture, '350x350', quality=99, format='PNG')
            # resizeimage.resize_cover(picture, [200, 100], validate=False)
            # rescale_image(picture,width=100,height=100)

        user_info = {
            'current_user':current_user,
            'user_categories':user_categories,
            'edited_picture':edited_picture,
            'profile_pic':profile_pic,
            'post_user':self.post_user,
        }
        user_info_list = [
            current_user, user_categories, edited_picture,
            profile_pic, self.post_user, self.post_user.username,
            self.post_user.first_name, self.post_user.last_name,
            self.post_user.email, self.post_user,
        ]
        # print(user_info)
        context['user_info_list'] = user_info_list
        return context

# class PostDetail(SelectRelatedMixin, DetailView):
#     model = Post
#     select_related = ("user", "category")
#
#     def get_queryset(self):
#         query_set = super().get_queryset()
#         return query_set.filter(
#             user__username__iexact=self.kwargs.get("username")
#         )


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = Post
    select_related = ("user", "category")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        return queryset.filter(user_id=user_id)

    def delete(self,*args,**kwargs):
        messages.success(self.request, "Post is deleted!")
        return super().delete(*args,**kwargs)


# def add_comment_to_post(request,username, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('posts:single', username=post.user.username, pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'posts/post_detail.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('posts:single', username=comment.post.user.username, pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    post = comment.post
    comment.delete()
    return redirect('posts:single',username=post.user.username, pk=post.pk)
