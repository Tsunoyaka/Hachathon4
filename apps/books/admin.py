from django.contrib import admin
from .models import Book, Rating, Like

admin.site.register([Rating, Like])
admin.site.register(Book)