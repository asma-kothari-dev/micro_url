# core python imports
import urlparse

# django imports
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404

# project imports
import micro_url.settings as settings

# app imports
from models import MicroUrl
from forms import MicroUrlForm


HTTP_GET = 'GET'
HTTP_POST = 'POST'


def create_micro_url(request):
    """
    Micro Url Generator Endpoint
    """

    if request.method == HTTP_POST:
        # Instantiate MicroUrlForm with POST data
        form = MicroUrlForm(request.POST)
        # Validate form
        if form.is_valid():
            # Form is valid, let's save the form
            obj = form.save()
            messages.success(request, 'Micro URL created succsessfully')
            return HttpResponseRedirect(reverse('display_micro_url', args=(obj.id,)))
    else:
        # Brand new form for a new micro url
        form = MicroUrlForm()
    data = {'form': form, 'layout': 'horizontal'}
    return render(request, 'shrink/create_micro_url.html', data)


def display_micro_url(request, pk):
    """
    Displays the micro url contructed
    """

    # Raises Http404 if Micro Url object is not found
    micro_url_object = get_object_or_404(MicroUrl, pk=pk)

    # Send preview of the micro url
    preview = '!' + micro_url_object.alias

    # prepare data
    data = {'micro_url': micro_url_object.micro_url,
            'preview': urlparse.urljoin(settings.BASE_MICRO_URL, preview)
            }
    return render(request, 'shrink/display_micro_url.html', data)


def preview_micro_url(request, pk):
    """
    Preview the micro url contructed
    """

    # Raises Http404 if Micro Url object is not found
    micro_url_object = get_object_or_404(MicroUrl, pk=pk)

    # Send preview of the micro url
    preview = '!' + micro_url_object.alias

    # prepare data
    data = {'original_url': micro_url_object.link,
            'micro_url': micro_url_object.micro_url,
            'submitter': micro_url_object.submitter
            }
    return render(request, 'shrink/preview_micro_url.html', data)


def redirect(request):
    """
    Redirects user from micro url to original url.
    Also redirects to preview the micro url
    """

    path_info = request.META['PATH_INFO']
    if path_info.endswith('/'):
        alias = path_info[:-1].split("/")[-1]
    else:
        alias = path_info.split("/")[-1]

    if '!' in alias:
        micro_url_object = MicroUrl.objects.get_micro_url_object(alias=alias[
                                                                 1:])
        return HttpResponseRedirect(reverse('preview_micro_url',
                                            args=(micro_url_object.id,)))

    # get original url for the received micro url
    original_url = MicroUrl.objects.get_original_url(alias=str(alias))

    # redirect to original url if exists otherwise raise 404
    if original_url:
        return HttpResponseRedirect(original_url)
    else:
        raise Http404('No url found for %s' % alias)
