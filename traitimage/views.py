from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OriginalImage,SketchImage
from .serializer import OriginalImageSerializer,SketchImageSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage


class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        # image description : get specs of image and return tuple (width,height,channels_number,weight)
        # affect the results into the data dict
        serializer = OriginalImageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # image to sketch : get sketch image,channels_number and weight
        # affect results to data dict
        serializer = OriginalImageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
            
        return Response(data=images, status=status.HTTP_200_OK)

