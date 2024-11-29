from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
#cart
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.

from .models import MainMenu
#cart
from .models import CartItem
#Checkout
from .forms import CheckoutForm
from django.contrib import messages

#Comment
from .models import Book, Comment
from .forms import CommentForm
from django.views import View
from django.shortcuts import redirect, render


def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })

def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })

def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():

            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()

            return HttpResponseRedirect('/postbook?submitted=True') #/postbook? <-- GET
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })

def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })

def searchbook(request):
    if request.method == "POST" and request.POST.get('search') != '':
        search = request.POST.get('search')
        books = Book.objects.filter(name__contains=search)
        return render(request,
                  'bookMng/searchresult.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'search': 'Search results for \'' + search + '\''
                  })
    else:
        return HttpResponseRedirect('/displaybooks')


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    comments = book.comments.all()#this helps get all comments relate to book
    book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'comment_form': comment_form,

                  })

def ratebook(request, book_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rate = request.POST.get('rate')
            book = Book.objects.get(id=book_id)
            book.ratings += int(rate)
            book.ratingscount += 1
            book.overallrating = book.ratings/book.ratingscount
            book.save()
            return HttpResponseRedirect('/displaybooks')
        else:
            return HttpResponseRedirect('/displaybooks')
    else:
        return HttpResponseRedirect('/login?next=/')


def mybooks(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(username=request.user)

        if len(books) == 0:
            return render(request,
                          'bookMng/mybooks.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'books': books,
                              'empty': True,
                          })
        else:
            for b in books:
                b.pic_path = b.picture.url[14:]

            return render(request,
                          'bookMng/mybooks.html',
                          {
                              'item_list': MainMenu.objects.all(),
                              'books': books,
                              'empty': False,
                          })
    else:
        return HttpResponseRedirect('/login?next=/')


def book_delete(request, book_id):

    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


# Cart Views
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = CartItem.objects.get_or_create(book=book, user=request.user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return cart_view(request)

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'bookMng/cart.html', {'item_list': MainMenu.objects.all(),'cart_items': cart_items, 'total': total})

def remove_from_cart(request, cart_item_id):
    CartItem.objects.filter(id=cart_item_id, user=request.user).delete()
    return cart_view(request)

def checkout(request):
    # Render a checkout template or handle checkout logic here
    return render(request, 'bookMng/checkout.html', {
        'item_list': MainMenu.objects.all()
    })


def update_cart(request, cart_item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            # If quantity is set to 0 or less, remove the item from the cart
            cart_item.delete()

    return redirect('cart_view')

#checkout
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the checkout form
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            contact_number = form.cleaned_data['contact_number']
            payment_method = form.cleaned_data['payment_method']

            # Placeholder: Save data or integrate with payment gateway
            print(f"Order Details:\nName: {full_name}\nAddress: {address}\nContact: {contact_number}\nPayment: {payment_method}")

            # Clear the cart after successful checkout
            CartItem.objects.filter(user=request.user).delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'bookMng/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    })

def order_success(request):
    return render(request, 'bookMng/order_success.html')

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def comment_form(request, book_id):
    # Fetch the book or return a 404 if not found
    book = get_object_or_404(Book, id=book_id)
    # Get all comments related to the book
    comments = book.comments.all()

    if request.method == 'POST':
        # Handle form submission
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Associate the comment with the book and the user
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            # Redirect to the book detail page after saving
            return redirect('book_detail', book_id=book.id)
    else:
        # Render an empty form for GET requests
        comment_form = CommentForm()

    # Render the template with the book and form context
    return render(request, 'bookMng/post_comment.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comment_form': comment_form,
        'comments': comments,  # Optional: Pass the comments to display them in the template
    })

