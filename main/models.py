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

    def __str__(self):
        return str(self.name)


class Contest(models.Model):
    hostingSite = models.CharField(max_length=300)
    participantsRegistered = models.IntegerField(default=0)
    ref = models.CharField(max_length=300, blank=True)
    # only register on site
    name = models.CharField(max_length=300, blank=True)
    finished = models.BooleanField(default=False)
    timing = models.DateTimeField()
    domain_contest = models.ForeignKey(
        Domain, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.hostingSite)


class User(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=100 , default="Unknown")
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    recentActivity = models.ForeignKey(
        Contest, on_delete=models.SET_NULL, null=True, related_name="recent_activity")
    user_points = models.IntegerField(default=0)
    contest_history = models.ManyToManyField(
        Contest, related_name="all_contests", blank=True)
    domain = models.ManyToManyField(Domain)

    # image = models.ImageField(default='user.png', upload_to='profile_pics')
    # bio = models.TextField(null=True, blank=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.username)


class Handle(models.Model):
    handleName = models.CharField(max_length=150)
    handle_domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.handleName)


class Points(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    alloted = models.BooleanField(default=False)


class Time(models.Model):
    time = models.DateTimeField(auto_now=True)
    updater = models.IntegerField(default=0)
