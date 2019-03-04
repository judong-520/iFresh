import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets, exceptions

from rest_demo.models import Book, Publish, Token, Author, User
from rest_demo.serializer import BookSerializers, BookSerializers_, AuthorSerializers, PublishSerializers


# =================================================认证组件===================================================
class AuthToken(object):

    def authenticate(self, request):
        token = request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if token_obj:
            return token_obj.user.name, token_obj.token
        raise exceptions.AuthenticationFailed('验证失败')

    def authenticate_header(self, request):
        pass


# ================================================权限组件===================================================
class SVIPPermission(object):
    message="只有超级用户才能访问"

    def has_permission(self,request, view):
        username=request.user
        user_type=User.objects.filter(name=username).first().user_type
        if user_type==3:
            return True # 通过权限认证
        return False

# =========================================================序列化======================================================
class BookView(APIView):

    def get(self, request):
        # 第一种
        # book_list = list(Book.objects.all().values('title', 'price', 'publish', 'authors'))  # 注意pub_date时间不能序列化
        # return HttpResponse(json.dumps(book_list))

        # 第二种
        # authod_list = []
        # authods_obj = Author.objects.all()
        # for authod in authods_obj:
        #     authod = model_to_dict(authod)  # model_to_dict并不支持时间格式的序列化, 所以此方法用于序列化Book表是会出错的
        #     authod_list.append(authod)
        # return HttpResponse(json.dumps(authod_list))

        # 第三种
        book_list = Book.objects.all()
        bs = BookSerializers(book_list, many=True)
        # bs = BookSerializers(book_list, context={'request': request})   # 超链接字段
        return Response(bs.data)

    def post(self, request):
        # print(request)
        # print('body:', request.body)
        # print('post:', request.POST)
        # print('data:', request.data)
        bs = BookSerializers(data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)


class BookDetailView(APIView):

    def get(self, request, id):
        book = Book.objects.get(id=id)
        bs = BookSerializers(book)
        return Response(bs.data)

    def put(self, request, id):
        book = Book.objects.get(id=id)
        bs = BookSerializers(book, data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        return Response(bs.errors)

    def delete(self, request, id):
        Book.objects.get(id=id).delete()
        return HttpResponse('OK')


# ==================================================视图===========================================================


# 第一种
class AuthorView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AuthorDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# 第二种
class PublishView(generics.ListCreateAPIView):

    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


class PublishDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


# 第三种
class PublishViewSet(viewsets.ModelViewSet):

    authentication_classes = [AuthToken]

    queryset = Publish.objects.all()
    serializer_class = PublishSerializers



