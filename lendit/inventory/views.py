from django.http import JsonResponse
from django.shortcuts import render

from .models import Item


def get_all_items(request):

    queryset = Item.objects.prefetch_related('tags')

    data = []

    for item in queryset:
        data.append({
            'id' : item.id,
            'name' : item.name,
            'image' : item.image.url,
            'tags' : [tag.name for tag in item.tags.all()],

        })

    return JsonResponse({'items':data}, safe=False)


def item_list_view(request):
    return render(request, 'item_list.html', {})