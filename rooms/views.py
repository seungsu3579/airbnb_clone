from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

# from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from . import models

# from django.http import HttpResponse

# Create your views here.


def all_rooms(request):
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


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/details.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
