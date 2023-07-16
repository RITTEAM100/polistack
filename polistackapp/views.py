from django.shortcuts import render
from .config import Config
from .constants import *

obj = Config()


def congress_view(request):
    page = int(request.GET.get("page", 1))
    search_query = request.GET.get("q", "").strip()

    sentiment_analysis_data = obj.perform_sentiment_analysis(search_query)
    tweets = sentiment_analysis_data["tweet_data"]
    sentiment_data = sentiment_analysis_data["sentiment_data"]

    congress_data = obj.fetch_bills(search_query, page, ITEMS_PER_PAGE)

    return render(
        request,
        "bills.html",
        {
            "congress_data": congress_data,
            "tweets": tweets,
            "sentiment_data": sentiment_data,
            "bills_per_page": ITEMS_PER_PAGE,
        },
    )


def bill_detail(request, bill_id):
    bill = obj.fetch_bill_details(bill_id)
    return render(request, "bill_detail.html", {"bill": bill})
