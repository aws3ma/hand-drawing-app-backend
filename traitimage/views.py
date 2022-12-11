from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Images
from .serializer import ImagesSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage


class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data
        data = data.copy()
        data["user"] = request.user.id
        # image to sketch : save image to server and return the name of the file
        # image description : get specs of image and return tuple (width,height,channels_number,weight)
        serializer = ImagesSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = str(request.user.id)
        id = "0"
        if "id" in request.query_params.keys():
            id = request.query_params["id"]
        # return all images
        if id == "0":
            images = Images.objects.filter(user_id=user_id)
        # return one image
        if id != "0":
            images = Images.objects.filter(id=id)
            # create data of the hist (TP2 II:1) {labels:[],data:[]}
            # create data of the second hist (TP2 II:2) {labels:[],datasets:{ds1:{data:[],color:"red"},ds2:{data:[],color:"green"}}}
        images = ImagesSerializer(
            images, many=True, context={"request": request})
        return Response(data=images, status=status.HTTP_200_OK)

    def save_image(image):
        fs = FileSystemStorage()
        path = fs.save(image.name, image)
        path = '.'+fs.url(path)
