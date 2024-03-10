from django.shortcuts import render
from django.views import View
from .models import SearchableCapsule
from .forms import SearchForm

class CapsuleSearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        query = form.cleaned_data['q'] if form.is_valid() and 'q' in form.cleaned_data else ''
        # query = self.request.GET.get('q', '')
        searchable_capsules = SearchableCapsule.objects.filter(capsule__name__icontains=query, capsule__is_public=True)

        context = {
            'form': form,
            'query': query,
            'capsules': [searchable_capsule.capsule for searchable_capsule in searchable_capsules],
        }

        return render(request, self.template_name, context)










