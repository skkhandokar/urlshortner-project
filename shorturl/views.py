from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from .models import Shortener
from .serializers import ShortenerSerializer
from django.contrib import admin


class URLShortenerView(APIView):
    def get(self, request, format=None):
        # Return empty serializer to provide the structure
        serializer = ShortenerSerializer()
        return Response({'form': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ShortenerSerializer(data=request.data)

        if serializer.is_valid():
            long_url = serializer.validated_data['long_url']

            # Check if long_url already exists in the database
            if Shortener.objects.filter(long_url=long_url).exists():
                shortened_object = Shortener.objects.get(long_url=long_url)
                shortened_object.last_accessed = timezone.now()
                shortened_object.save()

                new_url = request.build_absolute_uri('/') + shortened_object.short_url
                return Response({
                    'new_url': new_url,
                    'long_url': long_url,
                    'short_code': shortened_object.short_url
                }, status=status.HTTP_200_OK)

            # If long_url doesn't exist, create a new short URL
            else:
                shortened_object = serializer.save()
                new_url = request.build_absolute_uri('/') + shortened_object.short_url
                return Response({
                    'new_url': new_url,
                    'long_url': shortened_object.long_url,
                    'short_code': shortened_object.short_url
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class URLRedirectView(APIView):
    def get(self, request, shortened_part, format=None):
        if shortened_part == 'admin':
            return HttpResponseRedirect(admin.site.urls)

        try:
            shortener = Shortener.objects.get(short_url=shortened_part)
            shortener.times_followed += 1
            shortener.save()

            return HttpResponseRedirect(shortener.long_url)

        except Shortener.DoesNotExist:
            raise Http404('Sorry, this link is broken :(')
