from django.contrib import admin

from account.models import User, FriendshipRequest


admin.site.register(User)
admin.site.register(FriendshipRequest)
