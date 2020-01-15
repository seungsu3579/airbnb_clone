from django.shortcuts import render, redirect

# from django.urls import reverse
# from django.http import Http404
# from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage
from django_countries import countries
from django.views.generic import ListView, DetailView
from . import models


# Create your views here.


# def all_rooms(request):
# return render(request, template, content=, ...) >> 이것또한 HttpResponse를 제공
# return HttpResponse(content=f"<h1>Time is {now}</h1>")

"""
    page = int(request.GET.get("page", 1))
    page = int(page or 1)
    page_size = 10
    limit = page * page_size
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.all().count() / page_size)
    return render(
        request,
        "rooms/all_rooms.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )



    page = int(request.GET.get("page", 1))
    rooms_list = models.Room.objects.all()
    paginator = Paginator(rooms_list, 10)
    try:
        rooms = paginator.page(page)
        return render(request, "rooms/all_rooms.html", context={"page": rooms})
    except EmptyPage:
        rooms = paginator.page(1)
        return redirect("/")        #home
"""


class HomeView(ListView):

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


# functional method
"""
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/details.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
"""

# class method
class RoomDetail(DetailView):
    model = models.Room
    template_name = "rooms/details.html"


def search(request):
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    priceL = int(request.GET.get("priceL", 0))
    priceH = int(request.GET.get("priceH", 10000000))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "s_city": city,
        "s_country": country,
        "s_room_type": room_type,
        "s_priceL": priceL,
        "s_priceH": priceH,
        "s_guests": guests,
        "s_bedrooms": bedrooms,
        "s_beds": beds,
        "s_baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    rooms = models.Room.objects.filter()

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country__exact"] = country

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type

    filter_args["price__range"] = (priceL, priceH)

    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant:
        filter_args["instant_book__exact"] = True

    if superhost:
        filter_args["host__superhost__exact"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    rooms = rooms.filter(**filter_args)

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms}
    )
