from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Profile
from . import forms
from authentication.forms import EditProfileForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def LikeView(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))

@login_required
@transaction.atomic
def edit_account(request, id):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = forms.EditProfilePageForm(request.POST, instance=request.user.profile)
        profile_pic = forms.EditProfilePageForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #profile_pic.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse('profile', args=[str(id)]))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = forms.EditProfilePageForm(instance=request.user.profile)
    return render(request, 'edit_account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def index(request):
    post_list = Post.objects.filter(status=1).order_by('-created_on')
    return render(request, 'index.html', {'post_list':post_list})

class PostList(generic.ListView):
    queryset = Post.objects.order_by('-created_on')
    context = {'post_list': queryset}
    template_name = 'index.html'
    
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = stuff.get_total_likes()
        context['total_likes'] = total_likes
        return context 

class AddPostView(generic.CreateView):
    model = Post
    form_class = forms.PostForm
    template_name = 'add_post.html'

class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = forms.EditForm

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        post_list = Post.objects.filter(author=get_object_or_404(User, id=self.kwargs['pk']))
        print(self.kwargs['pk'], Post.objects.all())
        context['page_user'] = page_user
        context['post_list'] = post_list
        return context

class AboutView(generic.ListView):
    model = Post
    template_name = 'about.html'

class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'search_results.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        post_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        return post_list