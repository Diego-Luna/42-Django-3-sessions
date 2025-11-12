from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tip(models.Model):
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-date']

  def __str__(self):
    return f'Tip by {self.author.username} on {self.date.strftime("%Y-%m-%d %H:%M")} the content: {self.content[:30]}...'