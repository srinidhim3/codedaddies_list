from django.shortcuts import render
import requests as re
from requests.compat import quote_plus
from bs4 import BeautifulSoup as bs
from . import models
from django.utils import timezone
# Create your views here.
BASE_CRAIGLIST_URL = "https://bangalore.craigslist.org/search/?query={}"
BASE_URL_IMAGE = "https://images.craigslist.org/{}_300x300.jpg"
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
    post_listings = soup.find_all('li',{'class':'result-row'})
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_URL_IMAGE.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))
    stuff_for_frontend = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)