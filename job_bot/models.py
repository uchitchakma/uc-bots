from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

class JobLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
