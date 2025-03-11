from django.contrib import admin
from .models import *
from django.urls import path

# Register your models here.


admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Position)
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'position', 'candidate')
    list_filter = ('position', 'candidate')
    search_fields = ('voter__admin__email', 'position__name', 'candidate__name')
