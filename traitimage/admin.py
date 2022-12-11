from django.contrib import admin

from .models import Images

# Register your models here.
class ImagesAdmin(admin.AdminSite):
    site_header: str="images"
    site_title: str="images manager"
    site_url: str="images"

images_admin = ImagesAdmin(name="imagesadmin")
admin.site.register(Images)
