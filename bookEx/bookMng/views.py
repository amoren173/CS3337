from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# Create your views here.

from .models import MainMenu

def index(request):
    return render(request,
                  'bookMng/index.html',
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
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                  })
def mybooks(request):
    books = Book.objects.filter(username=request.user)

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  })
def book_delete(request, book_id):

    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
