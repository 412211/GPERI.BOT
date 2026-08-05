from django.db import models

# Create your models here.

class QuestionSetMaster(models.Model):
    
    Title = models.CharField(max_length=1000)
    
    
    def save(self, *args, **kwargs):
        self.Title = self.Title.upper()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.Title
    
class AnswerSetMaster(models.Model):
    
    Question = models.ForeignKey(QuestionSetMaster,on_delete=models.CASCADE,null=True)
    Title = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.Title
    
    
class User(models.Model):
    
    Name = models.CharField(max_length=20)
    Contact = models.CharField(max_length=12,unique=True,null=True)
    Email = models.EmailField()
    Password = models.CharField(max_length=8)
    Status = models.BooleanField(default=True)
    
    def __str__(self):
        return super().__str__()
    

class TempChatMaster(models.Model):
    
    Temptoken = models.IntegerField()
    Message = models.CharField(max_length=1000)
    Type = models.CharField(max_length=1000)
    UserId = models.IntegerField()
 
 
    def __str__(self):
        return super().__str__()

class QADataSet(models.Model):
    Question = models.ForeignKey(QuestionSetMaster,on_delete=models.CASCADE,null=True)
    Answer = models.ForeignKey(AnswerSetMaster,on_delete=models.CASCADE,null=True)
    