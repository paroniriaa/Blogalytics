from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.

def index(request):
    post_list = Post.objects.filter(status=1).order_by('-created_on')
    return render(request, 'index.html', {'post_list':post_list})

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context = {'post_list': queryset}
    template_name = 'index.html'
    
class AddPostView(generic.CreateView):
    exclude = ['post_id']
    model = Post
    fields = '__all__'
    template_name = 'add_post.html'