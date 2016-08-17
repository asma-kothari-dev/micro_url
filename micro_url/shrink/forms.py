# django imports
from django import forms

# project imports
import micro_url.settings as settings

# app imports
from shrink.models import MicroUrl


class MicroUrlForm(forms.ModelForm):
    """ Form which takes a long url and a custom alias as input.
    Validates that the alias is not already taken and ensures that
    it is not shorter than the configured length.
    """

    class Meta:
        model = MicroUrl
        fields = ('link', 'alias')

    def __init__(self, *args, **kwargs):
        super(MicroUrlForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            f = self.fields[field]
            f.widget.attrs['placeholder'] = f.help_text
            f.help_text = None

    def clean(self):
        cleaned_data = super(MicroUrlForm, self).clean()
        link = cleaned_data.get('link', None)
        alias = cleaned_data.get("alias", None)

        if link:
            micro_url = MicroUrl.objects.filter(link=link)
            if micro_url.exists():
                self.add_error('link', 'Micro URL %s is already ' \
                    'generated for this url.' % micro_url[0].micro_url)

        if alias:
            if MicroUrl.objects.filter(alias=alias).exists():
                self.add_error('alias', '"%s" is already taken' %  alias)

            if len(alias) < settings.SHORT_URL_MAX_LEN:
                self.add_error('alias', 'Please provide a custom alias ' \
                    'of  atleast %d characters' % settings.SHORT_URL_MAX_LEN)

        return cleaned_data
