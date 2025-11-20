from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.db.models import Sum, Case, When, IntegerField

# User = get_user_model()

class CustomUser(AbstractUser):
    def calculate_reputation(self):
        result = Vote.objects.filter(tip__author=self).aggregate(reputation=Sum(
            Case(
                When(value=Vote.UPVOTE, then=5),
                When(value=Vote.DOWNVOTE, then=-2),
                default=0,
                output_field=IntegerField(),
            )
        ))
        return result['reputation'] or 0
    
    def get_reputation(self):
        return self.calculate_reputation()
    
    def has_downvote_permission(self):
        return self.calculate_reputation() >= 15 or self.has_perm('protips.can_downvote')
    
    def has_deletion_permission(self):
        return self.calculate_reputation() >= 30 or self.has_perm('protips.delete_tip')

    def __str__(self):
       return f"CustomUser: {self.username} (Reputation: {self.calculate_reputation()})"

class Tip(models.Model):
  content = models.TextField()
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tips')
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-date']
    permissions = [
        ("can_downvote", "Can downvote tips"),
    ]

  def __str__(self):
    return f'Tip by {self.author.username} on {self.date.strftime("%Y-%m-%d %H:%M")} the content: {self.content[:30]}...'
  
  def upvote_count(self):
      return self.votes.filter(value=Vote.UPVOTE).count()
  
  def downvote_count(self):
      return self.votes.filter(value=Vote.DOWNVOTE).count()
  
  @transaction.atomic
  def vote(self, user, value):
      vote, created = Vote.objects.get_or_create(tip=self, user=user, defaults={'value': value})
      if created:
        return "New Vote"
      if vote.value == value:
         vote.delete()
         return "Vote removed"
      else:
          vote.value = value
          vote.save(update_fields=['value'])
          return "Vote updated"
  
class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = [
        (UPVOTE, 'Up vote'),
        (DOWNVOTE, 'Down vote'),
    ]

    tip = models.ForeignKey(Tip, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('tip', 'user')

    def __str__(self):
        return f'Vote by {self.user.username} on Tip ID {self.tip.id}: {"Upvote" if self.value == self.UPVOTE else "Downvote"}'