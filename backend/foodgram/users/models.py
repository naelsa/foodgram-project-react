from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.db.models import F, Model, Q


class User(AbstractUser):
    """Кастомный пользователь с дополнительными полями."""
    email = models.EmailField(
        validators=(EmailValidator,),
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=settings.MAX_LENGTH_USER,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Введите корректный username',
            code='invalid_username')]
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_NAME,)
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH_NAME,)
    password = models.CharField(
        max_length=settings.MAX_LENGTH_PASSWORD,
        verbose_name='Пароль',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    role = models.CharField(
        max_length=max(
            [len(role) for user, role in settings.USER_ROLE_CHOICES]),
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER_ROLE_USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return self.email

    @property
    def is_user(self):
        return self.role == settings.USER_ROLE_USER


class Subscribe(Model):
    """Подписка"""
    user = models.ForeignKey(
        User,
        related_name='followers',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followings',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='cant_follow_yourself')
        ]

    def __str__(self) -> str:
        return f'{self.user} follows {self.author}'
