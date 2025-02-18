from django.contrib import admin

# Register your models here.

from media_app.models import MediaFile

admin.site.register(MediaFile)