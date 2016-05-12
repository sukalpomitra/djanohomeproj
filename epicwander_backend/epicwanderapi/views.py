from django.shortcuts import render
from django.http import Http404

from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrIsSelf
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route, parser_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from serializers import UserSerializer
from serializers import PhotoSerializer
from models import User
from models import Photo
# Create your views here.


class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	'''
	def perform_create(self, serializer):
		queryset = User.objects.filter(email=self.request.data['email'])
		if queryset.exists():
			raise ValidationError("Id exists " + str(queryset[0].id))
		serializer.save()
	'''
		
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
		
class PhotoViewSet(RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAdminOrIsSelf,)

    def __init__(self, *args, **kwargs):
        super(PhotoViewSet, self).__init__(*args, **kwargs)

	@detail_route(methods=['POST'], permission_classes=[IsAdminOrIsSelf])
	@parser_classes((FormParser, MultiPartParser,))
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'upload' in request.data:
            user_photo = self.get_object()
            user_photo.image.delete()

            upload = request.data['upload']

            user_photo.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_photo.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
			
class PhotoMultiPartParserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAdminOrIsSelf,)

    def __init__(self, *args, **kwargs):
        super(PhotoMultiPartParserViewSet, self).__init__(*args, **kwargs)

    @parser_classes((MultiPartParser,))
    def update(self, request, *args, **kwargs):
        if 'upload' in request.data:
            user_photo = self.get_object()

            user_photo.image.delete()

            upload = request.data['upload']

            user_photo.image.save(upload.name, upload)

        return super(PhotoMultiPartParserViewSet, self).update(request, *args, **kwargs)
