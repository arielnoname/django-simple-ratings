# django-simple-ratings
Very simple, unobtrusive ratings app for Django

Usage:

1. Clone this repo to your django app's folder
2. Add 'django-simple-ratings' to INSTALLED_APPS
3. On your template, load the template tags:
  ```
{% load ratings %}
  ```
4. Use the "show_ratings" template tag on an object: ``` {% show_ratings <object> %} ```

If you want to show the top rated objects for a given model, use the "top_rated" template tag: ```{% top_rated '<app_name>' '<model_name>' %} ```

Where <app_name> and <model_name> are case UNsensitive, don't forget the single quotes.

This uses the Django ContentTypes Framework. Borrowed some code examples from django-star-ratings and I specifically didn't want to use "GenericRelation" for showing the top rated objects because I wanted this to work without touching the model to be rated code.

This code is not the most elegant possible and I think it must be very incomplete. django-star-ratings is Python3 compatible and far more complete I would say.

Being that said, feel free to do whathever you want with this code. Help with improving is very much appreciated.
