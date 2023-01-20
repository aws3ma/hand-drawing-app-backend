from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OriginalImage, SketchImage
from .serializer import OriginalImageSerializer, SketchImageSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
import os
from django.core.files.base import ContentFile
import numpy as np

class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # print(request.data)
        # data = request.data.copy()
        data = {}
        data["image"]=request.data["image"]
        data["user"] = request.user.id
        returnedData = {}
        serializer = OriginalImageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        id_original_image = serializer.data["id"]
        # image description : get specs of image and return tuple (width,height,channels_number,weight)
        specs = self.get_image_specs("."+serializer.data["image"])
        serializer2 = OriginalImageSerializer(
            instance=OriginalImage.objects.get(id=serializer.data["id"]),
            data=specs,
            partial=True,
            context={"request": request})
        if (serializer2.is_valid(raise_exception=True)):
            serializer2.save()
        returnedData["id"] = id_original_image
        

        # image to sketch : get sketch image,channels_number and weight
        sketch = self.img_to_sketch("."+serializer.data["image"])
        serializer = SketchImageSerializer(
            data={"image": sketch, "user": request.user.id, "original_image": id_original_image})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        specs = self.get_image_specs("."+serializer.data["image"])
        serializer2 = SketchImageSerializer(
            instance=SketchImage.objects.get(id=serializer.data["id"]),
            data=specs,
            partial=True,
            context={"request": request})
        if (serializer2.is_valid(raise_exception=True)):
            serializer2.save()
                

        return Response(data=returnedData, status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = str(request.user.id)
        original = None
        returned_data = {}
        if "original" in request.query_params.keys():
            original = request.query_params["original"]

        # return original images
        if original != None:
            # return all images
            if original == "all":
                original_images = OriginalImage.objects.filter(user_id=user_id)
                original_images_serializer = OriginalImageSerializer(
                original_images, many=True, context={"request": request})
                returned_data["original"]=original_images_serializer.data
            # return one original image
            else:
                original_image = OriginalImage.objects.get(id=original)
                hist = self.prepare_charts("."+original_image.image.url)
                original_image_serializer = OriginalImageSerializer(
                original_image, context={"request": request})
                returned_data["original"]=original_image_serializer.data
                returned_data["original"]["histogram"]=hist

                sketch_image = SketchImage.objects.get(original_image__id=original)
                hist = self.prepare_charts("."+sketch_image.image.url)
                sketch_image_serializer = SketchImageSerializer(
                sketch_image, context={"request": request})
                returned_data["sketch"]=sketch_image_serializer.data
                returned_data["sketch"]["histogram"]=hist

        return Response(data=returned_data, status=status.HTTP_200_OK)

    def get_image_specs(self, image_path):
        image = cv2.imread(image_path)
        height, width, channels_number = image.shape
        image_weight = os.stat(image_path).st_size/1024
        return {"height": height, "width": width, "channels_number": channels_number, "weight": round(image_weight, 2)}

    def img_to_sketch(self, image_path):
        # loads an image from the specified file
        image = cv2.imread(image_path)
        # convert an image from one color space to another
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(grey_img)  # helps in masking of the image
        # sharp edges in images are smoothed while minimizing too much blurring
        blur = cv2.GaussianBlur(invert, (21, 21), 0)
        invertedblur = cv2.bitwise_not(blur)
        sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
        ret, buf = cv2.imencode('.jpg', sketch)
        print(image_path[32:])
        content = ContentFile(buf.tobytes(), image_path[32:])
        return content

    def prepare_charts(self,image_path):
        image = cv2.imread(image_path)
        hist1,hist2=np.histogram(image,bins=256)
        return {"labels":np.arange(256),"data":hist1}