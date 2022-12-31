from rest_framework.serializers import ModelSerializer
from traitimage.models import OriginalImage, SketchImage


class OriginalImageSerializer(ModelSerializer):
    class Meta:
        model = OriginalImage
        fields = ('__all__')


class SketchImageSerializer(ModelSerializer):
    class Meta:
        model = SketchImage
        fields = ('__all__')
