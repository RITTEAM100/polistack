from django.shortcuts import render
from .config import Config

obj = Config()

def congress_view(request):
    limit = 10  # Set your desired limit
    offset = 0  # Set your desired offset

    congress_data = obj.store_congress_data(limit, offset)

    return render(request, 'bills.html', {'congress_data': congress_data})

