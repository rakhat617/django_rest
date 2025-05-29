from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Images(models.Model):
    image = models.ImageField(
        verbose_name="изображение",
        upload_to="images/",
    )
    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE,
        related_name="user_images",
        verbose_name="изображение пользователя",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self) -> str:
        return f"{self.pk}"