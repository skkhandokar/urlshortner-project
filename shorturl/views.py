from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener
from .forms import ShortenerForm
from django.utils import timezone
def home_view(request):
    template = 'urlshortener/home.html'
    context = {}
    context['form'] = ShortenerForm()
    
    if request.method == 'GET':
        return render(request, template, context)
    
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
           
           long_url = used_form.cleaned_data['long_url']
        
        # Check if long_url already exists in the database
           if Shortener.objects.filter(long_url=long_url).exists():
                shortened_object = Shortener.objects.get(long_url=long_url)
            
                shortened_object.last_accessed =timezone.now() 
                shortened_object.save()
                new_url = request.build_absolute_uri('/') + shortened_object.short_url
                
                context['new_url']  = new_url
                context['long_url'] = long_url
                context['short_code'] = shortened_object.short_url
            
                return render(request, template, context)
           
           else:
                shortened_object = used_form.save()
                new_url = request.build_absolute_uri('/') + shortened_object.short_url
                long_url = shortened_object.long_url 
                context['new_url']  = new_url
                context['long_url'] = long_url
                context['short_code'] = shortened_object.short_url
                
                return render(request, template, context)
        
        context['errors'] = used_form.errors

        return render(request, template, context)
    
def redirect_url_view(request, shortened_part):
    if shortened_part == 'admin':
        return admin.site.urls
    
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
        
    except Shortener.DoesNotExist:
        raise Http404('Sorry, this link is broken :(')