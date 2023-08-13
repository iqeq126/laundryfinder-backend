import os.path#, shutil

import simplejson
from django.views.decorators.csrf import csrf_exempt
#from rest_framework.response import Response
#from rest_framework.decorators import api_view
#from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.viewsets import ModelViewSet

from .models import Tag

from .serializers import TagSerializer as ts#, TagImageSerializer, TagImage

#from django.views.decorators.csrf import csrf_exempt
#from urllib.parse import urlencode, unquote, quote_plus
#import requests


#from django.db.models import Count
#from rest_framework.parsers import JSONParser

#from rest_framework import status
#from rest_framework.response import Response

#from rest_framework.views import APIView
#from rest_framework.generics import RetrieveAPIView, GenericAPIView, ListAPIView, CreateAPIView
#from rest_framework.permissions import AllowAny, IsAuthenticated

UPLOAD_DIR = os.path.dirname(__file__) + "/static/tag_images/"
# UPLOAD_DIR = "http://138.2.117.158/tag_images/"
# Create your views here.

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('-tag_name')
    serializer_class = ts
    #pagination_class = CustomResultsSetPagination
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = TagFilter
    #permission_classes = [IsSuperUserOrReadOnly]

@csrf_exempt
def Tag(request, hash_pk):
    #if not request.session.get('user'):
    #    return redirect('/user/login')
    tag = get_object_or_404(ts, pk=Tag.tag_name)
    articles = tag.article_set.order_by('-pk')
    context = {
        'hashtag': tag,
        'articles': articles,
    }
    serializer = ts
    return HttpResponse(simplejson.dumps(serializer.data))


@csrf_exempt
def insert(request):
    #if not request.session.get('user'):
    #    return redirect('/user/login')
    if "tag_name" in request.FILES:
        file = request.FILES["tag_name"]
        file_name = file._name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    else:
        file_name = "-"

    row = Tag(
        tag_name=request.POST["tag_name"],
        # price=request.POST["price"],
        content=request.POST["content"],
        tag_image = request.POST["tag_image"],
    )
    row.save()