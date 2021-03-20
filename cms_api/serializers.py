from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer, ValidationError, CharField)
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from .models import *
import six
import re

UserModel = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserRegistrationSerializer(DynamicFieldsModelSerializer, ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password', 'country', 'state', 'city', 'phone', 'address', 'pincode']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password")
        phone = data.get("phone")
        pincode = data.get("pincode")

        if re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password) is None:
            raise ValidationError('password length must be 8 and must contain1 uppercase 1 lowercase character')

        if len(str(phone)) != 10:
            raise ValidationError('Invalid Phone Number !! please check again')

        if len(str(pincode)) != 6:
            raise ValidationError('Invalid Pincode Number !! please check again')

        return data


class UserLoginSerializer(ModelSerializer):
    username = CharField()

    class Meta:
        model = UserModel
        fields = ['username', 'password', ]


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'email', 'full_name', 'phone', 'address', 'pincode']


# Taggit Library Custome Serializer
class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)
        return value


# Create Content
class ContentSerializer(TaggitSerializer, ModelSerializer):
    categories = NewTagListSerializerField()

    class Meta:
        model = Content
        fields = ['title', 'body', 'summary', 'document', 'categories']


# GET Individual Content
class ListContentSerializer(TaggitSerializer, ModelSerializer):
    categories = NewTagListSerializerField()
    app_user = UserDetailSerializer(many=False)

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'document', 'categories', 'update_time', 'upload_time', 'app_user']
