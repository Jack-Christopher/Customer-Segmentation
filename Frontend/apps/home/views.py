# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from requests import get
from base64 import b64encode

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    
    metrics = get('http://127.0.0.1:5000/metrics')
    context['metrics'] = metrics.json()

    history = get('http://127.0.0.1:5000/history')
    context['history'] = history.json()

    img = get('http://127.0.0.1:5000/plot')
    image = b64encode(img.content).decode('ascii')
    context['image'] = image
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def tables(request):
    context = {'segment': 'tables'}

    response = get('http://127.0.0.1:5000/partners')
    context['partners'] = response.json()

    response = get('http://127.0.0.1:5000/leads')
    context['leads'] = response.json()

    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context, request))