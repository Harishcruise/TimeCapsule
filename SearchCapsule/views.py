from django.shortcuts import render
from django.views import View
from .models import SearchableCapsule

class CapsuleSearchView(View):
    template_name = 'search_capsule/capsule_search_results.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')
        searchable_capsules = SearchableCapsule.objects.filter(capsule__name__icontains=query, capsule__is_public=True)

        context = {
            'query': query,
            'capsules': [searchable_capsule.capsule for searchable_capsule in searchable_capsules],
        }

        return render(request, self.template_name, context)










