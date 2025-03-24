import pandas as pd
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Address, Hotel
from .helpers.recommendation import persist_to_db


class ListHotelsView(ListView):
    queryset = Hotel.objects.filter(score__isnull=False).all().order_by("-star_rating")
    template_name = "hotels/index.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(ListHotelsView, self).get_context_data(**kwargs)
        p = Paginator(self.queryset, self.paginate_by)
        context["hotels_list"] = p.page(context["page_obj"].number)
        context["locality"] = set([hotel.address.locality for hotel in self.queryset])
        return context


class SingleHotelsView(DetailView):
    template_name = "hotels/hotel-detail.html"

    def get(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        context = {"hotel": hotel, "ratings": range(hotel.rounded_rating), "num_ratings": range(5 - hotel.rounded_rating)}
        return render(request, self.template_name, context)


class RecommendationView(View):

    template_name = "hotels/hotel-recommendation.html"

    def post(self, request):
        locality = request.POST.get("locality", "")
        price_range = request.POST.get("price_range", []).split(",")

        items = Hotel.objects.filter(
            price__gte=int(price_range[0]),
            price__lte=int(price_range[1]),
            address__locality=locality,
            score__isnull=False,
        ).order_by("score")[::-1]
        data = items[:10]

        context = {}
        context["hotels_list"] = data
        context["min_price"] = price_range[0]
        context["max_price"] = price_range[1]
        context["local"] = locality

        context["locality"] = set(
            [
                hotel.address.locality
                for hotel in Hotel.objects.filter(score__isnull=False).all()
            ]
        )
        return render(request, self.template_name, context)
