from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,  ** other_fields)
        user.set_password(password)
        user.save()
        return user


class Domain(models.Model):
    name = models.CharField(max_length=300)
    contestsHeld = models.IntegerField(default=0)


class Contest(models.Model):
    hostingSite = models.CharField(max_length=300)
    participantsRegistered = models.IntegerField(default=0)
    # only register on site
    finished = models.BooleanField(default=False)
    timing = models.DateTimeField()
    domain_contest = models.ForeignKey(
        Domain, on_delete=models.CASCADE, null=True)


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    recentActivity = models.ForeignKey(
        Contest, on_delete=models.SET_NULL, null=True, related_name="recent_activity")
    streak = models.IntegerField(default=0)
    contest_history = models.ManyToManyField(
        Contest, related_name="all_contests")
    domain = models.ManyToManyField(Domain)
    # image = models.ImageField(default='user.png', upload_to='profile_pics')
    # bio = models.TextField(null=True, blank=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.username)


# class Leaderboard(models.Model):
