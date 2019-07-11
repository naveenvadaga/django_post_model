from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Person, UserAdmin)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(React)
