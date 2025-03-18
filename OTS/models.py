# from django.db import models

# class Candidate(models.Model):
#     username=models.CharField(primary_key=True,max_length=20)
#     password=models.CharField(null=False,max_length=20)
#     name=models.CharField(null=False,max_length=30)
#     test_attempted=models.IntegerField(default=0)
#     points=models.FloatField(default=0.0)

#     def __str__(self):
#         return f"Registration Successful for {self.username}"



# class Question(models.Model):
#     qid=models.BigAutoField(primary_key=True,auto_created=True)
#     que=models.TextField()
#     a=models.CharField(max_length=255)
#     b=models.CharField(max_length=255)
#     c=models.CharField(max_length=255)
#     d=models.CharField(max_length=255)
#     ans=models.CharField(max_length=2)
# class Result(models.Model):
#     resultid=models.BigAutoField(primary_key=True,auto_created=True)
#     username=models.ForeignKey(Candidate,on_delete=models.CASCADE)
#     date=models.DateField(auto_now=True)
#     time=models.TimeField(auto_now=True)
#     attempt=models.IntegerField()
#     right=models.IntegerField()
#     wrong=models.IntegerField()
#     points=models.IntegerField()


from django.db import models
from django.contrib.auth.hashers import make_password

class Candidate(models.Model):
    username = models.CharField(primary_key=True, max_length=20, unique=True)
    password = models.CharField(max_length=255)  # Use a longer max_length for passwords
    name = models.CharField(max_length=30)
    test_attempted = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)

    def set_password(self, password):
        self.password = make_password(password)

    def __str__(self):
        return self.username

class Question(models.Model):
    qid = models.BigAutoField(primary_key=True, auto_created=True)
    que = models.TextField()
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=2)

    def __str__(self):
        return self.que

class Result(models.Model):
    resultid = models.BigAutoField(primary_key=True, auto_created=True)
    username = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='results')
    date = models.DateField(auto_now=True)  # Use auto_now_add instead of auto_now
    time = models.TimeField(auto_now=True)
    attempt = models.IntegerField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    points = models.IntegerField()


    def __str__(self):
        return f"{self.username.username} - {self.date}"