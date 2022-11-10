from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from slugify import slugify
from .utils import get_time


User = get_user_model()


class Book(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft')
    )

    user = models.ForeignKey(
        verbose_name='Опубликовано',
        to=User,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    title = models.CharField(max_length=200,verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    language = models.CharField(max_length=50,verbose_name='Язык книги', default='Русский')
    page = models.SmallIntegerField(verbose_name='Страниц')
    image = models.ImageField(upload_to='post_images')
    genre = models.CharField(max_length=100,verbose_name='Жанр')
    slug = models.SlugField(max_length=250,primary_key=True, blank=True)
    desc = models.TextField(verbose_name='Описание')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('created_at', )

    def get_adsolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.post.title}'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, 
        blank=True, 
        null=True)
    post = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'

