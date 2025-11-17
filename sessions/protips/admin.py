from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tip, Vote, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_reputation', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    
    def get_reputation(self, obj):
        return obj.get_reputation()
    get_reputation.short_description = 'Reputation'


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'author_reputation', 'date', 'upvote_count', 'downvote_count')
    search_fields = ('author__username', 'content')
    list_filter = ('date',)

    def author_reputation(self, obj):
        return obj.author.get_reputation()
    author_reputation.short_description = 'Author Rep'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tip', 'user', 'user_reputation', 'value')
    search_fields = ('tip__content', 'user__username')
    list_filter = ('value',)

    def user_reputation(self, obj):
        return obj.user.get_reputation()
    user_reputation.short_description = 'Voter Rep'