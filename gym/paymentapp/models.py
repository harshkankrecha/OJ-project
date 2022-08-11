from django.db import models

class Subscriber(models.Model):
    first_name=models.CharField(max_length=100,default='')
    last_name=models.CharField(max_length=100,default='')
    plan_name=models.CharField(max_length=100)
    plan_price=models.IntegerField(default=0)

    def __str__(self):
        return self.first_name+' '+self.last_name
        

