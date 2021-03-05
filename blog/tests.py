import time
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.urls import reverse

# Create your tests here.

def create_user():
    user = User.objects.create_user(username="test_name", email="test_email@mail.com", password="test_password")
    return user

def create_post(user, title, content):  
    post = Post.objects.create(title=title, content=content, author=user, status=1)
    return post

class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(self):
        print("setUp: Run once for every test method to setup clean data.")
        self.user = create_user()      
        self.post = create_post(title='test title', content="test content", user=self.user)

    def test_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, self.post.title)

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        post_title_length = post._meta.get_field('title').max_length
        self.assertEqual(post_title_length, 200)

    def test_slug_max_length(self):
        post = Post.objects.get(id=1)
        post_slug_length = post._meta.get_field('slug').max_length
        self.assertEqual(post_slug_length, 200)

    def test_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.content, self.post.content)

    def test_author(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.author.username, self.post.author.username)
    
    def test_status(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.status, self.post.status)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), self.post.get_absolute_url())



class PostPostListTests(TestCase):

    def test_accessability(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_accessability_about(self):
        self.client.get(reverse('home'))
        response = self.client.get(reverse('about'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_redirect_accessability_add_post(self):
        self.client.get(reverse('home'))
        response = self.client.get(reverse('add_post'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_html_template_correstness(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'index.html')

    def test_no_post(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "It seems like there are no post yet, do you want to be the first one?")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_one_post(self):
        user = create_user()
        post_1 = create_post(title='post 1', content='post 1 content', user=user)

        response = self.client.get(reverse('home'))       
        seen_post_list = response.context['post_list']
        self.assertEqual(seen_post_list[0], post_1)

    def test_few_post(self):
        user = create_user()
        post_1 = create_post(title='post 1', content='post 1 content', user=user)
        time.sleep(0.01)
        post_2 = create_post(title='post 2', content='post 2 contnet', user=user)
        time.sleep(0.01)
        post_3 = create_post(title='post 3', content='post 3 content', user=user)

        post_list = []
        post_list.append(post_3)
        post_list.append(post_2)
        post_list.append(post_1)

        response = self.client.get(reverse('home'))        
        seen_post_list = response.context['post_list']
        
        self.assertEqual(seen_post_list[0], post_list[0])
        self.assertEqual(seen_post_list[1], post_list[1])
        self.assertEqual(seen_post_list[2], post_list[2])
        
        #self.assertQuerysetEqual(response.context['post_list'], ['<Post: post 3>', '<Post: post 2>', '<Post: post 1>'])



class PostPostDetailTests(TestCase):
    @classmethod
    def setUpTestData(self):
        print("setUp: Run once for every test method to setup clean data.")
        self.user = create_user()      
        self.post = create_post(title='test title', content="test content", user=self.user)

    def test_accessability(self):
        response = self.client.get('/test-title/')
        self.assertEqual(response.status_code, 200)

    def test_html_template_correstness(self):
        response = self.client.get('/test-title/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'post_detail.html')
    
    def test_page_elements(self):
        response = self.client.get('/test-title/')
        self.assertEqual(response.status_code, 200)

        seen_post = response.context['post']
        self.assertEqual(seen_post, self.post)
        self.assertEqual(seen_post.title, self.post.title)
        self.assertEqual(seen_post.content, self.post.content)
        self.assertEqual(seen_post.author, self.post.author)


class PostAboutViewTests(TestCase):

    def test_accessability(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
    
    def test_html_template_correstness(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'about.html')

    def test_page_elements(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], [])
        self.assertContains(response, "Hey there! ")
        self.assertContains(response, "A letter from blogalytics developers")
        self.assertContains(response, "As you have already known, Blogalytics is a blog platform.")



class PostAddPostViewTests(TestCase):
    
    def test_add_post_functionaility(self):
        user = create_user()
        new_post_info = {
            'title' : 'new post title',
            'slug' : 'new post slug',
            'content' : "new post content",
            'author' : user.username,
            'status' : 1
        }

        response = self.client.post(reverse('add_post'), post_form=new_post_info)
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "new post content")
        #post = Post.objects.get(id=1)
        
        #self.assertEqual(post.title, new_post_info.title)
        #post = Post.objects.get(id=1)
        #self.assertFormError(response, post.is_valid())

        #self.assertEqual(response.status_code, 200)
        #self.assertQuerysetEqual(response.context['post_list'], [])















        







