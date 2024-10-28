from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from django.db.models import Q

def buy(request):
    properties = Property.objects.all
    context = {'properties':properties}
    return render(request, 'Buy_Page.html', context)

def home(request):
    return render(request, 'home.html')

@login_required
def sell(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('details', property_id=property.id)
    else:
        form = PropertyForm()
    
    user_properties = Property.objects.filter(owner=request.user)
    
    context = {
        'form': form,
        'user_properties': user_properties,
    }
    return render(request, 'sell_page.html', context)

def rent(request):
    properties = Property.objects.all
    context = {'properties':properties}
    return render(request, 'Rent_Page.html', context=context)

def details(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    is_favorited = False
    
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            property=property
        ).exists()
    
    context = {
        'property': property,
        'is_favorited': is_favorited,
    }
    
    return render(request, 'details.html', context)

def contactUs(request):
    return render(request, 'Contact_us.html')

def privacyPolicy(request):
    return render(request, 'Privacy_Policy.html')

def terms(request):
    return render(request, 'Terms_&_Conditions.html')

def cookies(request):
    return render(request, 'Cookie_Policy.html')

def about(request):
    return render(request, 'About_us.html')

def search(request):
    query = request.GET.get('query', '')
    listing_type = request.GET.get('listing_type', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')

    properties = Property.objects.all()

    if query:
        properties = properties.filter(
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(zip_code__icontains=query)
        )

    if listing_type:
        properties = properties.filter(listing_type=listing_type)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)

    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)

    context = {
        'properties': properties,
        'query': query,
        'listing_type': listing_type,
        'min_price': min_price,
        'max_price': max_price,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
    }

    return render(request, 'search_results.html', context)

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.latitude = request.POST.get('latitude')
            property_instance.longitude = request.POST.get('longitude')
            property_instance.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    user_properties = Property.objects.filter(owner=request.user)
    return render(request, 'Sell_Page.html', {'form': form, 'user_properties': user_properties})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Property, Favorite
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_favorite(request, property_id):
    try:
        property = get_object_or_404(Property, id=property_id)
        favorite = Favorite.objects.filter(
            user=request.user,
            property=property
        )
        
        if favorite.exists():
            favorite.delete()
            return JsonResponse({
                'status': 'removed',
                'message': 'Property removed from favorites',
                'is_favorited': False
            })
        else:
            Favorite.objects.create(
                user=request.user,
                property=property
            )
            return JsonResponse({
                'status': 'added',
                'message': 'Property added to favorites',
                'is_favorited': True
            })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def favorite_properties(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    context = {
        'favorites': favorites
    }
    return render(request, 'favorite_properties.html', context)



