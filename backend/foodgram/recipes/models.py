from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты для рецептов"""
    name = models.CharField(
        max_length=settings.INGREDIENT_NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=settings.INGREDIENT_MEASURE_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Тэг для рецепта"""
    name = models.CharField(
        max_length=settings.TAG_NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=settings.TAG_COLOR_LENGTH,
        unique=True,
        verbose_name='Цвет')
    slug = models.SlugField(
        unique=True,
        verbose_name='Относительный URL',
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Введите корректный URL',
            code='invalid_slug'
        )])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Рецепт"""
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Aвтор',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=settings.RECIPE_NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Ссылка на картинку'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (минуты)',
        validators=[
            MinValueValidator(1, 'Не может быть меньше 1 минуты'),
            MaxValueValidator(60, 'Не может быть больше 60 минут')
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientInRecipe(models.Model):
    """Ингредиенты для одного конкретного рецепта"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, 'Не может быть меньше 1')]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_in_recipe')
        ]

    def __str__(self):
        return f'Ингредиент {self.ingredient} рецепта {self.recipe.name}'


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User,
        related_name='favourites',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favourites',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe.name} в избранном у {self.user.name}'


class ShoppingCart(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User,
        related_name='purchases',
        verbose_name='Покупатель',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='purchases',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shoppingcart')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe.name} в списке покупок {self.user.name}'
