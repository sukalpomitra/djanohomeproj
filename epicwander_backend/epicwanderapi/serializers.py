from rest_framework import serializers
from models import User
from models import Photo
# Create your views here.

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		field = ('id', 'facebook_id', 'first_name', 'last_name', 'email', 'access_token')

'''		
class ImageSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Photo
        field = ('id', 'image', 'owner' )
'''
		
class PhotoSerializer(serializers.HyperlinkedModelSerializer):
	owner = UserSerializer(read_only = True)
	image = serializers.ImageField(max_length=None, use_url=True)
	class Meta:
		model = Photo
        field = ('id', 'image', 'owner')
        read_only_fields = ('owner')