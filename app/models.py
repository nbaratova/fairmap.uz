from django.db import models


class Category(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ['-name']
        verbose_name = 'Category'
        verbose_name_plural = '📚 Categories'

    def __str__(self):
        return self.name


class CorruptionData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=200, db_index=True, blank=True)
    
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category,
        related_name='corruption_data',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Corruption Survey Data'
        verbose_name_plural = '📔 Corruption Survey Data'

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
