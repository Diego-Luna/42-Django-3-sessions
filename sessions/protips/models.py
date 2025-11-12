from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Tip(models.Model):
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-date']

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('tip', 'user')

    def __str__(self):
        return f'Vote by {self.user.username} on Tip ID {self.tip.id}: {"Upvote" if self.value == self.UPVOTE else "Downvote"}'