from django.shortcuts import render
from .config import Config
from .constants import *

obj = Config()

def congress_view(request):
    page = int(request.GET.get('page', 1))

    congress_data = obj.fetch_bills(page, ITEMS_PER_PAGE)

    return render(request, 'bills.html', {'congress_data': congress_data, "bills_per_page": ITEMS_PER_PAGE})