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
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
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

from .models import HeatMap, Element, Page

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.core import serializers
# from django.views.generic.list_detail import object_list
from django.db import transaction

import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib import mlab as mlab
from matplotlib.backends.backend_agg import FigureCanvasAgg

import numpy as np
import os
from multiprocessing import Process

PAGE = ['url', 'doc_width', 'doc_height']
PROPERTIES = ['time_entered', 'time_left', 'width', 'height', 'x', 'y']


def clean_value(value):
    value = value.replace('u', '')
    value = value.replace("'", '')
    return value


def generate_screenshot(url):
    '''BUG: webkit2png does not seem to be able to interact with the Django built-in web server, it generates a time out error'''

    url = 'http://google.com'  # Temp workaround to generate charts
    location = os.getcwd() + '/heatmap/html/images/%s.png' % url
    os.system(os.getcwd() + '/heatmap/webkit2png.py -F -o %s %s' % (location, url))
    return url.replace('/', '').replace(':', '').replace('http', '').replace('.', '')


@transaction.atomic
def save_coordinates(elements):
    for element in elements:
        elem = Element()
        element = elements[element]
        keys = element.keys()
        for key in keys:
            setattr(elem, key, element[key])
        elem.url = page
        elem.time_spent = elem.time_left - elem.time_entered
        del elem.time_left
        del elem.time_entered
        elem.save()
    transaction.commit()


def parse_coordinates(raw_data):
    x, y = [], []
    page = {}
    elements = {}
    #print(raw_data)
    for key, value in raw_data.items():
        # print key, value

        if key == 'url':
            value = clean_value(value)
        else:
            value = clean_value(value)
        # print key, value
        if key.startswith('x'):
            x.append(int(value))
        elif key.startswith('y'):
            y.append(int(value))
        elif key.endswith('id'):
            print
            (key, value)
            if value not in elements:
                elements[int(value)] = {}
        elif key in PAGE:
            print
            (key, value)
            page[key] = value


    keys = elements.keys()
    for key in keys:
        for property in PROPERTIES:
            value = raw_data[str(key) + property]
            # print property, value
            value = clean_value(value)
            elements[key][property] = int(value)

    # print x, y
    # print page
    # print elements

    return x, y, page, elements


def to_json(queryset):
    json_serializer = serializers.get_serializer("json")()
    return json_serializer.serialize(queryset, ensure_ascii=False)


def retrieve_heatmap_information(request, id):
    page = HeatMap.objects.filter(name=id)
    data = to_json(page)
    return HttpResponse(data, content_type='application/json')


def retrieve_html_elements(request, id):
    elements = Element.objects.filter(url=id)
    data = to_json(elements)
    return HttpResponse(data, content_type='application/json')


def process_coordinates(post):
    heatmap = HeatMap()
    x, y, doc, elements = parse_coordinates(post)
    #print(x, y, doc, elements)
    url = doc['url']
    post_name = url.split('/')[-2]
    width = doc['doc_width']
    height = doc['doc_height']
    page, created = Page.objects.get_or_create(url=url, defaults={'url': url, 'width': width, 'height': height})
    if created:
        page.save()
    heatmap.url = page
    heatmap.x_coord = x
    heatmap.y_coord = y
    heatmap.name = post_name

    '''
    Screenshot generator is causing a lot of trouble, commenting it out for the time
    '''
    # file = generate_screenshot(page.url)
    # heatmap.file = file

    heatmap.file = ''

    try:
        heatmap.save()
        save_coordinates(elements)
    except:
        return HttpResponseServerError()


def store_coordinates(request):
    print("haha")
    if request.POST:
        process_coordinates(request.POST)
        print(HttpResponse(status=200))
        return HttpResponse(status=200)

    else:
        print(HttpResponse(status=200))
        return HttpResponse(status=200)


def generate_heatmap(request, id):
    heatmap = get_object_or_404(HeatMap, pk=id)
    dpi = 150
    width = heatmap.url.width / dpi
    height = heatmap.url.height / dpi
    gridsize = 30
    x = heatmap.x_coord[1:-1]

    x = x.replace('u', '')
    x = x.replace("'", '')
    x = x.split(',')
    x = [int(i) for i in x]

    y = heatmap.y_coord[1:-1]
    y = y.replace('u', '')
    y = y.replace("'", '')
    y = y.split(',')
    y = [int(i) for i in y]

    X, Y = np.meshgrid(x, y)
    x = X.ravel()
    y = Y.ravel()

    fig = plt.figure(figsize=(width, height), dpi=dpi, facecolor='w', edgecolor='k')

    # ax = fig.add_subplot(111, frame_on=False, alpha=0.5)
    rect = [0, 0, 1, 1]
    ax = fig.add_axes(rect, frameon=False)
    fig.patch.set_alpha(0.3)
    ax.patch.set_alpha(0.3)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

    ax.hexbin(x, y, C=None, gridsize=gridsize, cmap=cm.jet, bins=None, alpha=0.3, edgecolors='none')
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.invert_yaxis()
    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response
