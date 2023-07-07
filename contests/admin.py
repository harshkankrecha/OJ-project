from django.contrib import admin
from .models import Contest,Question,Submission,Testcases,Score
import time
from django.contrib import admin
from datetime import datetime
from threading import Thread
from .signals import start_contest_signal,end_contest_signal



class ContestAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Save the model object
        super().save_model(request, obj, form, change)

        # Create and start a new thread
        thread = Thread(target=self.schedule_contest, args=(request,obj,))
        thread.start()

    def schedule_contest(self, request,obj):
        # Perform time-consuming operations or background tasks here
        # Access the saved model object (obj) and process the data
        current_time=datetime.now()
        obj_start_time=obj.start_time
        obj_start_time_datetime=datetime(obj_start_time.year, obj_start_time.month, obj_start_time.day, obj_start_time.hour, obj_start_time.minute, obj_start_time.second)
        rem_time=(obj_start_time_datetime-current_time).total_seconds()        
        print(rem_time)
        time.sleep(rem_time)
        self.start_contest(request,obj)
        time.sleep(30)
        self.end_contest(request,obj)

        # Example: Print the object's name
        print(obj.name)
    
    def start_contest(self,request,obj):
    # Code to start the contest
    # Retrieve the contest object based on the contest_id    
        print('contest started')
    # Perform actions to start the contest
        obj.is_active = True
        obj.save()     
        start_contest_signal.send(sender=None,instance=obj)         
        print("signal sent")
    # Any other logic for starting the contest

    def end_contest(self,request,obj):
        # Code to end the contest
        # Retrieve the contest object based on the contest_id       
        # # Perform actions to end the contest
        obj.is_active = False
        obj.save()
        print('contest ended')
        
        # Any other logic for ending the contest

      
       

admin.site.register(Contest, ContestAdmin) 
#admin.site.register(Contest)
admin.site.register(Score)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Testcases)



