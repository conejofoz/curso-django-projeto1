from django.contrib import admin

# Register your models here.

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Recipe, RecipeAdmin)


