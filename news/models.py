from linecache import cache

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


# Модель Author
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = sum(post.rating * 3 for post in self.post_set.all())
        comments_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        author_comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        self.rating = posts_rating + comments_rating + author_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='post_cat_name')

    def __str__(self):
        return f'{self.name}'

# Модель UserCategory
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель Post
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    POST_TYPE_CHOICES = [
        ('article', 'Article'),
        ('news', 'News')
    ]
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.created_at}+{self.title}+{self.text}+{self.post_type}+{self.rating}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def get_absolute_url(self):
        return reverse('onepost', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')


# Модель PostCategory
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text}+{self.created_at}+{self.rating}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

