from rest_framework import serializers
from app.models import Music
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ["id", "name", "file", "category", "producer"]
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        # if request.parser_context.get("kwargs").get("pk"):
        #     rep.pop("id", None)