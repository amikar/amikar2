from django.contrib import admin

# Register your models here.


from django.contrib import admin
from website.models import Category, Page
from website.models import UserProfile

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name')}

 #admin.site.register(Category,CategoryAdmin)


admin.site.register(UserProfile)