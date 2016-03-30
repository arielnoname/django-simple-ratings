import datetime
from django import template
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from ..forms import CreateRatingForm
from ..models import Rating, Score
register = template.Library()


@register.inclusion_tag('ratings.html', takes_context=True)
def show_ratings(context, instance):
    create_rating_form = CreateRatingForm(auto_id=False)
    content_type = ContentType.objects.get_for_model(instance)
    object_id = instance.pk
    votes = Rating.objects.filter(object_id=object_id, content_type=content_type)
    try:
        Score.objects.get(object_id=object_id, content_type=content_type)
    except Score.DoesNotExist:
        score = 0
    return {
        'content_type_id': content_type.id,
        'object_id': object_id,
        'create_rating_form': create_rating_form,
        'return_url': str(context.request.path),
        'votes': votes,
        'score': score,
    }


@register.inclusion_tag('top_rated.html', takes_context=True)
def top_rated(context, app, model):
    content_type = ContentType.objects.get_by_natural_key(app, model)
    top_scores = Score.objects.filter(content_type=content_type).order_by('-total_score')[:10]

    today = datetime.date.today()
    month_ago = today - datetime.timedelta(days=30)

    objects_ids = []
    for rated_object in top_scores:
        objects_ids.append(rated_object.object_id)
    all_rated = content_type.get_all_objects_for_this_type()
    top_rated = all_rated.filter(created__range=(month_ago, today), pk__in=objects_ids)
    return {'top_rated': top_rated}
