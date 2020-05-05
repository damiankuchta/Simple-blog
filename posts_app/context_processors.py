import datetime
import calendar

from django.core.cache import cache

from . import models

"""dates aviable for dates menu"""
def show_dates(request):
    if not cache.get("dates"):
        earielst_post_date = models.Post.objects.earliest('date').date
        start_date = [earielst_post_date.year, earielst_post_date.month]
        finish_date = [datetime.date.today().year, datetime.date.today().month]
        dates = []
        while True:
            if start_date[1] >= 13:
                start_date = [start_date[0]+1, 1]

            """if any posts exists fort that day append it into return value"""
            posts = models.Post.objects.filter(date__month=start_date[1])
            if posts:
                dates.append({"year": start_date[0],"month_name": calendar.month_name[start_date[1]], "month": start_date[1]})
                if finish_date == start_date:
                    break

            start_date = [start_date[0], start_date[1] + 1]
        cache.set("dates", reversed(dates))
        return {"dates": reversed(dates)}
    else:
        return { "dates": cache.get("dates") }