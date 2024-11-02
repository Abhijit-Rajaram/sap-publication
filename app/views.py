from django.shortcuts import render
from app.models import *
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            # Additional custom profile fields can be handled here
            messages.success(request, 'User registered successfully!')
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f'Error registering user: {e}')
    return render(request, 'registration.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login') 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('mainhome')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
# Create your views here.

def auth_login(request):
    user = None
    print(request.user,'abcdefgh',request.session.keys())
    if request.method == "POST":
        print('post method')
        email_or_username = request.POST.get('username')
        password = request.POST.get('password')
        print(email_or_username,'=',password)
        if not email_or_username or not password:
            return render(request, 'login.html')
        
        try:
                user = User.objects.get(
                Q(email=email_or_username) | Q(username=email_or_username))
        except User.MultipleObjectsReturned:
                print('User.MultipleObjectsReturned')
                return render(request, 'login.html')
         

        if check_password(password, user.password):
            pass

            try:
                user = authenticate(
                    username=user.username, password=password)
                login(request, user)
            except Exception as e:
                print(e, "Exception auth user login partner.")
                return render(request, 'login.html')

        if request.user.is_authenticated:
            request.session['user_id'] = request.user.id
            print(request.user.id)
                  
            request.session['username'] = request.user.username
            
            
            return HttpResponseRedirect('/app/home')

    return render(request, 'login.html')

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_book(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        if key == 'add-book':
            print('adding book .......................')
            img = request.FILES['img']
            print(img)
            title = request.POST.get('title')
            author = request.POST.get('author')
            description = request.POST.get('description')
            isbn = request.POST.get('isbn')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            published_date = request.POST.get('published_date')
            department = request.POST.get('select_department')
            semester = request.POST.get('semester')
            year = request.POST.get('year')

            book_data = {
                'img': img,
                'title': title,
                'author': author,
                'description': description,
                'isbn': isbn,
                'price': price,
                'stock': stock,
                'published_date': published_date,
                'semester':semester,
                'year':year,
            }
            print(book_data)
            new_book = Book.objects.create(**book_data)
            new_book.department = Department.objects.get(id = department)
            new_book.save()
            print(new_book,'book')
        if key == 'add-department':
            print('adding category .......................')
            department = request.POST.get('department')
            degree = request.POST.get('select_degree')
            cat = Department.objects.create(degree_id=degree,name = department)
            print(cat,'Department')
        if key == 'add-degree':
            print('adding category .......................')
            name = request.POST.get('degree')
            cat = Degree.objects.create(name=name)
            print(cat,'Degree')
        # books = Book.objects.all()
        # print(books)
        # categories = Degree.objects.all()
        # print(categories)
        # # Redirect to a success page or any other page
        # return render(request, 'admin_page.html',{'books':books,'categories':categories})

    # If the request method is GET, render the form template

    books = Book.objects.all()
    print(books)
    degrees = Degree.objects.all()
    print(degrees)
    departments = Department.objects.all()
    print(departments)
    return render(request, 'admin_page.html',{'books':books,'degrees':degrees,'departments':departments})

def home(request):
    department = Department.objects.values('id','name','degree__name')
    data = []
    for i in department:
        sem = Book.objects.filter(department_id=i['id']).values('semester').order_by('semester').distinct()
        sem_list = [a['semester'] for a in sem]
        data.append({
            'id':i['id'],
            'degree__name':i['degree__name'],
            'name':i['name'],
            'semester':sem_list
        })
    print(data,'data')
    categories = Degree.objects.all()
    print(categories)
    return render(request, 'index.html',{'department':department,'categories':categories})

def mainhome(request):
    department = Department.objects.values('id','name','degree__name')
    data = []
    for i in department:
        year = Book.objects.filter(department_id=i['id']).values('year').order_by('year').distinct()
        print(year,'year')
        if len(year) > 0:
            year_list = []
            for a in year:
                sem = Book.objects.filter(department_id=i['id'],year=a['year']).values('semester').order_by('semester').distinct()
                year_list.append({
                    'year':a['year'],
                    'semester': [b['semester'] for b in sem]
                })
            data.append({
                'id':i['id'],
                'degree__name':i['degree__name'],
                'name':i['name'],
                'semester':year_list
            })
    print(data,'data')
    categories = Degree.objects.all()
    print(categories)
    return render(request, 'home.html',{'department':department,'categories':categories,'data':data})

def product(request,isbn):
    book = Book.objects.get(isbn=isbn)
    print(book)
    return render(request, 'single-product.html',{'book':book})

@login_required
def buy(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        print(isbn)
        book = Book.objects.get(isbn=isbn)
        quantity = request.POST.get('quantity')
        print(book)
        total_price = int(book.price) * int(quantity)
        order = Order.objects.create(user_id = request.user.id,total_price = total_price)
        orderitem = OrderItem.objects.create(order=order,book=book,quantity = quantity,price = book.price)
        print(order)
        print(orderitem)
        items = {
            'order':order,
            'orderitem':orderitem
        }
        return render(request, 'successPage.html',{'items':items})
    print('book - order')
    return render(request, 'buy.html',{'books':'buying'})

@login_required
def carting(request,id):
    book = Book.objects.get(id=id)
    print(book)
    cart = CartItem.objects.get_or_create(user_id=request.user.id,book_id = id)
    return render(request, 'cart.html',{'cart':cart})

def addQuantity(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        id = request.POST.get('id')
        if key == 'delete':
            CartItem.objects.filter(id=id).delete()
            return JsonResponse({'status':'deleted'})
        id = request.POST.get('id')
        quantity = request.POST.get('quantity')
        cart = CartItem.objects.get(id=id)
        cart.change_quantity(quantity)
        return JsonResponse({'status':'success'})
    return JsonResponse({'status':'success'})

# @login_required
def cart(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        quantity = request.POST.get('quantity')
        book = Book.objects.get(isbn=isbn)
        print(book)
        cart = CartItem.objects.get_or_create(user_id=request.user.id,book = book)
        cart = cart[0]
        cart.quantity = cart.quantity + int(quantity)
        cart.save()
        print(cart)
        return JsonResponse({'status': book.title + ' has been added to cart successfullfy'})
    cart = CartItem.objects.filter(user_id=request.user.id).annotate(
        total_price=ExpressionWrapper(
            F('book__price') * F('quantity'),
            output_field=FloatField()
        )
    )
    print(cart)
    return render(request, 'cart.html',{'cart':cart})

@login_required
def order(request):
    order = Order.objects.filter(user_id = request.user.id)
    data = []
    for i in order:
        data.append({
            'order':i,
            'orderitem':OrderItem.objects.filter(order=i)
        })
    return render(request, 'order.html',{'orderitem':data})

def booklist(request,degree,department,semester):
    print(degree,department,semester)
    data = Book.objects.filter(department__name = department,department__degree__name = degree,semester = semester)
    print(data)
    return render(request, 'booklist.html',{'data':data})

@login_required(login_url='/login/')
def buyBookPage(request,isbn):
    book = Book.objects.get(isbn = isbn)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        total_price = int(quantity) * book.price
        order = Order.objects.create(user_id = request.user.id,total_price = total_price)
        orderitem = OrderItem.objects.create(order=order,book=book,quantity = quantity,price = book.price)
        return JsonResponse({'status':'Ordered Successfully'})
    print(book,'buy book')
    return render(request, 'buying.html',{'book':book})

def viewBookPage(request,isbn):
    book = Book.objects.get(isbn = isbn)
    print(book,'view book')
    return render(request, 'booklist.html',{'book':book})

def searchbar(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        if key == 'dynamic':
            value = request.POST.get('value')
            book_list = Book.objects.filter( Q(isbn__contains = value) | Q(title__contains = value) | Q(author__contains = value)).values('title','isbn','author')
            data = []
            for book in book_list:
                data.append(book['title'] + ' -- ' + book['author'] + ' -- ' + book['isbn'])
            print(data)
            return JsonResponse(data,safe=False)
        value = request.POST.get('search_book').split('--')
        value = value[2].strip()
        print(value)
        book_list = list(Book.objects.filter(isbn = value).values('title','isbn','author','img','price','semester','year'))
        print(book_list)
    return JsonResponse(book_list,safe=False)


# views.py
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def buy(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        quantity = int(request.POST.get('quantity'))
        book = Book.objects.get(isbn=isbn)
        total_amount = int(book.price) * quantity

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            'amount': total_amount * 100,  # Amount in paisa
            'currency': 'INR',
            'receipt': f'order_{request.user.id}_{isbn}_{quantity}',  # Unique order ID
            'payment_capture': 1  # Auto capture payment
        }
        try:
            # Create Razorpay order
            razorpay_order = client.order.create(data=payment_data)
            order_id = razorpay_order['id']

            # Save order details in session
            request.session['razorpay_order_id'] = order_id
            request.session['total_amount'] = total_amount

            # Render Razorpay payment form
            return render(request, 'payment.html', {'razorpay_order_id': order_id, 'total_amount': total_amount})
        except Exception as e:
            messages.error(request, f'Error initiating payment: {e}')
    
    # Handle GET request or if payment initiation fails
    return redirect('cart')

# views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        razorpay_order_id = request.session.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        total_amount = request.session.get('total_amount')

        # Verify the payment signature (security check)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            # Payment is successful, update your database or process the order here
            # Example: Mark the order as paid
            # order = Order.objects.get(id=your_order_id)
            # order.paid = True
            # order.save()

            messages.success(request, 'Payment successful!')
            return redirect('order_success')  # Redirect to a success page
        except Exception as e:
            messages.error(request, f'Error verifying payment: {str(e)}')
    
    # Handle GET request or if payment verification fails
    return redirect('cart')

def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        status = False
        if User.objects.filter(username=username).exists():
            status = True
        return JsonResponse({'status':status})
