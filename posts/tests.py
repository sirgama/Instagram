from django.test import TestCase
from .models import Stream, Likes, Comments, Post, User, Follow
from posts.models import Profile

# Create your tests here.
class PostTestClass(TestCase):
    def setUp(self):
        self.user = User(username='alex')
        self.user.save()
        self.user_profile = Profile(user=self.user,Post="mypic.png")
        self.post = Post(name="views",caption="my views",user=self.user_profile)
        
    def tearDown(self):
        Post.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))
            
    def test_save_post(self):
        self.post.save_Post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)>0)
        
    def test_delete_post(self):
        self.post.save_Post()
        self.post.delete_Post()
        posts=Post.objects.all()
        self.assertTrue(len(posts)==0)   

class CommentsTestClass(TestCase):
    def setUp(self):
        self.user = User(username='alex')
        self.user.save()
        self.user_Profile = Profile(user=self.user,Post="mypic.png")
        self.post = Post(name="views",caption="my views",user=self.user_Profile)
        self.post.save()
        self.comment = Comments(comment="Awsome",post=self.post,user=self.user)
        
    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()
        Comments.objects.all().delete()
        Profile.objects.all().delete()
                    
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comments))

    def test_delete_comment(self):
        self.comment.save_comment()
        self.comment.delete_comment()
        comments=Comments.objects.all()
        self.assertTrue(len(comments)==0) 

    def test_save_comment(self):
        self.comment.save_comment()
        comments=Comments.objects.all()
        self.assertTrue(len(comments)>0)

class ProfileTestClass(TestCase):
    def setUp(self):
        self.user = User(username='alex')
        
        self.user_Profile = Profile(user=self.user,Post="mypic.png")
   
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
      
    def test_instance(self):
        self.assertTrue(isinstance(self.user_Profile,Profile))
            
    def test_save_user_Profile(self):
        self.user_Profile.save_Profile()
        Profiles=Profile.objects.all()
        self.assertTrue(len(Profiles)>0)