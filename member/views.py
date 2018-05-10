# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Member
from .forms import MemberForm, AdhesionForm


# sample get
# @csrf_exempt
@login_required
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

@login_required
def index(request):
    template = loader.get_template('member/index.html')
    context = {'user': request.user}
    return HttpResponse(template.render(context, request))

@login_required
def member(request):
    if request.method == 'POST':
        member_form = MemberForm(request.POST, prefix = "member")
        adh_form = AdhesionForm(request.POST, prefix = "adhesion")
        if member_form.is_valid() and  adh_form.is_valid():
            new_adherent = member_form.save()
            adh = adh_form.save(commit = False)
            adh.member = new_adherent
            adh.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        member_form = MemberForm(prefix = 'member')
        adh_form = AdhesionForm(prefix = 'adhesion')

    return render(request, 'member/member.html', {'user': request.user, 'form': member_form, 'adh_form': adh_form})



