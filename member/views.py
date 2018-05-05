# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Member
from .forms import MemberForm


# sample get
# @csrf_exempt
def add_member(request):
    if request.method == 'GET':
        latest_member = Member.objects.all()[:5]
        output = ', '.join([q.email for q in latest_member])
        return HttpResponse(output)
    elif request.method == 'POST':
        if request.body:
            json_str = str(request.body, 'utf-8')
            json_data = json.loads(json_str)
            member = Member(email = json_data["email"], nom = json_data["nom"], prenom = json_data["prenom"])
            member.save()
            print (json_data)
            return HttpResponse("in body %s" % json_data["email"])
        else:
            # TODO : manage the error
            return HttpResponse("in body2")
    else:
        # TODO : manage the error
        return HttpResponse("in body3")

def index(request):
    template = loader.get_template('member/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
def militant(request):
    template = loader.get_template('member/militant.html')
    context = {}
    return HttpResponse(template.render(context, request))
def benevole(request):
    template = loader.get_template('member/benevole.html')
    context = {}
    return HttpResponse(template.render(context, request))
def adhesion(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MemberForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MemberForm()

    return render(request, 'member/adhesion.html', {'form': form})


def get_member(request, member_id):
    return HttpResponse("You're looking at member %s." % member_id)
