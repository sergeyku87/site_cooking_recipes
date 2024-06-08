from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.models import Subscription
from users.serializers import (
    AvatarSerializer,
    SubscribeSerializer,
    UserGETSerializer,
    UserPOSTSerializer,
)
from users.utils import delete_or_400
from users.variables import (
    ERROR_MSG_AVATAR,
    ERROR_MSG_SUBSCRIBE,
    ERROR_MSG_SUBSCRIBE_CREATE,
    PERMISSION_VARIABLES,
)


class UserViewSet(DjoserUserViewSet):
    actions_classes_serializer = {
        'list': UserGETSerializer,
        'retrieve': UserGETSerializer,
        'create': UserPOSTSerializer,
        'me': UserGETSerializer,
    }

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action in self.actions_classes_serializer.keys():
            return self.actions_classes_serializer[self.action]
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in PERMISSION_VARIABLES:
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(['patch', 'delete', 'put'], detail=False, url_path='me/avatar')
    def avatar(self, request, *args, **kwargs):
        instance = get_object_or_404(
            get_user_model(),
            username=request.user
        )
        if request.method == 'DELETE':
            instance.avatar = ''
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if not request.data:
            return Response(
                {'error': ERROR_MSG_AVATAR},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AvatarSerializer(
            instance=instance,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(['post', 'delete'], detail=True,)
    def subscribe(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method == 'DELETE':
            subscriber = get_object_or_404(
                get_user_model(),
                id=kwargs.get('id')
            )
        if request.method == 'POST':
            if request.user.id == int(kwargs.get('id')):
                return Response(
                    {'error': ERROR_MSG_SUBSCRIBE},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            _, created = Subscription.objects.get_or_create(
                user=request.user,
                subscriber=subscriber,
            )
            if not created:
                return Response(
                    {'error': ERROR_MSG_SUBSCRIBE_CREATE},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if request.method == 'DELETE':
            return delete_or_400(
                Subscription,
                user=request.user,
                subscriber=subscriber,
            )

        serializer = SubscribeSerializer(
            subscriber,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['get'], detail=False,)
    def subscriptions(self, request, *args, **kwargs):
        response = Subscription.objects.filter(user=request.user)
        page = self.paginate_queryset([sub.subscriber for sub in response])
        serializer = SubscribeSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    # disabled unused methods

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
