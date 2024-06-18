from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.models import Subscription
from api.users.serializers import (
    AvatarSerializer,
    SubscribeSerializer,
    UserGETSerializer,
    UserPOSTSerializer,
)
from api.utils.variables import (
    ERROR_MSG_AVATAR,
    ERROR_MSG_SUBSCRIBE,
    ERROR_MSG_SUBSCRIBE_CREATE,
    PERMISSION_VARIABLES,
)
from common.utils import delete_or_400


class UserViewSet(DjoserUserViewSet):
    actions_classes_serializer = {
        'list': UserGETSerializer,
        'retrieve': UserGETSerializer,
        'create': UserPOSTSerializer,
        'me': UserGETSerializer,
        'subscriptions': SubscribeSerializer,
    }

    def get_queryset(self):
        if self.action == 'subscriptions':
            return get_user_model().objects.filter(
                subscriptions__in=Subscription.objects.filter(user=self.request.user)
            )
        return get_user_model().objects.all()

    def get_serializer_class(self):
        return self.actions_classes_serializer[self.action] if (
            self.action in self.actions_classes_serializer.keys()
        ) else super().get_serializer_class()

    def get_permissions(self):
        if self.action in PERMISSION_VARIABLES:
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(['patch', 'put'], detail=False, url_path='me/avatar')
    def avatar(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {'error': ERROR_MSG_AVATAR},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = get_object_or_404(
            get_user_model(),
            username=request.user
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

    @avatar.mapping.delete
    def delete_avatar(self, request, *args, **kwargs):
        instance = get_object_or_404(
            get_user_model(),
            username=request.user
        )
        instance.avatar = ''
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True,)
    def subscribe(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('id')):
            return Response(
                {'error': ERROR_MSG_SUBSCRIBE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscriber = get_object_or_404(
            get_user_model(),
            id=kwargs.get('id')
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

        serializer = SubscribeSerializer(
            subscriber,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, *args, **kwargs):
        subscriber = get_object_or_404(
            get_user_model(),
            id=kwargs.get('id')
        )
        return delete_or_400(
            Subscription,
            user=request.user,
            subscriber=subscriber,
        )

    @action(['get'], detail=False,)
    def subscriptions(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
