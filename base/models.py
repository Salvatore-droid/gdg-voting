from django.db import models
from django.contrib.auth.models import User

# Candidate Model
class Candidate(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Position Model
class Position(models.Model):
    name = models.CharField(max_length=200, null=True)
    candidates = models.ManyToManyField(Candidate, related_name='positions')  # Many-to-many relationship

    def __str__(self):
        return self.name

# Voter Model
class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    votes = models.ManyToManyField('Vote', related_name='voters')  # Track votes for each position
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return str(self.user)

# Vote Model (to track votes per position)
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name='vote_set')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.voter.user.username} voted for {self.candidate.name} as {self.position.name}"