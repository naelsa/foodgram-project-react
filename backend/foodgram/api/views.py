from django.db.models.aggregates import Sum
from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscribe
from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDestroy
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeObtainSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          SubscriptionsSerializer, TagSerializer, User)
from .utils import create_shopping_cart_txt


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        url_path='me',
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if not self.request.user.is_anonymous:
            user = self.request.user
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Пользователь не авторизован',
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request, pk=None):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ['post'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        following = get_object_or_404(User, id=id)
        subscription = self.request.user.followers.filter(author=following)
        if request.method == 'POST':
            subscription = Subscribe.objects.create(
                user=self.request.user, author=following
            )
            serializer = SubscribeSerializer(subscription)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(
            {'error': 'Вы не подписаны на этого автора'},
            status=HTTP_400_BAD_REQUEST
        )

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        get_object_or_404(
            Subscribe, user=request.user, author__id=id
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = get_list_or_404(User, followings__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter


class RecipeViewSet(CreateDestroy):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filterset_class = RecipeFilter
    filterset_fields = ('author', )

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'get':
            return RecipeObtainSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["POST"])
    def favorite(self, request, pk):
        return self._post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk,
            model=Favorite)

    @action(detail=True, methods=["POST"])
    def shopping_cart(self, request, pk):
        return self._post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk,
            model=ShoppingCart)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientInRecipe.objects
            .select_related('ingredient', 'recipe')
            .prefetch_related('purchases')
            .filter(recipe__purchases__user=request.user)
            .values_list('ingredient__name', 'ingredient__measurement_unit')
            .annotate(Sum('amount'))
        )
        return create_shopping_cart_txt(ingredients)


class FavoriteViewSet(CreateDestroy):
    serializer_class = FavoriteSerializer
    model_class = Favorite


class PurchaseListView(CreateDestroy):
    serializer_class = ShoppingCartSerializer
    model_class = ShoppingCart
