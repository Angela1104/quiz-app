from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    quizzes = models.ManyToManyField('Quiz', related_name='user_profiles', blank=True)  # Add this line

    def __str__(self):
        return self.user.username
    

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    thumbnailUrl = models.CharField(max_length=255, blank=True, null=True)
    background = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(UserProfile, related_name='quizzes_participated', blank=True)  # Add this line

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Question: {self.text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer: {self.text} for Question: {self.question.text}"


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"Score: {self.score}"

class TopScorer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Quiz: {self.quiz}, Score: {self.score}, College: {self.college}, Program: {self.program}"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()