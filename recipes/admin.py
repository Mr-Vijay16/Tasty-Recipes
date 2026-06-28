from django.contrib import admin
from .models import Category, Recipe, Favorite
from .models import Rating, Comment

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(Rating)
admin.site.register(Comment)