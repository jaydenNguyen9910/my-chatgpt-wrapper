from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    conversation_id = models.TextField(null=True, default=None)
    account_id = models.IntegerField(default=0)
