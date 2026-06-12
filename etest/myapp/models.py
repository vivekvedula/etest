from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_option = models.CharField(max_length=10)

    def __str__(self):
        return self.question_text


# ✅ NEW MODEL (IMPORTANT)
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"