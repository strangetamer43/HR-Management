from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
from multiselectfield import MultiSelectField


weekofftype =(
			    ('MO', 'Monday'),
			    ('TU', 'Tuesday'),
                ('WE', 'Wednesday'),
                ('TH', 'Thursday'),
                ('FR', 'Friday'),
                ('SA', 'Saturday'),
                ('SU', 'Sunday'),
			)

class Company(models.Model):
    company_name=models.CharField(max_length=100,null=True,unique=True)
    payroll_date = models.DateField(auto_now_add=False,null=True,blank=True,auto_now=False)
    total_working_days=models.IntegerField(null=True,blank=True)
    ceo_id = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.company_name

class Teams(models.Model):
    company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    team_type = models.CharField(max_length=50,null=True)
    target = models.CharField(max_length=100,null=True,blank=True)
    work_per_day = models.IntegerField(null=True,blank=True)
    work_per_hour = models.IntegerField(null=True,blank=True)
    cal_id= models.CharField(max_length=1000,null=True,blank=True)
    cal_link=models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.team_type)

class Customer(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True,blank=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='images',default="userprofile.png",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    total_leaves = models.IntegerField(null=True,blank=True,default=20)
    casual_leaves = models.IntegerField(null=True,blank=True,default=10)
    sick_leaves = models.IntegerField(null=True,blank=True,default=5)
    optional_leaves = models.IntegerField(null=True,blank=True,default=5)
    status=models.CharField(max_length=200,null=True,default='Not Available')
    team = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(null=True,blank=True,default=1)
    designation = models.CharField(null=True,max_length=100,blank=True)
    works_under=models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True,blank=True)
    salary_to_be_paid = models.IntegerField(null=True,blank=True)

    def __str__(self):
    	return str(self.name)

class Hierarchy(models.Model): 
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE) 
    team_type = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.team_type)


class Leave(models.Model):
    LEAVETYPE = (
			('Casual', 'Casual'),
			('Sick', 'Sick'),
			('Optional', 'Optional'),
			)
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField()
    leave_type = models.CharField(max_length=200, null=True, choices=LEAVETYPE)
    accepted=models.BooleanField(default=False,null=True, blank=True)
    seen=models.BooleanField(default=False,null=True, blank=True)
    applied_at=models.DateField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']

    
    def __str__(self):
        return self.user.name


class Workitems(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    work_title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    date = models.DateField(auto_now=True, auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        return self.user.name


class Timesheet(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    entry = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    break1= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    break1_end= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    meet= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    endmeet= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    systemissue= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    endsystemissue= ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    lunch =ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,blank=True,null=True)
    lunch_end = ArrayField(models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True),default=list,null=True,blank=True)
    out = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.user.name


class PolicyUpdate(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    policy_title = models.CharField(max_length=200, null=True)
    slug=models.SlugField(null=True,blank=True)
    description = models.TextField(null=True)
    time=models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.policy_title)
        super(PolicyUpdate,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.team)

class Event(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    team_type = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    # end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    count=models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    google_link = models.CharField(max_length=150, null=True, blank=True)
    weekoff=MultiSelectField(choices=weekofftype,max_choices=2,default='TU',max_length=20)
    # google link is used to edit events in google if you change them in your website

    def __str__(self):
        return str(self.team_type)


class UserCalender(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    cal_id= models.CharField(max_length=1000,null=True,blank=True)
    cal_link=models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.customer.name)

class User_Event(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    count=models.IntegerField(null=True)
    # end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    google_link = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return str(self.customer.name)


class Template_cal(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    template_name=models.CharField(max_length=50, null=True, blank=True)
    team_type = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    count=models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    google_link = models.CharField(max_length=150, null=True, blank=True)
    

    def __str__(self):
        return str(self.template_name)

class Process(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    process_title=models.CharField(max_length=200,null=True,blank=True)
    start_time=models.DateTimeField(auto_now_add=False,null=True, blank=True)
    end_time=models.DateTimeField(auto_now_add=False,null=True, blank=True)

    def __str__(self):
        return str(self.process_title)

#class for task management
class Task(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    process= models.ForeignKey(Process,on_delete=models.CASCADE, null=True, blank=True)
    sent_by = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    person=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True,related_name='person')
    task_title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    published_at=models.DateTimeField(auto_now_add=False,null=True, blank=True)
    completed=models.BooleanField(null=True, blank=True,default=False)
    end_time=models.DateTimeField(auto_now_add=False,null=True, blank=True)

    class Meta:
       ordering = ('-published_at', )

    def __str__(self):
        return str(self.task_title)

class ReceiverTask(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    task=models.ForeignKey(Task,on_delete=models.CASCADE, null=True, blank=True)
    start_time=models.DateTimeField(auto_now_add=False,null=True, blank=True)
    end_time=models.DateTimeField(auto_now_add=False,null=True, blank=True)

    def __str__(self):
        return str(self.task)


class Ticket(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    sent_by = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True, related_name='sent_by')
    send_to=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    task_title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    completed=models.BooleanField(null=True, blank=True,default=False)
    completed_at=models.DateTimeField(auto_now_add=False,null=True, blank=True)

    def __str__(self):
        return str(self.task_title)


class TicketResponse(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    ticket= models.ForeignKey(Ticket,on_delete=models.CASCADE, null=True, blank=True)
    message=models.TextField(blank=True,null=True)
    sent_by = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True, related_name='sent_by1')
    send_to=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.ticket)

class OverTimeSchedule(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    team_type = models.ForeignKey(Teams,on_delete=models.CASCADE, null=True, blank=True)
    summary = models.CharField(max_length=50)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    no_of_slots=models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    google_link = models.CharField(max_length=150, null=True, blank=True)
    fcfs=models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        # return self.id
        return str(str(self.start_time)+"-"+str(self.end_time))

class SelectOvertime(models.Model):
    company=models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    overtimedate = models.DateField()
    overtime = models.ForeignKey(OverTimeSchedule,on_delete=models.CASCADE, null=True, blank=True)
    person = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    accepted=models.BooleanField(default=False,null=True, blank=True)
    seen=models.BooleanField(default=False,null=True, blank=True)
    

    def __str__(self):
        return str(self.person)



