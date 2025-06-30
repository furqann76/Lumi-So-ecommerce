# store/models.py

from django.db import models


class SiteTheme(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("custom", "Custom"),
    ]

    name = models.CharField(max_length=20, choices=THEME_CHOICES, unique=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {'(Active)' if self.is_active else ''}"
