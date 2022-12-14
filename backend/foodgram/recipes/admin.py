from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 0


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',
                    'ingredient_name', 'tag_name', 'count_favourites')
    list_filter = ('author', 'name', 'tags',)
    inlines = [IngredientInRecipeInline, TagInline]

    @admin.display(description='В избранном')
    def count_favourites(self, obj):
        return obj.favourites.count()

    @admin.display(description='Ингредиенты')
    def ingredient_name(self, obj):
        return " %s" % (', '.join(
            [obj.ingredient.name for obj.ingredient in obj.ingredients.all()]))

    @admin.display(description='Тэги')
    def tag_name(self, obj):
        return " %s" % (', '.join(
            [obj.tag.name for obj.tag in obj.tags.all()]))


@admin.register(ShoppingCart)
class ShoppinpCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
