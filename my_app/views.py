from django.shortcuts import render
import requests as re
from requests.compat import quote_plus
from bs4 import BeautifulSoup as bs
from . import models
from django.utils import timezone
# Create your views here.
BASE_CRAIGLIST_URL = "https://bangalore.craigslist.org/search/?query={}"
def home(request):
    return render(request, 'my_app/base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    print(final_url)
    response = re.get(final_url)
    data = response.text
    soup = bs(data, features='html.parser')
    post_titles = soup.find_all('a',{'class':'result-title'})
    print(post_titles)
    stuff_for_frontend = {
        'search':search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)