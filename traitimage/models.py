from django.db import models
from django.contrib.auth.models import User


def original_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'static/images/user_{}/original/{}'.format(instance.user.id, filename)


def sketch_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'static/images/user_{}/sketch/{}'.format(instance.user.id, filename)


class OriginalImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=original_directory_path)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    channels_number = models.PositiveBigIntegerField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return self.image.name


class SketchImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ForeignKey(OriginalImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=sketch_directory_path)
    weight = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    channels_number = models.PositiveBigIntegerField(null=True)

    # def __str__(self) -> str:
    #     return self.image.name
