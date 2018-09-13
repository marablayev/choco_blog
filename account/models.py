from django.db import models

from django.contrib.auth.models import User

from shared.utils import get_file_path


class Author(User):
    photo = models.ImageField(upload_to=get_file_path('media/images'), null=True, \
                              blank=True)
