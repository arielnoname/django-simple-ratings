from django import forms

RANGES = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class CreateRatingForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect, choices=RANGES)
