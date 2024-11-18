from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, MainMenu
from .forms import PostForm


def index(request):
    return render(request,
                  'board/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postlist(request):
    posts = Post.objects.all()  # Query all Post objects

    return render(request,
                  'board/postlist.html',
                  {
                      'posts': posts,
                      'item_list': MainMenu.objects.all(),
                  })

    # return render(request, 'postlist.html', {'posts': posts})


def postdetail(request, post_id):
    posts = Post.objects.all()

    return render(request,
                  'board/postdetail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'posts': posts,
                  })

    #post = get_object_or_404(Post, id=post_id)
    #return render(request, 'board/postdetail.html', {'post': post})


def postcreate(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('postlist')
    else:
        form = PostForm()
    return render(request, 'board/postcreate.html', {'form': form})
