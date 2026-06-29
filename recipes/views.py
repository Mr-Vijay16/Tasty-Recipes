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




# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm, RegisterForm



from .models import Recipe, Category, Favorite, Rating, Comment

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
            category__id=category
        )

    context = {
        'recipes': recipes,
        'categories': categories,
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
def dashboard(request):
    recipes = Recipe.objects.filter(
        user=request.user
    )

    total_recipes = recipes.count()

    total_favorites = Favorite.objects.filter(
        user=request.user
    ).count()

    context = {
        'recipes': recipes,
        'total_recipes': total_recipes,
        'total_favorites': total_favorites,
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
        {'form': form}
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

    for recipe in recipes:
        if recipe.image:
            recipe.static_image = recipe.image.name.replace(
                'recipes/',
                'images/'
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
def recipe_detail(request, id):
    recipe = Recipe.objects.get(id=id)

    return render(
        request,
        'recipe_detail.html',
        {'recipe': recipe}
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
    recipes = Recipe.objects.filter(user=request.user)

    # Create static image path
    for recipe in recipes:
        if recipe.image:
            recipe.static_image = recipe.image.name.replace(
                'recipes/',
                'images/'
            )

    total_recipes = recipes.count()

    favorite_ids = Favorite.objects.filter(
        user=request.user
    ).values_list(
        'recipe_id',
        flat=True
    )

    total_favorites = len(favorite_ids)

    context = {
        'recipes': recipes,
        'total_recipes': total_recipes,
        'total_favorites': total_favorites,
        'favorite_ids': favorite_ids,
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
    favorite = get_object_or_404(
        Favorite,
        id=id,
        user=request.user
    )

    favorite.delete()

    return redirect('favorites')

@login_required
def rate_recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    stars = request.POST.get('stars')

    Rating.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={
            'stars': stars
        }
    )

    return redirect(
        'recipe_detail',
        id=id
    )
    
@login_required
def add_comment(request, id):
    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    if request.method == 'POST':
        text = request.POST.get('comment')

        Comment.objects.create(
            user=request.user,
            recipe=recipe,
            text=text
        )

    return redirect(
        'recipe_detail',
        id=id
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