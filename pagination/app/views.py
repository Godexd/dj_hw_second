from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


list_bus_stops = []
with open(BUS_STATION_CSV, newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        dict_one_bus_stop = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District'] }
        list_bus_stops.append(dict_one_bus_stop)


def bus_stations(request):
    elements_per_page = 10
    paginator = Paginator(list_bus_stops, elements_per_page)
    current_page = request.GET.get('page', 1)
    page_obj = paginator.get_page(current_page)
    prev_page, next_page = None, None
    if page_obj.has_previous():
        prev_page = '?'.join([reverse(bus_stations), urlencode({'page': page_obj.previous_page_number()})])
    if page_obj.has_next():
        next_page = '?'.join([reverse(bus_stations), urlencode({'page': page_obj.next_page_number()})])
    context = {
        'bus_stations': page_obj.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page,
        'next_page_url': next_page,
    }
    return render(request, 'index.html', context=context)
