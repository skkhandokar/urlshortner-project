from rest_framework import serializers
from .models import Shortener

class ShortenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortener
        fields = ['id', 'long_url', 'short_url', 'created','last_accessed',"times_followed"]
        read_only_fields = ['short_url']                                       
