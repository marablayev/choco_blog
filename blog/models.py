from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _

from account.models import Author
from shared.utils import get_file_path, unique_slug_generator


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slug_generator(self)
        super(Category, self).save(*args, **kwargs)


class Post(models.Model):
    STATUSES = (
        (0, _('Unpublished')),
        (1, _('Published')),
        (2, _('Archived'))
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=get_file_path('media/images'), null=True, \
                              blank=True)
    text = models.TextField()
    publish_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=0, choices=STATUSES)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def rating(self):
        return self.rates.aggregate(Avg('rate')).get('rate__avg', 0)

    def __str__(self):
        return "{} by {}".format(self.title, self.author.username)

    @property
    def label(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slug_generator(self)
        super(Post, self).save(*args, **kwargs)


class Rate(models.Model):
    rate = models.PositiveSmallIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, \
                             related_name='rates')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, \
                               related_name='rates')


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    publish_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
