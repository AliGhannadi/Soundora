from rest_framework import serializers
from app.models import Music
from users.models import User, Artist
from app.models import Category
# added absolute_url 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.SlugRelatedField(
            read_only=True,
            slug_field="name"
        )
    class Meta:
        model = Artist
        fields = ["category", "played_time", "website", "rating", "user"]
        
    

class MusicListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Music
        fields = ["title", "category", "artist",  "cover_image", "file", "absolute_url"]
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        relative_url = obj.get_absolute_api_url()
        return request.build_absolute_uri(relative_url)
    

class MusicDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    class Meta:
        model = Music
        fields = ["title", "category", "artist", "lyrics", "cover_image", "uploaded_at", "file"]