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
    book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                  })

def ratebook(request, book_id):
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


def mybooks(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(username=request.user)

        for b in books:
            b.pic_path = b.picture.url[14:]

        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': books,
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
    return render(request, 'bookMng/cart.html', {'cart_items': cart_items, 'total': total})

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

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
