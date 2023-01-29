from django.contrib import admin
from .models import Category, CorruptionData


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'slug',
    )
    
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(CorruptionData)
class CorruptionData(admin.ModelAdmin):
    list_display = (
        'latitude',
        'longitude',
        'location_name',
    )

    list_filter = (
        'created_at',
        'category',
    )


# Renaming Admin Panel
admin.site.site_header = "FAIR MAP"
admin.site.site_title = "FAIR MAP Admin Portal"
admin.site.index_title = "Welcome to Admin Panel of FAIR MAP"
