from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Posts, Comments, Follower, Following
from django.contrib.auth.models import User
from users.models import CustomUser
from ecommerce.models import Order
from ecommerce.views import create_product

Users = get_user_model()

def mainPage(request):
    # получаем все значения модели
    follower = Follower.objects.filter(user=request.user.id).values('follower_user')
    if follower != []:
        news_list = Posts.objects.filter(user__in=follower)
        news_list = news_list.union(Posts.objects.filter(user=request.user))
    else:
        news_list = Posts.objects.filter(user=request.user)
    follower_list = Follower.objects.filter(user=request.user.id)
    following_list = Following.objects.filter(user=request.user.id)
    users_list = Users.objects.exclude(id__in=follower)
    if not users_list:
        users_list = Users.objects.all()
    image_comments = Comments.objects.all()
    # Проверка есть ли товар в корзине пользователя
    orders = Order.objects.filter(customer=request.user.id).values('product')
    new_order = list()
    for order in orders:
         new_order.append(order['product'])
    orders = new_order
    return render(request, 'network/mainPage.html', {
        'news_list': news_list,
        'orders': orders,
        'users_list': users_list,
        'follower_list': follower_list,
        'following_list': following_list,
        'follower': follower,
        'image_comments': image_comments,
        })

def new_post(request):
    return render(request, 'network/new_post.html')

def submit(request):
        if request.method == 'POST':
            text_field = request.POST.get('text_field')
            image_field =  request.FILES.get('image_field')
            product_field = request.POST.get('product_field')
            if product_field == 'on':
                product_field = True
                price_field = request.POST.get('price_field')
                count_field = request.POST.get('count_field')
                profile_obj=Posts(text=text_field, user=request.user, date=datetime.now(), 
                                  image=image_field, product=product_field, price=price_field, 
                                  count=count_field).save()
                create_product(text_field, image_field, int(price_field)*100)
            else:
                profile_obj=Posts(text=text_field, user=request.user, date=datetime.now(), 
                                  image=image_field).save()
        return HttpResponseRedirect('/mainPage/')

def subscribe(request, id):
        if request.method == 'POST':
            user = CustomUser.objects.get(id=id)
            try:
                follower = Follower.objects.create(user=request.user)
            except:
                follower = Follower.objects.get(user=request.user)
            follower.follower_user.add(user)
            try:
                following = Following.objects.create(user=user)
            except:
                following = Following.objects.get(user=user)
            following.following_user.add(request.user)
        return HttpResponseRedirect('/mainPage/')

def unsubscribe(request, id):
        if request.method == 'POST':
            user = CustomUser.objects.get(id=id)
            my_obj = Following.objects.get(user=user, following_user=request.user)
            my_obj.following_user.remove(request.user)
            my_obj = Follower.objects.get(user=request.user, follower_user=user)
            my_obj.follower_user.remove(user)
        return HttpResponseRedirect('/mainPage/')

def likes(request, image_id, id):
        if request.method == 'POST':
            user = CustomUser.objects.get(id=id)
            news = Posts.objects.get(id=image_id)
            if not Posts.objects.filter(id=image_id, likes=user):
                if Posts.objects.filter(id=image_id, dislikes=user):
                    news.dislikes.remove(request.user)
                news.likes.add(request.user)
            else:
                news.likes.remove(request.user)
        return HttpResponseRedirect('/mainPage/')

def dislikes(request, image_id, id):
        if request.method == 'POST':
            user = CustomUser.objects.get(id=id)
            news = Posts.objects.get(id=image_id)
            if not Posts.objects.filter(id=image_id, dislikes=user):
                if Posts.objects.filter(id=image_id, likes=user):
                    news.likes.remove(request.user)
                news.dislikes.add(request.user)
            else:
                news.dislikes.remove(request.user)
        return HttpResponseRedirect('/mainPage/')

def add_comment(request, image_id):
    if request.method == 'POST':
        text = request.POST.get('text_field')
        image = Posts.objects.get(id=image_id)
        date = datetime.now()
        profile_obj=Comments(text=text, user=request.user, date=datetime.now(), image=image).save()
    return HttpResponseRedirect('/mainPage/')

# Для страницы пользователя
def userPage(request, id):
    news_list = Posts.objects.filter(user=id)
    user_name = Users.objects.filter(id=id)[0]
    followed_list = Following.objects.filter(user=id)
    return render(request, 'network/userPage.html', {
        'user_name': user_name,
        'news_list': news_list, 
        'followed_list': followed_list,
        })