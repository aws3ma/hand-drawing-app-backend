from django.contrib import admin

from .models import OriginalImage, SketchImage

# Register your models here.


class OriginalImageAdmin(admin.AdminSite):
    site_header: str = "original images"
    site_title: str = "original images manager"
    site_url: str = "original images"


images_admin = OriginalImageAdmin(name="original_images_admin")
admin.site.register(OriginalImage)


class SketchImageAdmin(admin.AdminSite):
    site_header: str = "sketch images"
    site_title: str = "sketch images manager"
    site_url: str = "sketch images"


images_admin = SketchImageAdmin(name="sketch_images_admin")
admin.site.register(SketchImage)
