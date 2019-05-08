from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render, redirect
from .models import Clothes, Bidding, Person
from .forms import ClothesForm, BiddingForm, FilterForm, AddFilterForm, RegistrationForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.mail import send_mail
import pytz, re
from django.http import Http404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def index(request, page_id=0):
    clothes_per_page = 30
    Clothes.objects.filter(closed=False, openuntil__lte=datetime.utcnow().replace(tzinfo=pytz.utc)).update(closed=True)
    min_ind, max_ind = page_id * clothes_per_page, (page_id + 1) * clothes_per_page
    if not request.method == 'POST':
        if 'search-clothes-post' in request.session:
            request.POST = request.session['search-clothes-post']
            request.method = 'POST'
    if request.method == 'POST':
        request.session['search-clothes-post'] = request.POST
        form = FilterForm(request.POST, request.user)

        if form.is_valid():
            input_brand = request.POST.get('brand')
            input_color = request.POST.get('color')
            input_ctype = request.POST.get('ctype')
            input_size = request.POST.get('size')
            input_condition = request.POST.get('condition')
            input_sellprice_low = request.POST.get('input_sellprice_low')
            input_sellprice_high = request.POST.get('input_sellprice_high')
            input_originalprice_low = request.POST.get('input_originalprice_low')
            input_originalprice_high = request.POST.get('input_originalprice_high')
            clothes_list = Clothes.objects.all()
            if input_size:
                clothes_list = clothes_list.filter(size=input_size).all()
            if input_condition:
                clothes_list = clothes_list.filter(condition=input_condition).all()
            if input_brand:
                clothes_list = clothes_list.filter(brand__icontains=input_brand).all()
            if input_color:
                clothes_list = clothes_list.filter(color__icontains=input_color).all()
            if input_ctype:
                clothes_list = clothes_list.filter(ctype__icontains=input_ctype).all()
            if input_sellprice_low:
                clothes_list = clothes_list.filter(sellprice__gte=input_sellprice_low).all()
            if input_sellprice_high:
                clothes_list = clothes_list.filter(sellprice__lte=input_sellprice_high).all()
            if input_originalprice_low:
                clothes_list = clothes_list.filter(orginalprice__gte=input_originalprice_low).all()
            if input_originalprice_high:
                clothes_list = clothes_list.filter(orginalprice__lte=input_originalprice_high).all()
            clothes_list = clothes_list.filter(closed=False).order_by('openuntil').all()
            max_page = clothes_list.count() // clothes_per_page
            clothes_list = clothes_list[min_ind:max_ind] # all clothes items that are open for bidding
            next_page = page_id + 1 if page_id + 1 <= max_page else None
            prev_page = page_id - 1 if page_id - 1 >= 0 else None
            context = RequestContext(request, {"clothes": clothes_list, "form": form,
                                               "next": next_page, "prev": prev_page})
            return render(request, 'index.html', context.flatten())
    else:
        form = FilterForm()
        max_page = Clothes.objects.count() // clothes_per_page
        clothes_list = Clothes.objects.all()
        next_page = page_id + 1 if page_id + 1 <= max_page else None
        prev_page = page_id - 1 if page_id - 1 >= 0 else None
        clothes_list = clothes_list.filter(closed=False).order_by('openuntil').all()[min_ind:max_ind]  # order clothes items by date
        context = RequestContext(request, {"clothes": clothes_list, "form": form,
                                           "next": next_page, "prev": prev_page})
    return render(request, 'index.html', context.flatten())


def clothes(request):
    if request.method == 'POST':
        form = ClothesForm(request.POST, request.FILES)
        if form.is_valid():
            clothes_image = request.FILES.get('clothes_img')
            clothes_original_price = request.POST.get('clothes_original_price', '')
            clothes_sellprice = request.POST.get('clothes_sellprice', '')
            clothes_size = request.POST.get('clothes_size', '')
            clothes_color = request.POST.get('clothes_color', '')
            clothes_brand = request.POST.get('clothes_brand', '')
            clothes_type = request.POST.get('clothes_type', '')
            clothes_condition = request.POST.get('clothes_condition', '')
            clothes_details = request.POST.get('clothes_details', '')
            clothes_obj = Clothes(sellerid=Person.objects.get(username=request.user.username),
                                  orginalprice=clothes_original_price,
                                  sellprice=clothes_sellprice,
                                  condition=clothes_condition,
                                  size=clothes_size,
                                  color=clothes_color,
                                  brand=clothes_brand,
                                  ctype=clothes_type,
                                  details=clothes_details,
                                  image=clothes_image,
                                  closed=False,
                                  openuntil=datetime.now() + timedelta(days=7))
            clothes_obj.save()
            return redirect('/')
    else:
        form = ClothesForm()
    return render(request, 'clothes.html', {'form': form})


def detail(request, clothes_id):
    if request.method == 'GET':
        clothes = get_object_or_404(Clothes, pk=clothes_id)
        try:
            bidding = Bidding.objects.filter(clothes__pk=clothes_id).order_by('-biddingtime').first()
        except Bidding.DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        contact = clothes.sellerid

    elif request.method == 'POST':
        clothes = get_object_or_404(Clothes, pk=clothes_id)
        contact = clothes.sellerid
        try:
            bidding = Bidding.objects.filter(clothes__pk=clothes_id).order_by('-biddingtime').first()
        except bidding.DoesNotExist:
            raise Http404("No Bidding matches the given query.")
        bidding_check = BiddingForm(request.POST, request.FILES)
        if bidding_check.is_valid() and request.user.username:
            bidding_price = request.POST.get('bidding_price', '')
            if bool(re.search('(![0-9\.])', bidding_price)) or (not bidding_price.isnumeric) or (float(bidding_price) <= 0):
                messages.info(request, 'Invalid Bid!')
            if not bidding:
                if round(float(bidding_price), 2) > clothes.sellprice and request.user.username != clothes.sellerid.username:
                    bidding = Bidding(
                        person=Person.objects.get(username=request.user.username),
                        biddingtime=datetime.now(),
                        biddingprice='{:.2f}'.format(round(float(bidding_price), 2)),
                        clothes=clothes
                    )
                    bidding.save()
                    messages.info(request, 'Successful Bid!')
                else:
                    messages.info(request, 'Invalid Bid!')
            elif request.user.username == clothes.sellerid.username or round(float(bidding_price), 2) <= bidding.biddingprice or clothes.closed:
                messages.info(request, 'Invalid Bid!')
            else:
                if request.user.username != bidding.person.username:
                    send_mail(
                        'Someone Has A Higher Bid!',
                        'Hi there!\n\nIt seems that someone has a higher bid on the {} item.\n\nYour bidding price '
                        'was ${}.\n\nAccess our website to secure your deal!\n\n'.format(clothes.brand,
                                                                                         bidding.biddingprice),
                        'FashionBiddingWeb@duke.edu',
                        [bidding.person.email],
                        fail_silently=False,
                    )
                bidding = Bidding(
                    person=Person.objects.get(username=request.user.username),
                    biddingtime=datetime.now(),
                    biddingprice='{:.2f}'.format(round(float(bidding_price), 2)),
                    clothes=clothes
                )
                bidding.save()
                messages.info(request, 'Successful Bid!')
        else:
            try:
                bidding = Bidding.objects.filter(clothes__pk=clothes_id).order_by('-biddingtime').first()
            except Bidding.DoesNotExist:
                raise Http404("No Bidding matches the given query.")
            messages.info(request, 'Invalid Bid!')
    return render(request, 'details.html', {'clothes': clothes, 'bidding': bidding, 'contact': contact})


def profile(request, user_id):
    username = User.objects.get(pk=user_id).username
    sold_clothes = Clothes.objects.filter(sellerid__username=username)
    bid_clothes = list(set([i.clothes for i in Bidding.objects.filter(person__username=username)]))
    context = RequestContext(request, {'soldclothes': sold_clothes,
                                        'bidclothes': bid_clothes})
    return render(request, 'profile.html', context.flatten())


def signup(request):
    if request.method == 'POST':
        form1 = UserCreationForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            username = form1.cleaned_data.get("username")
            form2.cleaned_data['username'] = username
            form2.save()
            password = form1.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/page/0')
    else:
        form1 = UserCreationForm()
        form2 = RegistrationForm()
    return render(request, 'signup.html', {'form1': form1, 'form2': form2})


def page(request):
    if 'search-clothes-post' in request.session:
        request.session.modified = True
        for i in request.session['search-clothes-post']:
            if 'csrf' not in i:
                request.session['search-clothes-post'][i] = ''
        request.POST = request.session['search-clothes-post']
    return redirect('/page/0', request)
