from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from accounts.models import UserProfile
import json
from django.urls import reverse


class UserProfileSerializer(ModelSerializer):
    github = SerializerMethodField()
    linkedin = SerializerMethodField()
    twitter = SerializerMethodField()
   
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def get_github(self, obj):
        return json.dumps(json.loads(obj.meta)["github"], indent=4)

    def get_twitter(self, obj):
        return json.dumps(json.loads(obj.meta)["twitter"], indent=4)

    def get_linkedin(self, obj):
        return json.dumps(json.loads(obj.meta)["linkedin"], indent=4)


class UserProfileListSerializer(ModelSerializer):
    id = HyperlinkedIdentityField(view_name='user-detail-api',
                                  lookup_field='pk')

    class Meta:
        model = UserProfile
        exclude = ('user', 'meta',)


class UserProfileAPISerializer(ModelSerializer):
    meta = SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def get_meta(self, obj):
        return json.loads(obj.meta)
