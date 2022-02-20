from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

import os


def profile_picture_path(instance, filename):
    # return f'profile_pictures/user_{instance.id}/{filename}'
    return os.path.join('profile_pictures', 'user_%s' % instance.id, filename)


class User(AbstractUser):
    GENDER_CHOICE_MALE = 'male'
    GENDER_CHOICE_FEMALE = 'female'

    GENDER_CHOICES = (
        (GENDER_CHOICE_MALE, 'Male'),
        (GENDER_CHOICE_FEMALE, 'Female')
    )

    email = models.EmailField(_('Email'), unique=True)
    profile_picture = models.ImageField(_('Profile Picture'), upload_to=profile_picture_path, null=True, blank=True)

    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    gender = models.CharField(_('Gender'), choices=GENDER_CHOICES, default=None, max_length=10, null=True, blank=True)

    class Meta:
        ordering = ('username',)

    @property
    def full_name(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'.strip()
        return '%s' % self.username

    @property
    def age(self):
        if self.date_of_birth:
            from users.utils import calculate_age
            return calculate_age(self.date_of_birth)
        return None

    def save(self, *args, **kwargs):
        self.name = f'{self.first_name} {self.last_name}'.strip()
        if not self.pk:
            saved_image = self.profile_picture
            self.profile_picture = None
            super(self.__class__, self).save(*args, **kwargs)
            self.profile_picture = saved_image
        super(self.__class__, self).save(*args, **kwargs)
