from django.contrib import admin
from .models import Tip, Vote

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'date', 'upvote_count', 'downvote_count')
    search_fields = ('author__username', 'content')
    list_filter = ('date',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tip', 'user', 'value')
    search_fields = ('tip__content', 'user__username')
    list_filter = ('value',)