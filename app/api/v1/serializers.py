from rest_framework import serializers
from app.models import Music
from users.models import User, Producer
# added absolute_url 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class ProducerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Producer
        fields = ["category", "played_time", "website", "rating", "user"]
        
    

class MusicSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
            read_only=True,
            slug_field="name"
        )
    absolute_url = serializers.SerializerMethodField()
    producer = ProducerSerializer(read_only=True)
    class Meta:
        model = Music
        fields = ["id", "name", "category", "file", "producer", "absolute_url"]
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        relative_url = obj.get_absolute_api_url()
        return request.build_absolute_uri(relative_url)