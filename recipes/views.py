from django.shortcuts import render
from .models import Recipe,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from django.db.models import Avg



# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm, RegisterForm



from .models import Recipe, Category, Favorite, Rating, Comment

from django.core.paginator import Paginator

def home(request):
    recipes = Recipe.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        recipes = recipes.filter(
            title__icontains=search
        )

    if category:
        recipes = recipes.filter(
            category_id=category
        )

    favorites = []

    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(
            user=request.user
        ).values_list(
            'recipe_id',
            flat=True
        )

    context = {
        'recipes': recipes,
        'categories': categories,
        'favorites': favorites,
    }

    return render(
        request,
        'home.html',
        context
    )

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    comments = Comment.objects.filter(
        recipe=recipe
    ).order_by('-created_at')

    context = {
        'recipe': recipe,
        'comments': comments,
    }

    return render(
        request,
        'recipe_detail.html',
        context
    )
   
def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(
    request,
    'register.html',
    {'form': form}
)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user:
        login(request, user)
        return redirect('dashboard')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')

@login_required
def dashboard(request):
    recipes_list = Recipe.objects.filter(
        user=request.user
    ).order_by('-created_at')

    paginator = Paginator(recipes_list, 6)  # 6 recipes per page

    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)

    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    context = {
        'recipes': recipes,
        'favorites_count': favorites_count,
        'total_recipes': recipes_list.count(),
        'page_obj': recipes,
    }

    return render(
        request,
        'dashboard.html',
        context
    )

@login_required
def add_recipe(request):
    form = RecipeForm()


    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()
        return redirect('dashboard')

    return render(request, 'add_recipe.html', {'form': form})


@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(
    Recipe,
    id=id,
    user=request.user
    )

    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        form = RecipeForm(
            request.POST,
            request.FILES,
            instance=recipe
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(
    request,
    'edit_recipe.html',
    {
        'form': form,
        'recipe': recipe,
    }
)


@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(
    Recipe,
    id=id,
    user=request.user
    )

    if request.method == 'POST':
        recipe.delete()
        return redirect('dashboard')

    return render(
        request,
        'delete_recipe.html',
        {'recipe': recipe}
    )



def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        recipes = recipes.filter(title__icontains=search)

    if category:
        recipes = recipes.filter(category_id=category)

    paginator = Paginator(recipes, 6)  # 6 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorites = []

    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(
            user=request.user
        ).values_list('recipe_id', flat=True)

    context = {
        'recipes': page_obj,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'favorites': favorites,
    }

    return render(request, 'home.html', context)
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    comments = Comment.objects.filter(
        recipe=recipe
    ).order_by('-created_at')

    average_rating = Rating.objects.filter(
        recipe=recipe
    ).aggregate(
        Avg('stars')
    )['stars__avg']

    context = {
        'recipe': recipe,
        'comments': comments,
        'average_rating': average_rating,
    }

    return render(
        request,
        'recipe_detail.html',
        context
    )

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(
        request,
        'register.html',
        {'form': form}
    )

def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    recipes = Recipe.objects.filter(
        user=request.user
    )

    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    context = {
        'recipes': recipes,
        'recipes_count': recipes.count(),
        'favorites_count': favorites_count,
    }

    return render(
        request,
        'dashboard.html',
        context
    )
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user

            new_category = request.POST.get('new_category')

            if new_category:
                category, created = Category.objects.get_or_create(
                    name=new_category
                )
                recipe.category = category

            recipe.save()
            return redirect('dashboard')

    else:
        form = RecipeForm()

    return render(request, 'add_recipe.html', {'form': form})
@login_required
def edit_recipe(request, id):

    recipe = Recipe.objects.get(id=id)

    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        form = RecipeForm(
            request.POST,
            request.FILES,
            instance=recipe
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(
        request,
        'edit_recipe.html',
        {'form': form}
    )

@login_required
def delete_recipe(request, id):

    recipe = Recipe.objects.get(id=id)

    recipe.delete()

    return redirect('dashboard')


@login_required
def favorite_recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )

    return redirect('favorites')
@login_required
def favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        'recipe',
        'recipe__category'
    )

    context = {
        'favorites': favorites
    }

    return render(
        request,
        'favorites.html',
        context
    )

@login_required
def favorite_list(request):
    favorites = Favorite.objects.select_related(
        'recipe',
        'recipe__category'
    ).filter(
        user=request.user
    )

    return render(
        request,
        'favorites.html',
        {
            'favorites': favorites
        }
    )
@login_required
def remove_favorite(request, id):

    Favorite.objects.filter(
        user=request.user,
        recipe_id=id
    ).delete()

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'favorites'
        )
    )

@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    if request.method == 'POST':
        stars = request.POST.get('stars')

        Rating.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={
                'stars': stars
            }
        )

    return redirect(
        'recipe_detail',
        recipe_id=recipe.id
    )
    
@login_required
def add_comment(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    if request.method == 'POST':
        text = request.POST.get('comment')

        if text:
            Comment.objects.create(
                recipe=recipe,
                user=request.user,
                text=text
            )

    return redirect(
        'recipe_detail',
        recipe_id=recipe.id
    )
    
@login_required
def profile(request):

    total_recipes = Recipe.objects.filter(
        user=request.user
    ).count()

    total_favorites = Favorite.objects.filter(
        user=request.user
    ).count()

    total_comments = Comment.objects.filter(
        user=request.user
    ).count()

    context = {
        'total_recipes': total_recipes,
        'total_favorites': total_favorites,
        'total_comments': total_comments,
    }

    return render(
        request,
        'profile.html',
        context
    )