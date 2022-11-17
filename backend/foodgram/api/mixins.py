from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from recipes.models import IngredientInRecipe, Recipe
from users.models import Subscribe


class CreateDestroy(ModelViewSet):
    """Вьюсет, содержащий методы для создания и удаления экземпляров класса."""
    model_class = None

    def _post_method_for_actions(self, request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    # def _delete_method_for_actions(self, request, pk):
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     model_obj = get_object_or_404(
    #         self.model_class, user=request.user, recipe=recipe)
    #     model_obj.delete()
    #     return Response(status=HTTP_204_NO_CONTENT)


class IsSubscribed:
    """Класс добавляющий в сериализатор дополнительное поле,
    отображающее наличие подписки на автора."""

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.followers.filter(author=obj).exists()


class CreatePopItems:
    """Вспомогательный класс для сериализатора.
    Задаёт методы создания и изменения рецептов."""

    @staticmethod
    def create_ingredients(recipe, ingredients):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients])

    @staticmethod
    def create_tags(recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)

    @staticmethod
    def pop_items(validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        return tags, ingredients


class RepresentationMixin(ModelSerializer):
    """Сериализатор с переопределённым методом."""

    def to_representation(self, instance):
        from .serializers import (RecipeObtainSerializer, RecipeSerializer,
                                  SubscriptionsSerializer)
        context = {'request': self.context.get('request')}
        if isinstance(instance, Subscribe):
            return SubscriptionsSerializer(
                instance.author, context=context).data
        if isinstance(instance, Recipe):
            return RecipeObtainSerializer(
                instance=instance, context=context).data
        return RecipeSerializer(
            instance.recipe, context=context).data
