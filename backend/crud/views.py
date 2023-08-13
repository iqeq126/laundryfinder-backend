import os.path

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework import settings as settings
from .models import Product, Clothes#, Tag
from .ProductSerializer import ProductSerializer as ps, ProductInsertSerializer as pis
from .ProductSerializer import ClothesSerializer as cs
# from .ProductSerializer import TagSerializer as ts
import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from urllib.parse import urlencode, unquote, quote_plus
import requests

import base64

UPLOAD_DIR = "C:/NAS/Frontend/frontend/public/images/"#os.path.dirname(__file__) + "/static/images/"
TAG_DIR = "C:/NAS/Frontend/frontend/public/tag_images/" #os.path.dirname(__file__) + "/static/tag_images/"
# TAG_DIR = "http://138.2.117.158/tag_images/"
serviceKey = "RCRS2BYQrxm9Ughup5pUew%2BQJljutDtoR2FFUrfs8MxNosEYPRHmBqLEWifOLl7vi6jgSc45OWHSmfZySLoUiQ%3D%3D"
serviceKeyDecoded = unquote(serviceKey, 'UTF-8')
"""
def Tag(request, hash_pk):
    tag = get_object_or_404(ts, pk=hash_pk)
    articles = tag.article_set.order_by('-pk')
    context = {
        'hashtag': tag,
        'articles': articles,
    }
    return render(request, '', context)"""
@api_view(['GET'])
def mapAPI(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    url = "//dapi.kakao.com/v2/maps/sdk.js?appkey=a499198564b134ecd2c79412b1c30365"
    #returnType = "json"
    #numOfRows = "3"
    #pageNo = "1"

    response = requests.get(url)
    return HttpResponse(response)

def clothesAPI(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    url = "https://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1?ServiceKey=RCRS2BYQrxm9Ughup5pUew%2BQJljutDtoR2FFUrfs8MxNosEYPRHmBqLEWifOLl7vi6jgSc45OWHSmfZySLoUiQ%3D%3D&desc_kor=%EB%B0%94%EB%82%98%EB%82%98%EC%B9%A9&numOfRows=1&pageNo=1&type=json"
    returnType="json"
    numOfRows="3"
    pageNo="1"

    # queryParams = '?' + urlencode({ quote_plus('ServiceKey=') : serviceKeyDecoded, quote_plus('&numOfRows=') : numOfRows, quote_plus('&pageNo=') : pageNo, quote_plus('&type=') : returnType })
    # res = requests.get(url)
    # json = res.text
    # print(json)
    # return json
    # return HttpResponse(simplejson.dumps(json))

    #datas = Food.myJson.all()
    #mydata = datas[0]
    #serializer = fs(mydata)
    #return Response(serializer.data)
    response = requests.get(url)
    return HttpResponse(response.text)



def home(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    return render(request, "index.html")



def list(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    user = request.user
    tag = request.GET.get("tag")
    try:
        product_name = request.GET["product_name"]
        if tag:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name, tag__tag_name__exact=tag).order_by(
                "-product_name"
            )
        else:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name).order_by(
                "-product_name"
            )
    except:
        product_name = ""
        if tag:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name, tag__tag_name__exact=tag).order_by(
                "-product_name"
            )
        else:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name).order_by(
                "-product_name"
            )

    serializer = ps(items, many=True)
    return HttpResponse(simplejson.dumps(serializer.data))



def list2(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    user = request.user
    tag = request.GET.get("tag")
    try:
        product_name = request.GET["product_name"]
        if tag:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name, tag__tag_name__iconstains=tag).order_by(
                "-product_name"
            )
        else:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name).order_by(
                "-product_name"
            )
    except:
        product_name = ""
        if tag:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name, tag__tag_name__icontains=tag).order_by(
                "-product_name"
            )
        else:
            items = Product.objects.filter(
                user=user, product_name__contains=product_name).order_by(
                "-product_name"
            )

    serializer = ps(items, many=True)
    return HttpResponse(simplejson.dumps(serializer.data))



"""
@method_decorator(csrf_exempt, name='dispatch')
class insertView(APIView):

    @csrf_exempt
    def post(self, request):
        serializer = ps(data = request.data)
        product =  ps(data = request.data)

        if "images" in request.FILES:
            file = request.FILES["images"]
            filename = file._name
            fs = FileSystemStorage(location=UPLOAD_DIR + filename)
            filename = fs.save(UPLOAD_DIR, file)

            product = serializer.save()
            product.filename = fs.url(filename)
            default_storage.save(UPLOAD_DIR+ file.name, file)
            #fp = open("%s%s" % (UPLOAD_DIR, filename), "wb")
            #product = serializer.save()
            #product.images.save(file._name, file)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Product created successfully', 'product_name': product.product_name}, status=201)
        return Response(serializer.errors, status=400)
"""



@method_decorator(csrf_exempt, name='dispatch')
class insertView(APIView):

    @csrf_exempt
    def post(self, request):
        serializer = ps(data=request.data)

        if "images" in request.FILES:
            file = request.FILES["images"]

            # 데이터 URL을 이미지 파일로 변환하여 저장
            if file.name.startswith("blob:"):
                data_url = file.read().decode('utf-8')
                _, data = data_url.split(";base64,")
                image_data = base64.b64decode(data)

                # 파일 이름 생성
                ext = file.content_type.split("/")[-1]
                file_name = f"{default_storage.get_valid_name(file.name)}.{ext}"
                file_path = default_storage.save(file_name, ContentFile(image_data))
                filename = default_storage.url(file_path)
            else:
                # 일반적인 이미지 파일 처리
                filename = default_storage.save(file.name, file)

            if serializer.is_valid():
                product = serializer.save()
                product.filename = filename
                product.save()

                return Response({'message': 'Product created successfully', 'product_name': product.product_name},
                                status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'message': 'No image file provided'}, status=400)
def detail(request, product_code):
#    if not request.session.get('user'):
#        return redirect('/user/login')

    row = Product.objects.get(product_code=product_code)
    serializer = ps(row)
    return HttpResponse(simplejson.dumps(serializer.data))


@csrf_exempt
def update(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    product_code = request.POST["product_code"]
    row_src = Product.objects.get(product_code=product_code)

    filename = row_src.filename
    if "img" in request.FILES:
        file = request.FILES["img"]
        filename = file._name

        fp = open("%s%s" % (UPLOAD_DIR, filename), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    if "tag_image" in request.FILES:
        tag = request.FILES["tag_image"]
        tag_name = tag._name
        fp = open("%s%s" % (TAG_DIR, tag_name), "wb")
        for chunk in tag.chunks():
            fp.write(chunk)
        fp.close()
    else:
        tag_name = "-"
    row_new = Product(
        product_code=product_code,
        product_name=request.POST["product_name"],
        description=request.POST["description"],
        #price=request.POST["price"],
        filename=filename,
        tag_name = tag_name,
    )

    row_new.save()


def delete(request):
#    if not request.session.get('user'):
#        return redirect('/user/login')
    Product.objects.get(product_code=request.GET["product_code"]).delete()
