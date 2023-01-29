import random
from collections import Counter

import folium
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg

from .models import CorruptionData, Category


def show_fairmap(request):
    data = CorruptionData.objects.values('latitude', 'longitude').annotate(count=Count('id'))

    # Get the average latitude and longitude of the data
    latitude = data.aggregate(Avg('latitude'))['latitude__avg']
    longitude = data.aggregate(Avg('longitude'))['longitude__avg']

    # Create a map centered on the mean coordinates of the data
    map = folium.Map(
        location=[latitude, longitude], 
        zoom_start=12,
    )

    # Add a marker for each data point
    for row in data:
        if row['count'] >= 10:
            color = 'red'
        elif row['count'] >= 5:
            color = 'orange'
        else:
            color = 'blue'

        data_ = CorruptionData.objects.filter(latitude=row['latitude'], longitude=row['longitude']).first()

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=data_.location_name + '<br><br>' + 'Corruption cases: ' + str(row['count']) + '<br><br>' +f'<a href="{reverse("location_detail", args=[row["latitude"],row["longitude"]])}">Read Comments</a>',
            icon=folium.Icon(color=color),
        ).add_to(map)

    # Save the map to an HTML file
    map.save("templates/app/fairmap.html")

    return render(request, 'app/fairmap.html')


def get_location_detail(request, latitude, longitude):
    latitude=float(latitude)
    longitude=float(longitude)

    location_info = CorruptionData.objects.filter(latitude=latitude, longitude=longitude).first()
    location_data = CorruptionData.objects.filter(latitude=latitude, longitude=longitude)
    
    context = {
        'location_data': location_data,
        'category': location_info.category,
        'location_name': location_info.location_name,
        'latitude': latitude,
        'longitude': longitude,
    }
    
    return render(request, 'app/location_detail.html', context)


def ranking(request):
    ranking = CorruptionData.objects.values('latitude', 'longitude').annotate(count=Count('id')).order_by('-count')

    ranking_list = []
    for rank in ranking:
        data = CorruptionData.objects.filter(latitude=rank['latitude'], longitude=rank['longitude']).first()
        ranking_list.append(
            {
                'latitude': data.latitude,
                'longitude': data.longitude,
                "location_name": data.location_name,
                "category": data.category,
                'count': rank['count'],
            }
        )
    
    context = {
        'ranking': ranking_list,
        'section': 'ranking',
    }
    return render(request, 'app/ranking.html', context)


def survey(request):
    if request.method == "POST":
        latitude = round(float(request.POST.get('latitude')), 6)
        longitude = round(float(request.POST.get('longitude')), 6)
        location_name = request.POST.get('location_name')
        category = request.POST.get('category')
        comment = request.POST.get('comment')
        
        category = Category.objects.filter(id=int(category)).first()

        if latitude and longitude and location_name and category and comment:
            CorruptionData.objects.create(
                latitude=latitude, 
                longitude=longitude, 
                location_name=location_name, 
                category=category, 
                comment=comment
            )
            return redirect('show_fairmap')

        return HttpResponse("Please fill the form correctly")
    
    context = {
        'category': Category.objects.all()
    }
    return render(request, 'app/survey.html', context)


def index(request):
    context = {
        'section': 'index',
    }
    return render(request, 'app/index.html', context)

def about(request):
    context = {
        'section': 'about',
    }
    return render(request, 'app/about.html', context)


def open_data(request):
    data_list = []
    for data in CorruptionData.objects.all():
        data_list.append({
            "latitude": data.latitude, 
            "longitude": data.longitude, 
            "location_name": data.location_name, 
            "category": data.category.name, 
            "comment": data.comment,
            "created_at": data.created_at,
        })

    return JsonResponse(data_list, status=200, safe=False)
