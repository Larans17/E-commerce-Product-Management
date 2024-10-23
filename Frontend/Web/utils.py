
from django.utils.timezone import localtime
from django.shortcuts import redirect, render
from datetime import datetime, timezone
from django.conf import settings
import requests
import traceback
from django.contrib import messages
from datetime import datetime, timedelta
from functools import wraps

url = settings.BACK_END_URL
# dt = datetime.now(timezone.utc)
# dt = localtime(dt)

# current_date = datetime.now()
# days_until_saturday = (5 - current_date.weekday() + 7) % 7
# days_until_sunday = (6 - current_date.weekday() + 7) % 7
# saturday_date = current_date + timedelta(days=days_until_saturday)
# sunday_date = current_date + timedelta(days=days_until_sunday)

# # Get Current weekend Dates ::
# get_from_date = saturday_date.strftime("%Y-%m-%d")
# get_to_date = sunday_date.strftime("%Y-%m-%d")



class WebResponse:

    @staticmethod
    def Token_Authentication(request):
        
        try:
            Token = request.session['Token']
            headers = {'Authorization': 'Token {Token}'.format(Token=Token)}
            return headers
        except KeyError:
            headers = None
        
            
            
