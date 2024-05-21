from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserGETSerializer, UserPOSTSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    http_method_names = ['get', 'post']
    actions_classes_serializer = {
        'list': UserGETSerializer,
        'retrieve': UserGETSerializer,
        'create': UserPOSTSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.actions_classes_serializer[self.action]
        except KeyError:
            raise KeyError('Not Allowed method')
    
    @action(detail=True, url_name='bb', url_path='tt', methods=('get', 'patch',))
    def me(self, request, *args, **kwargs):
        return Response({})
    


