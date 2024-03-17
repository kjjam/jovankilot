from django.http import Http404
from django.shortcuts import render

from installation.forms import SearchRequestForm
from installation.models import Request


def search_request_view(request):
    if request.method == 'GET':
        request_code = request.GET.get('r', '')
        form = SearchRequestForm(initial={'search_field': request_code})

        return render(request, 'main.html', {"form": form})
    if request.method == 'POST':
        form = SearchRequestForm(request.POST)
        if form.is_valid():
            web_id = form.cleaned_data['search_field']
            web_id = web_id.strip()
            request_object = Request.objects.filter(web_id__exact=web_id).first()
            if request_object:
                return render(request, 'request_detail.html', {"object": request_object})
            else:
                raise Http404
        else:
            raise Http404


def custom_404(request, exception):
    return render(request, '404.html', status=404)
