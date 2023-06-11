from django.contrib import admin
from .models import Posts, Comments, Follower, Following

admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Following)
admin.site.register(Follower)