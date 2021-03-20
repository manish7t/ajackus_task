from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.settings import api_settings as token_settings
from rest_framework.settings import api_settings
from .serializers import *
from .models import *
from rest_framework import mixins
from django.contrib.auth import (authenticate, login as auth_login)
from .funcation import *
from django.shortcuts import get_object_or_404

# pagination setting for api view
pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
paginator = pagination_class()


@permission_classes([AllowAny])
class UserRegistration(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        data = request.data
        password = request.data['password']
        serailizer = UserRegistrationSerializer(data=data)

        if serailizer.is_valid():
            instance = serailizer.save(username=request.data['email'])
            instance.set_password(password)
            instance.save()
        else:
            return Response({'status': 400, 'errors': serailizer.errors})

        # Token Generated after registration
        payload = token_settings.JWT_PAYLOAD_HANDLER(instance)
        token = token_settings.JWT_ENCODE_HANDLER(payload)
        return Response({'status': '200', 'token': token})


@permission_classes([AllowAny])
class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = request.data['username']
        password = request.data['password']

        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid():

            user = authenticate(username=username, password=password)
            auth_login(request, user)
            payload = token_settings.JWT_PAYLOAD_HANDLER(user)
            token = token_settings.JWT_ENCODE_HANDLER(payload)
            return Response({'status': '200', 'token': token})
        else:
            return Response({'status': '400', 'errors': serializer.errors})


# Create Content API
@permission_classes([IsAuthenticated])
class CreateContent(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = ContentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            app_user = AppUser.objects.get(id=self.request.user.id, is_superuser=0)
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'Invalid User!!'})

        return serializer.save(app_user=app_user)


# Retrieve All Content
@permission_classes([IsAuthenticated])
class GetAllContentAPI(ListModelMixin, GenericAPIView):
    queryset = Content.objects.all()
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = ListContentSerializer

    def get(self, request, *args, **kwargs):
        return paginator.get_paginated_response({'status': 200, 'data': self.list(request, *args, *kwargs).data})


# GET Individual Content API
@permission_classes([IsAuthenticated])
class RetrieveContent(RetrieveModelMixin, GenericAPIView):
    serializer_class = ListContentSerializer
    queryset = Content.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        try:
            content_instance = Content.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return Response({'status': '400', 'error': 'Invalid Content !!'})
        serializer = self.get_serializer(content_instance)
        return Response(serializer.data)


# Update Individual Content API
@permission_classes([IsAuthenticated])
class UpdateContent(UpdateModelMixin, GenericAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def perform_update(self, serializer):
        return serializer.save()

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(Content, id=kwargs.get('pk'))
        if instance.app_user.id != self.request.user.id:
            user = get_object_or_404(AppUser, id=self.request.user.id)
            if user.is_superuser != 1:
                raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})

        return self.update(request, *args, **kwargs)


# Delete Content API
@permission_classes([IsAuthenticated])
class DeleteContent(DestroyModelMixin, GenericAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def perform_destroy(self, instance):

        if instance.app_user.id != self.request.user.id:
            user = AppUser.objects.get(id=self.request.user.id)

            if user.is_superuser == 1:
                instance.delete()
            else:
                raise ValidationError({'status': '400', 'error': 'unauthorized user to perform this operation!!'})
        else:
            instance.delete()

    def delete(self, request, *args, **kwargs):
        return Response({'status': '200', 'msg': 'deleted', 'data': self.destroy(request, *args, **kwargs).data})


# Search Content API
@permission_classes([IsAuthenticated])
class SearchContent(APIView):

    def get(self, request):
        # get search keyword
        search_keyword = request.GET.get('search', '')

        # called search_contant function
        search_result = search_contant(search_keyword=search_keyword)

        # check search result
        if search_result:
            serializer = ContentSerializer(search_result, many=True)
            return Response({'data': serializer.data})

        return Response({'status': '400', 'error': 'No Records To Display'})
