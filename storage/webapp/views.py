import os

from django.shortcuts import render

from django.http import HttpResponse
from django.conf import settings


# Create your views here.
def index(request):
    try:
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse(
            """
             Webapp not found
            """,
            status=501,
        )
