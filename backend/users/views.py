from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
#from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import AvatarSerializer, UserGETSerializer, UserPOSTSerializer


class UserViewSet(DjoserUserViewSet):
    queryset = get_user_model().objects.all()
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = (AllowAny,)
    actions_classes_serializer = {
        'list': UserGETSerializer,
        'retrieve': UserGETSerializer,
        'create': UserPOSTSerializer,
        'me': UserGETSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.actions_classes_serializer.keys():
            return self.actions_classes_serializer[self.action]
        return super().get_serializer_class()

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
    
    @action(['patch', 'delete', 'put'], detail=False, url_path='me/avatar')
    def avatar(self, request, *args, **kwargs):
        instance = get_object_or_404(
            self.queryset,
            username=request.user
        )

        serializer = AvatarSerializer(
            instance=instance,
            data=request.data,
            partial=True,
            context={'request':request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @action(['post', 'delete'], detail=True,)
    def subscribe(self, request, *args, **kwargs):
        print(request)
        return Response({'plug': 'Plug'})
    
    @action(['get'], detail=False,)
    def subscriptions(self, request, *args, **kwargs):
        print(request)
        return Response({'plug': 'Plug'})
    
    
# -------------------------------------------------------------
    # unused methods are disabled
    def activation(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def resend_activation(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def reset_password(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def set_username(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def reset_username(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(
            {'error': 'disabled functionality'},
            status=status.HTTP_400_BAD_REQUEST
        )


