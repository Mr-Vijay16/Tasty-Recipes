from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('recipe/<int:id>/',
         views.recipe_detail,
         name='recipe_detail'),

    path('register/',
         views.register,
         name='register'),

    path('login/',
         views.login_user,
         name='login'),

    path('logout/',
         views.logout_user,
         name='logout'),

    path('dashboard/',
         views.dashboard,
         name='dashboard'),

    path('add/',
         views.add_recipe,
         name='add_recipe'),

    path('edit/<int:id>/',
         views.edit_recipe,
         name='edit_recipe'),

    path('delete/<int:id>/',
         views.delete_recipe,
         name='delete_recipe'),
     path(
    'favorite/<int:id>/',
    views.favorite_recipe,
    name='favorite_recipe'
),
     path(
    'favorites/',
    views.favorites,
    name='favorites'
),


path(
    'favorites/',
    views.favorite_list,
    name='favorites'
),
path(
    'remove-favorite/<int:id>/',
    views.remove_favorite,
    name='remove_favorite'
),
path(
    'rate/<int:id>/',
    views.rate_recipe,
    name='rate_recipe'
),
path(
    'comment/<int:id>/',
    views.add_comment,
    name='add_comment'
),
path(
    'profile/',
    views.profile,
    name='profile'
),
path(
    'unfavorite/<int:id>/',
    views.remove_favorite,
    name='remove_recipe_favorite'
),


]