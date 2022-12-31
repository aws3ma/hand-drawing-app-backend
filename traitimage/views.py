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


class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        # image description : get specs of image and return tuple (width,height,channels_number,weight)
        serializer = OriginalImageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        id_original_image = serializer.data["id"]
        specs = self.get_image_specs("."+serializer.data["image"])
        serializer2 = OriginalImageSerializer(
            instance=OriginalImage.objects.get(id=serializer.data["id"]), 
            data=specs, 
            partial=True)
        if (serializer2.is_valid(raise_exception=True)):
            serializer2.save()

        # image to sketch : get sketch image,channels_number and weight
        sketch = self.img_to_sketch("."+serializer.data["image"])
        serializer = SketchImageSerializer(data={"image":sketch,"user":request.user.id,"original_image":id_original_image})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        specs = self.get_image_specs("."+serializer.data["image"])
        serializer2 = SketchImageSerializer(
            instance=SketchImage.objects.get(id=serializer.data["id"]), 
            data=specs, 
            partial=True)
        if (serializer2.is_valid(raise_exception=True)):
            serializer2.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = str(request.user.id)
        original = None
        sketch = None
        if "original" in request.query_params.keys():
            original = request.query_params["original"]
        if "sketch" in request.query_params.keys():
            sketch = request.query_params["sketch"]

        # return original images
        if original != None:
            # return all original images
            if original == "all":
                images = OriginalImage.objects.filter(user_id=user_id)
            # return one original image
            else:
                images = OriginalImage.objects.filter(id=original)
                # create data of the hist (TP2 II:1) {labels:[],data:[]}
                # create data of the second hist (TP2 II:2) {labels:[],datasets:{ds1:{data:[],color:"red"},ds2:{data:[],color:"green"}}}

            images = OriginalImageSerializer(
                images, many=True, context={"request": request})
            print(images.data)
        # return sketch images
        if sketch != None:
            # return all sketch images
            if sketch == "all":
                images = SketchImage.objects.filter(user_id=user_id)
            # return one sketch image
            else:
                images = SketchImage.objects.filter(id=sketch)
                # create data of the hist (TP2 II:1) {labels:[],data:[]}
                # create data of the second hist (TP2 II:2) {labels:[],datasets:{ds1:{data:[],color:"red"},ds2:{data:[],color:"green"}}}

            images = SketchImageSerializer(
                images, many=True, context={"request": request})
        # return one image

        return Response(data=images.data, status=status.HTTP_200_OK)

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
        content = ContentFile(buf.tobytes(),image_path[32:])
        return content
