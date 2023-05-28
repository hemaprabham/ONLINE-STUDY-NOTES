from django.contrib import admin
from .models import*


# Register your models here.
admin.site.register(Customer)

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
admin.site.register(Post,PostAdmin)
admin.site.register(Favorite)
admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Learning)
admin.site.register(Prerequisite)
admin.site.register(Course )
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(UserCourse )
