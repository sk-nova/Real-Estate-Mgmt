from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "user", "gender", "occupation", "slug"]
    list_display_links = ["pkid", "user"]
    list_filter = ["occupation"]