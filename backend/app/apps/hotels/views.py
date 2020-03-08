import pandas as pd
import requests
from datetime import datetime
import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View

from ..authentication.models import User
from .helpers.recommendation import persist_to_db
from .models import Address, Hotel


class ListHotelsView(ListView):
    queryset = Hotel.objects.filter(
        score__isnull=False).all().order_by('-star_rating')
    template_name = 'hotels/index.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(ListHotelsView, self).get_context_data(**kwargs)
        p = Paginator(self.queryset, self.paginate_by)
        context['hotels_list'] = p.page(context['page_obj'].number)
        context['locality'] = set(
            [hotel.address.locality for hotel in self.queryset])
        return context


class SingleHotelsView(DetailView):
    template_name = 'hotels/hotel-detail.html'

    def get(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        hotel.views = hotel.views+1 if hotel.views else 1
        hotel.save()
        context = {'hotel': hotel}
        return render(request, self.template_name, context)


class Dashboard(DetailView):
    template_name = 'hotels/dashboard.html'

    def get(self, request):
        # hotel = get_object_or_404(Hotel, id=hotel_id)
        weather = requests.get(
            "http://api.weatherapi.com/v1/current.json?key=77e334f55f184f91afc144327201409&q=Nairobi")
        res = json.loads(weather.content)
        total_hotels = Hotel.objects.all().count()
        users = User.objects.filter(deleted=False).count()
        views = Hotel.objects.aggregate(Sum('views'))
        reviews = Hotel.objects.aggregate(Sum('total_reviews'))
        # import pdb; pdb.set_trace()
        weather = {
            "time": datetime.now().strftime("%c"),
            'wind': res['current']['wind_kph'],
            "icon": res['current']['condition']['icon'].replace("//", 'http://'),
            "humidity": res['current']['humidity'],
            "pressure": res['current']['pressure_in'],
            "temperature": res['current']['temp_c'],
            "uv":res['current']['uv']
        }

        regions = Address.objects.values('locality').distinct().count()
        context = {'hotels': total_hotels, "users": users,
                   'regions': regions, 'views': views, 'reviews': reviews, 'weather': weather}
        return render(request, self.template_name, context)


class AddHotel(DetailView):
    template_name = 'hotels/hotel-add.html'

    def get(self, request):
        # hotel = get_object_or_404(Hotel, id=hotel_id)
        context = {'hotel': "hotel"}
        return render(request, self.template_name, context)


class RecommendationView(View):

    template_name = 'hotels/hotel-recommendation.html'

    def post(self, request):
        locality = request.POST.get("locality", '')
        price_range = request.POST.get("price_range", []).split(',')

        items = Hotel.objects.filter(
            price__gte=int(price_range[0]),
            price__lte=int(price_range[1]),
            address__locality=locality,
            score__isnull=False).order_by('score', 'price')
        # price_gt = f"price >= {int(price_range[0])}"
        # price_lt = f"price <= {int(price_range[1])}"
        # locality = f"address__locality = {locality}"
        # score = "score is not null"
        # qs = Hotel.objects.extra(where=[
        #     price_gt, price_lt, score, locality
        # ])
        # items = qs.extra(order_by=['score', 'price'])
        # q = q.extra(order_by = ['-is_top'])
        # import pdb; pdb.set_trace()
        data = items[:10]

        context = {}
        context['hotels_list'] = data
        context['min_price'] = price_range[0]
        context['max_price'] = price_range[1]
        context['local'] = locality

        context['locality'] = set(
            [hotel.address.locality for hotel in Hotel.objects.filter(
                score__isnull=False).all()])
        return render(request, self.template_name, context)

    def get(self, request):
        return HttpResponseRedirect(reverse('hotels:list-hotels'))
