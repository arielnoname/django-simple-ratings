# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse  # NOQA

from .models import Rating, Score


def create(request):
    content_type_id = request.POST.get('content_type_id')
    object_id = request.POST.get('object_id')
    ct = ContentType.objects.get_for_id(content_type_id)
    return_url = request.POST.get('return_url')
    try:
        # Current user HAS rated this object
        # Updates his rating and total score
        rating = Rating.objects.get(author=request.user, object_id=object_id, content_type_id=content_type_id)
        rating.vote = request.POST.get('vote')
        rating.save()

        votes = Rating.objects.filter(object_id=object_id, content_type_id=content_type_id)
        total_score = calculate_score(votes)
        score = Score.objects.get(object_id=object_id, content_type_id=content_type_id)
        score.total_score = total_score
        score.save(force_update=True)
        messages.success(request, 'Score updated succesfully')
    except Rating.DoesNotExist:
        # Current user has NOT rated this object
        # Saves first new rating
        rating = Rating()
        rating.content_type = ct
        rating.object_id = object_id
        rating.vote = request.POST.get('vote')
        rating.author = request.user
        rating.save()

        # Saves first new total score, same value as new rating
        try:
            score = Score.objects.get(object_id=object_id, content_type_id=content_type_id)
            votes = Rating.objects.filter(object_id=object_id, content_type_id=content_type_id)
            total_score = calculate_score(votes)
            score.total_score = total_score
            score.save(force_update=True)
            messages.success(request, 'Score updated succesfully')

        except Score.DoesNotExist:
            score = Score()
            score.content_type = ct
            score.object_id = object_id
            score.total_score = rating.vote
            score.save()
            messages.success(request, 'Score created succesfully')
    return redirect(return_url)


def calculate_score(votes):
    score = []
    for vote in votes:
        score.append(vote.vote)
    score = [item for item in score if item != 0]
    n = len(score)
    if n == 0:
        n = 1
    score = float(sum(score))
    score = float(score / n)
    score = round(score, 1)
    return score
