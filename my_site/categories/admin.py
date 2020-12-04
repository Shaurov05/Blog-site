from django.contrib import admin

from . import models
# Register your models here.
class CategoryMemberInline(admin.TabularInline):
    model = models.CategoryMember

admin.site.register(models.Category)
