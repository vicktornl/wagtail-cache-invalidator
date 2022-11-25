from django import forms
from django.forms import fields

from wagtail_cache_invalidator.models import InvalidationRequest, PurgeCacheSite


class PurgeForm(forms.ModelForm):
    sites = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        queryset=PurgeCacheSite.objects.all(),
    )

    class Meta:
        model = InvalidationRequest
        fields = (
            "sites",
            "urls",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
