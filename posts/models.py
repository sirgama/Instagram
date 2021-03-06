import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid

# Create your models here.


#uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag")
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

   

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="Picture", blank=True)
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    posted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    # comments = models.CharField(max_length=30, blank=True)

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])
    @classmethod
    def search_by_caption(cls,search_term):
        captions = cls.objects.filter(caption__icontains=search_term)
        return captions
    
   
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
    
# class Stream(models.Model):
#     stream_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_user')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
#     date = models.DateTimeField()
    
#     def add_post(sender, instance, *args, **kwargs):
#         post = instance
#         current_user = post.user
#         followers = FollowersCount.objects.all().filter(user=current_user)

#         for follower in followers:
#             stream = Stream(post=post, current_user=follower.follower, date=post.posted, user=current_user)
#             stream.save()
            
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    
class Comments(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.comment} Post'
    
    def save_comment(self):
        self.save()
        
    def delete_comment(self):
        self.delete()
    @classmethod
    def filter_comments_by_post_id(cls, id):
        comments = Comments.objects.filter(post__id=id)
        return comments
        

    class Meta:
        ordering = ["-pk"]
            
# post_save.connect(Stream.add_post, sender=Post)