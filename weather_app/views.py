from distutils.log import error
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
import requests
from requests.adapters import HTTPAdapter
from . models import City
from . forms import CityForm, CityUpdateForm
# Create your views here.

def CityWeatherView(request):
    # the open weathermap api
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=278de88460b27cf7d073de2541ab61f8"
    
    errmsg = ""
    msgclass = ''
    msg = ""
    if request.method=='POST':
        # here the form will save the create post
        form = CityForm(request.POST)
        if form.is_valid():
            # cleaned data returns a dictionary of validated form input fields and their values
            new_city= form.cleaned_data['name']
            # here the name of the city is counted. if it's more than 0 then city name will not be 
            # saved
            city_count = City.objects.filter(name=new_city).count()
            if city_count==0:
                # here the url data will be json formatted
                r = requests.get(url.format(new_city)).json()
                # in the api the existing cities have a code of 200
                # that's why it's checked in here
                if r['cod']==200:
                    form.save()
                else:
                    errmsg ="This city does not exist"
            else:
                errmsg ="This city is already in the database"
        # these error messages will be exported to the template to show both successful and error
        # message
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg= "This city is successfully added in database"
            msgclass = 'is-success'      
    form = CityForm()
    weather = []
    city = City.objects.all()
    for p in city:
        r = requests.get(url.format(p)).json()
        # print(r)
        # here json data is being parsed to the variables set below
        city_weather = {
            'city':p,
            'temperature':r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        # weather is an array where json data is being appended
        weather.append(city_weather)
        # print(weather)
    # context for sending it to the template
    context = {
        'weather': weather,
        'form': form,
        'msg': msg,
        'msgclass': msgclass
        
    }
    return render(request, 'weather_app/home.html', context) 


def City_delete(request, city_name):
    # get_object_or_404 is used to check if the object is available in model or not
    city= get_object_or_404(City,name=city_name)
    city.delete()
    return redirect('City_Weather')

def City_update(request, city_name):
    # first the single city_data is being selected
    city_data = City.objects.get(name=city_name)
    # form = CityUpdateForm(instance=city_data)
    # i =0
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=278de88460b27cf7d073de2541ab61f8"
    errmsg = ""
    msgclass = ''
    msg = ""
    if request.method=='POST':
        # i =1
        # then the input data is stored here
        new_city_data = request.POST.get('city')
        # form = CityUpdateForm(instance=city)
        
        # i =2
        new_city= new_city_data
        city_count = City.objects.filter(name=new_city).count()
        if city_count==0:
            r = requests.get(url.format(new_city)).json()
            if r['cod']==200:
                city_data.name = request.POST.get('city')
                city_data.save()
                return redirect('City_Weather')
            else:
                errmsg ="This city does not exist"
        else:
            errmsg ="This city is already in the database"
        
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg= "This city is successfully updated in database"
            msgclass = 'is-success' 

    weather = []
    # print(i)
    r = requests.get(url.format(city_data)).json()
     # print(r)
    city_weather = {
        'city':city_data,
        'temperature':r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    weather.append(city_weather)
        
    # print(weather)
    context = {
        'weather': weather,
        'msg': msg,
        'msgclass': msgclass,
        
    }
    return render(request, 'weather_app/update_city.html', context)