from django.contrib import admin
from .models import *
from django.utils.html import format_html 
from django.urls import path

# Register your models here.


admin.site.register(Voter)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'bio')  # Add 'display_image' to list_display
    readonly_fields = ('image_preview',)  # Add 'image_preview' to readonly_fields

    def display_image(self, obj):
        if obj.imageURL:  # Use the imageURL property
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit:cover;" />', obj.imageURL)
        return "No Image"

    def image_preview(self, obj):
        if obj.imageURL:  # Use the imageURL property
            return format_html('<img src="{}" width="150" height="150" style="border-radius: 10px; object-fit:cover;" />', obj.imageURL)
        return "No Image"

    display_image.short_description = 'Image'  # Column header for list view
    image_preview.short_description = 'Image Preview'  # Field label for detail view

# Register the Candidate model with the custom admin class
admin.site.register(Candidate, CandidateAdmin)
    
    

admin.site.register(Position)
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'position', 'candidate')
    list_filter = ('position', 'candidate')
    search_fields = ('voter__admin__email', 'position__name', 'candidate__name')
