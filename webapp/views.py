from django.shortcuts import render,HttpResponse
from .models import *

from django.shortcuts import render, redirect 

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import datetime
from .forms import *
import json

from django.contrib.auth.decorators import login_required
from json import dumps
from .calendar_API import test_calendar
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url='login')
def sec_to_day(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    s=str(hour)+":"+str(minutes)+":"+str(seconds)
    return s


def registerPage(request):
    form = CreateUserForm()
    cform=CompanyForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        cform=CompanyForm(request.POST)
        if form.is_valid() and cform.is_valid() :
            user = form.save()
            comform=cform.save()
            # comform.payroll_date=datetime.datetime.now().date()
            comform.save()
            # user = form.save(commit=False)
            user.is_staff=True
            # user.company=comform.company_name
            user.save()            

            k=Customer.objects.create(user=user,name=user.username,email=user.email,company=comform)
            comform.ceo_id = k.id
            comform.save()
            try:
                user_group = Group.objects.get(name='Manager')
                user.groups.add(user_group)
            except:
                pass
            messages.success(request, 'Manager Account was created for ' + user.username)
            return redirect('login')
    context = {'form':form,'cform':cform}
    return render(request, 'register.html', context)  

@login_required(login_url='login')
def clientregisterPage(request):
    if request.user.is_authenticated:
        form = CreateUserForm()
        manager=request.user.customer
        team=Teams.objects.filter(company=manager.company)
        print(team)
        head=Customer.objects.filter(company=manager.company)
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            design=request.POST['designation']
            salary=request.POST['salary']
            tea=request.POST['team']
            wu=request.POST['worksunder']
            print(")))))))))))))))))))))))))))))))))))")
            print(tea,wu)
            tea=Teams.objects.get(id=tea)
            wu=Customer.objects.get(id=wu)
            if form.is_valid():
                user = form.save()
                # print(design)
                Customer.objects.create(user=user,team=tea,works_under=wu,name=user.username,email=user.email,company=manager.company,designation=design,salary=salary)
                messages.success(request, ' Account was created for ' + user.username)
                return redirect('clientregister')
        context = {'form':form,'team':team,'worksunder':head}
        return render(request, 'clientregister.html', context)  
    return redirect('login')


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')

	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or password is incorrect')

		context = {}
		return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    customer = request.user.customer
    form = WorkItemForm()	
    cust=Customer.objects.get(id=customer.id)			
    if request.method == 'POST':
        form = WorkItemForm(request.POST)
        if form.is_valid():
            k= form.save(commit=False)
            cust.save()
            k.user=request.user.customer
            k.company=customer.company
            print(k)
            k.save()
            messages.success(request, 'Work Submitted')
            return redirect('home')
    context = {'form':form,'cust':cust}
    return render(request, 'base.html',context)


@login_required(login_url='login')
def leave(request):
    form=LeaveForm()
    customer=request.user.customer
    cust=Customer.objects.get(id=customer.id)

    if request.method=="POST":
        form=LeaveForm(request.POST)
        if form.is_valid():
           k= form.save(commit=False) 

           dateobj = Leave.objects.filter(date=k.date,user=customer)
           if len(dateobj)>0:
               print("date already exists")
               messages.warning(request, 'Leave already exists for this date')
               return redirect('leave')

           if k.leave_type=="Casual":
            if cust.casual_leaves<=0:
                messages.error(request, 'No Casual Leaves left')
                return redirect('leave')
            # else:
            #     cust.casual_leaves-=1
            #     cust.total_leaves-=1
           elif k.leave_type=="Sick":
            if cust.sick_leaves<=0:
                messages.error(request, 'No Sick Leaves left')
                return redirect('leave')
            # else:
            #     cust.sick_leaves-=1
            #     cust.total_leaves-=1
           elif k.leave_type=="Optional":
            if cust.optional_leaves<=0:
                messages.error(request, 'No Optional Leaves left')
                return redirect('leave')
            # else:
            #     cust.optional_leaves-=1
            #     cust.total_leaves-=1

        cust.save()

        k.user=request.user.customer
        k.company=request.user.customer.company
        k.save()

        messages.success(request, 'Leave Submitted')

    return render(request,'leaves.html',{'form':form,'cust':cust})

@login_required(login_url='login')
def input(request):
    try:
        if request.method=="POST":
            customer=Customer.objects.get(user=request.user)
            reason=request.POST['reason']
            user=request.user.customer
            time=datetime.datetime.now().time().strftime("%H:%M:%S")
            k=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            today=datetime.date.today()
         
            if reason=='login':
                ob=Timesheet(date=today,entry=time,user=user)
                customer.status="Available"
            elif reason=='break':
                ob=Timesheet.objects.get(date=today,user=user)
                
                l=ob.break1
                l.append(time)
                ob.break1=l
                customer.status="On Break" 
            elif reason=='endbreak':
                ob=Timesheet.objects.get(date=today,user=user) 
                   
                l=ob.break1_end
                l.append(time)
                ob.break1_end=l
                customer.status="Available"
            elif reason=='meet':
                ob=Timesheet.objects.get(date=today,user=user)
                
                l=ob.meet
                l.append(time)
                ob.meet=l
                customer.status="In meet"    
            elif reason=='endmeet':
                ob=Timesheet.objects.get(date=today,user=user)
                    
                l=ob.endmeet
                l.append(time)
                ob.endmeet=l
                customer.status="Available"
                 
            elif reason=='systemissue':
                ob=Timesheet.objects.get(date=today,user=user)
                
                l=ob.systemissue
                l.append(time)
                ob.systemissue=l
                customer.status="Not Available" 
                
            elif reason=='endsystemissue':
                ob=Timesheet.objects.get(date=today,user=user)
                    
                l=ob.endsystemissue
                l.append(time)
                ob.endsystemissue=l
                customer.status="Available"
            elif reason=='lunch':
                ob=Timesheet.objects.get(date=today,user=user)
                
                l=ob.lunch
                l.append(time)
                ob.lunch=l
                customer.status="On Break" 
            elif reason=='endlunch':
                ob=Timesheet.objects.get(date=today,user=user)
                
                l=ob.lunch_end
                l.append(time)
                ob.lunch_end=l
                customer.status="Available" 
            elif reason=='out':
                ob=Timesheet.objects.get(date=today,user=user)
                customer.status="Logged Out"
                ob.out=time
            ob.save()
            customer.save()

            dataJSON=dumps({'time':str(k),'status':customer.status})
            return render(request,'index.html',{'ob':ob,'data':dataJSON}) 
        today=datetime.date.today()  
        ob=Timesheet.objects.get(date=today,user=request.user.customer)
        flag=0
        dataJSON=dumps({'time':flag})
        return render(request,'index.html',{'data':dataJSON})

    except Timesheet.DoesNotExist:
        print("Exception ------------------")
        flag='User just entered'
        dataJSON=dumps({'status':flag})
        return render(request,'index.html',{'data':dataJSON})

@login_required(login_url='login')
def time_diff(start_time,end_time):
    # convert time string to datetime
    print('::::::::::::::::::::::::::::::::::::')
    print(start_time,end_time)
    t1 = datetime.datetime.strptime(start_time, "%H:%M:%S")
    print('Start time:', t1.time())

    t2 = datetime.datetime.strptime(end_time, "%H:%M:%S")
    print('End time:', t2.time())

    # get difference
    delta = t2 - t1
    print(delta)

    # time difference in seconds
    print(f"Time difference is {delta.total_seconds()} seconds")

    return int(delta.total_seconds())

@login_required(login_url='login')
def date_time_diff(start_time,end_time):
    # start time
    # convert time string to datetime
    start_time=start_time.replace('-',':')
    end_time=end_time.replace('-',':')

    t1 = datetime.datetime.strptime(start_time, "%Y:%m:%d")
    print('Start date:', t1)
    t2 = datetime.datetime.strptime(end_time, "%Y:%m:%d")
    print('End date:', t2)
    # get difference
    delta = t2 - t1

    # time difference in seconds
    print(f"days difference is {delta.days} days")

    # return int(delta.days)
    return delta

@login_required(login_url='login')
def prod_time(request,date):
    try:
        ob = Timesheet.objects.get(user=request.user.customer,date=date)
        print(ob)
        s = 0
        bt=0
        mt=0
        lt=0
        si=0
        s = (time_diff(str(ob.entry),str(ob.out)))
        for i in range(len(ob.break1)):
            bt= time_diff(str(ob.break1[i]),str(ob.break1_end[i]))
        for i in range(len(ob.lunch)):
            lt= time_diff(str(ob.lunch[i]),str(ob.lunch_end[i]))
        for i in range(len(ob.systemissue)):
            si= time_diff(str(ob.systemissue[i]),str(ob.endsystemissue[i]))
        for i in range(len(ob.meet)):
            mt= time_diff(str(ob.meet[i]),str(ob.endmeet[i]))
        
        s-=(bt+lt+si)
        l=[s,bt,lt,si,mt]
        # t=str(int(s//3600))+":"+str(int(s//60))+ ":"+ str(int(s%60))
        return l
    except Timesheet.DoesNotExist:
        print("Object does not exist")
        return [0,0,0,0,0]

@login_required(login_url='login')
def status(request):
    customers=Customer.objects.filter(company=request.user.customer.company)
    return render(request,'status.html',{'customers':customers})

@login_required(login_url='login')
def policy(request):
    customer=Customer.objects.get(user=request.user)
    policyobj=PolicyUpdate.objects.filter(team=customer.team)[::-1]
    context={'policy':policyobj}
    return render(request,'policy.html',context)

@login_required(login_url='login')
def policyview(request,slug):
    policy=PolicyUpdate.objects.filter(slug=slug)
    return render(request,'policyview.html',{'policy':policy})

@login_required(login_url='login')
def policy_admin(request):
    form = PolicyForm(request=request)
    if request.method == 'POST':
        form = PolicyForm(request.POST,request=request)
        if form.is_valid():
            k= form.save(commit=False)
            k.customer = request.user.customer
            k.company = request.user.customer.company
            k.save()
            return redirect('policy_admin')
    return render(request,'policy_admin.html',{'form':form})

@login_required(login_url='login')
def analytics(request):
    obj = Timesheet.objects.filter(user=request.user.customer)
    today = str(request.user.customer.company.payroll_date)
    print(today)
    year = int(today[:4])
    day = int(today[8:]) 
    count = 0
    month=int(str(datetime.datetime.now().date())[5:7])
    print(month)
    
    for i in obj:
        date = str(i.date)
        yr = int(date[:4])
        # print(yr)
        mo = int(date[5:7])
        # print(mo)
        d = int(date[8:])
 
        if mo == month and yr >= year:
            if d>=day:
                count+=1
            else:
                break

    if request.method=='POST':
        from_date=request.POST['from']
        to=request.POST['to']
        print(from_date,to)
        casual = 0
        sick = 0
        optional = 0
        total_leaves_taken = Leave.objects.filter(user=request.user.customer).filter(date__range=[from_date,to])
        total_leaves_count=len(total_leaves_taken)
        for i in range(len(total_leaves_taken)):
            if(total_leaves_taken[i].leave_type=="Casual"):
                casual+=1
            elif(total_leaves_taken[i].leave_type=="Sick"):
                sick+=1
            elif(total_leaves_taken[i].leave_type=="Optional"):
                optional+=1
        print(total_leaves_taken)
        workitems = len(Workitems.objects.filter(user=request.user.customer).filter(date__range=[from_date,to]))
        tasks = len(Task.objects.filter(person=request.user.customer,completed=True).filter(end_time__range=[from_date,to]))
        ticket = len(Ticket.objects.filter(sent_by=request.user.customer,completed=True).filter(completed_at__range=[from_date,to]))

        workitems+=tasks+ticket
        print("??????????????????????????????????????????????????????????")
        print(tasks,ticket)
        total_days_worked=len(Timesheet.objects.filter(user=request.user.customer).filter(date__range=[from_date,to]))
        from_date=from_date.replace('-',':')
        to=to.replace('-',':')
        target_perday,target_perhour=0,0
        diff=date_time_diff(from_date,to).days
        if(diff==30):
            team = request.user.customer.team
            print(team)
            ob= Teams.objects.get(team_type=team)
            target_perday = ob.work_per_day
            target_perhour = ob.work_per_hour
        date=datetime.datetime.strptime(from_date, '%Y:%m:%d')
        print('------------',diff)
        productive_time,break_time,launch_time,systemissue,meet_time=0,0,0,0,0
        while(diff>=0):
            diff-=1
            k=str(date)
            k=k[:]
            a=prod_time(request,k[:10])
            productive_time=productive_time+ a[0]
            break_time+=a[1]
            launch_time+=a[2]
            systemissue+=a[3]
            meet_time+=a[4]
            date+=datetime.timedelta(days=1)
        h=0
        hour =  productive_time// 3600
        if hour==0:
            h=1
            hour=1
        work_items_per_hour=workitems/hour
        if h==1:
            work_items_per_hour=0
            h=0 
            hour=0
        h=0
        if total_days_worked==0:
            h=1
            total_days_worked=1
        workitems_ratio=workitems//total_days_worked
        if h==1:
            workitems_ratio=0
            h=0
            total_days_worked=0

        productive_time = str(productive_time//3600)+":"+str((productive_time%3600)//60)+":"+str((productive_time%3600)%60)
        break_time = str(break_time//3600)+":"+str((break_time%3600)//60)+":"+str((break_time%3600)%60)
        meet_time = str(meet_time//3600)+":"+str((meet_time%3600)//60)+":"+str((meet_time%3600)%60)
        systemissue = str(systemissue//3600)+":"+str((systemissue%3600)//60)+":"+str((systemissue%3600)%60)

        
        label=['productive_time','breaktime','meettime','systemtime']
        data=[productive_time,break_time,meet_time,systemissue]
        
        context = {'workitems_ratio':workitems_ratio,'workitems':workitems,'time':productive_time,
        'target_perday':target_perday,'target_perhour':target_perhour,
        'breaktime':break_time,'meettime':meet_time,'systemtime':systemissue,
        'casual':casual,'sick':sick,'optional':optional,'total_days_worked':total_days_worked,
        'total_leaves_count':total_leaves_count,'label':label,'datas':data,'work_items_per_hour':work_items_per_hour,'count':count}

        return render(request,'analytics.html',context)

    return render(request,'analytics.html',{'count':count})

# @login_required(login_url='login')
def demo(request):
    results = test_calendar()
    context = {"results": results}
    return render(request, 'demo1.html', context)

@login_required(login_url='login')
def teams(request):
    form = TeamsForm()
    if request.method == 'POST':
        form = TeamsForm(request.POST)
        if form.is_valid():
            k=form.save(commit=False)
            k.company=request.user.customer.company
            k.save()
            messages.success(request, 'Form Submitted')
    context = {'form':form}
    return render(request,'teams.html',context)

@login_required(login_url='login')
def profileSettings(request):
    customer=request.user.customer
    print(customer.id)
    try:
        obj = Hierarchy.objects.get(team_type=request.user.customer.team)	
    except:
        obj=None			
    form = CustomerForm(instance=customer)				
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form,'customer':customer,'obj':obj}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def calender(request):
    customer=request.user.customer
    try:
        teamlink=customer.team.cal_link
    except:
        print("No Team Calendar")
        teamlink='#'
    try:
        obj=UserCalender.objects.get(customer=customer)
        percallink=obj.cal_link
    except:
        percallink='#'
        print("No personel calendar exists")
    
    context={'teamcal':teamlink,'percal':percallink}
    return render(request,'calender.html',context)

@login_required(login_url='login')
def events(request):
    temp=Template_cal.objects.filter(company=request.user.customer.company)
    context = {'template':temp}
    return render(request,'events.html',context)

@login_required(login_url='login')
def custom_events(request):
    tempname=request.GET.get('temp1')
    obj=Template_cal.objects.get(template_name=tempname,company=request.user.customer.company)
    form=EventForm(instance=obj,request=request)
    if request.method == 'POST':
        form = EventForm(request.POST,request=request)
        if form.is_valid():
            k = form.save(commit=False)
            k.company = request.user.customer.company
            k.save()
            messages.success(request, 'Event Submitted')
            return redirect('events')
    context = {'form':form}
    return render(request,'custom_event.html',context)

@login_required(login_url='login')
def overtime_events(request):
    form=OverTimeForm(request=request)
    if request.method == 'POST':
        form = OverTimeForm(request.POST,request=request)
        if form.is_valid():
            k=form.save(commit=False)
            k.company=request.user.customer.company
            k.save()
            messages.success(request, 'Overtime Schedule Submitted')
            return redirect('overtime_events')
    context = {'form':form}
    return render(request,'overtime_events.html',context)

@login_required(login_url='login')
def select_overtime(request):
    customer = request.user.customer
    form=SelectOvertimeForm(user=customer)

    if request.method == 'POST':
        form = SelectOvertimeForm(request.POST,user=customer)
        if form.is_valid():
            k= form.save(commit=False)
            k.company=request.user.customer.company
            # k.overtimedate=datetime.datetime.now()
            print('______________________________________________________________________')
            l=k.overtime
            try:
                obj = SelectOvertime.objects.get(person=customer,overtime=l)
                print(obj)
                messages.error(request, 'You have already applied for this overtime')
                return redirect('select_overtime')
            except:
                print(l.id)
                ob= OverTimeSchedule.objects.get(id=l.id)
                if ob.fcfs:
                    ob.no_of_slots=ob.no_of_slots-1
                    ob.save()
                    k.seen=True
                    k.accepted=True
                k.save()
                messages.success(request, 'Overtime Request Submitted')
                return redirect('select_overtime')
    context = {'form':form}
    return render(request,'select_overtime.html',context)

@login_required(login_url='login')
def ajax_load_overtime(request):
    team_id = request.GET.get('team')
    print(type(team_id))
    persons = OverTimeSchedule.objects.filter(start_date=team_id,company=request.user.customer.company)
    return render(request, 'ajax_load_overtime.html', {'persons': persons})

#funtion to view analytics of a particular user
@login_required(login_url='login')
def admin_view(request):    
    if request.user.is_staff:
        user = Customer.objects.all()
        if request.method == 'POST':
            user1 = request.POST.get('user')
            print("@@#$%%%%")
            print(user1)
            from_date=request.POST['from']
            to=request.POST['to']
            print(from_date,to)
            casual = 0
            sick = 0
            optional = 0
            total_leaves_taken = Leave.objects.filter(user=request.user.customer).filter(date__range=[from_date,to])

            total_leaves_count=len(total_leaves_taken)
            for i in range(len(total_leaves_taken)):
                if(total_leaves_taken[i].leave_type=="Casual"):
                    casual+=1
                elif(total_leaves_taken[i].leave_type=="Sick"):
                    sick+=1
                elif(total_leaves_taken[i].leave_type=="Optional"):
                    optional+=1
            print(total_leaves_taken)
            workitems = len(Workitems.objects.filter(user=request.user.customer).filter(date__range=[from_date,to]))
            total_days_worked=len(Timesheet.objects.filter(user=request.user.customer).filter(date__range=[from_date,to]))
            
            from_date=from_date.replace('-',':')
            to=to.replace('-',':')
            diff=date_time_diff(from_date,to).days
            temp = diff
            date=datetime.datetime.strptime(from_date, '%Y:%m:%d')
            print('------------',diff)
            productive_time,break_time,launch_time,systemissue,meet_time=0,0,0,0,0
            while(diff>=0):
                diff-=1
                k=str(date)
                k=k[:]
                a=prod_time(request,k[:10])
                productive_time=productive_time+ a[0]
                break_time+=a[1]
                launch_time+=a[2]
                systemissue+=a[3]
                meet_time+=a[4]
                date+=datetime.timedelta(days=1)
            target_perday=0
            target_perhour=0
            if(temp==30):
                user2=Customer.objects.get(id=int(user1))
                ob= Teams.objects.get(team_type=user2.team)
                target_perday = ob.work_per_day
                target_perhour = ob.work_per_hour
            h=0
            hour = productive_time// 3600
            if hour==0:
                h=1
                hour=1
            work_items_per_hour=workitems/hour
            if h==1:
                work_items_per_hour=0
                h=0 
                hour=0
            h=0
            if total_days_worked==0:
                h=1
                total_days_worked=1
            workitems_ratio=workitems//total_days_worked
            if h==1:
                workitems_ratio=0
                h=0
                total_days_worked=0

            label=['productive_time','breaktime','meettime','systemtime']
            data=[productive_time,break_time,meet_time,systemissue]

            context = {'workitems_ratio':workitems_ratio,'workitems':workitems,'time':productive_time,
            'breaktime':break_time,'meettime':meet_time,'systemtime':systemissue,
            'casual':casual,'sick':sick,'optional':optional,'total_days_worked':total_days_worked,
            'total_leaves_count':total_leaves_count,'label':label,'datas':data,'work_items_per_hour':work_items_per_hour,
            'target_perday':target_perday,'target_perhour':target_perhour}
            return render(request,'admin_view.html',context)
        context = {'users':user}
        return render(request,'admin_view.html',context)
    else:
        return HttpResponse('not accessible')

@login_required(login_url='login')
def task(request):
    customer = request.user.customer
    form = TaskForm(user=customer)
    
    if request.method == 'POST':
        form = TaskForm(request.POST,user=customer)
        # form.fields['sent_by']=request.user
        if form.is_valid():
            formob=form.save(commit=False)
            formob.published_at=datetime.datetime.now()
            p=Task.objects.filter(person=customer)
            try:
                formob.process=p.process
                print(p)
                formob.save()
                messages.success(request, 'Task Submitted')
                return redirect('task')
            except:
                messages.error(request, 'No Process Found, Contact Admin')                   
    context = {'form':form}
    return render(request,'task.html',context)

@login_required(login_url='login')
def tasks_display(request): 
    # try:
        
        task=Task.objects.filter(person=request.user.customer,completed=False)
        print(task)
        completed_task=Task.objects.filter(person=request.user.customer,completed=True)
        l=[]
        date=str(datetime.datetime.now())
        for i in completed_task:
            k=date_time_diff(str(i.end_time)[:10],date[:10]).days
            if k<=15:
                l.append(i)
        print(l)


        return render(request,"task_display.html",{'task':task,'completed_task':l})
    # except:
    #     print("NOOOOO TAKSSSSSSSSSSSSSS")
    #     return render(request,"task_display.html")

@login_required(login_url='login')    
def end_process(request,pid):
    t = Task.objects.get(id=pid)
    ob= Process.objects.get(process_title=t.process)
    ob.end_time=datetime.datetime.now()
    ob.save()
    return redirect('/')

@login_required(login_url='login')
def task_view(request,pid):
    task=Task.objects.get(id=pid)
    process= Process.objects.get(process_title=task.process)
    if len(str(process.end_time))>3:
        completed=True
    else:
        completed=False

    try:
        flag=None
        rec=ReceiverTask.objects.get(task=task)
    except:
        flag=1
    print("$$$$$$$$$$$$$$$$4444444",flag)
    return render(request,"task_view.html",{'task':task,'flag':flag,'process':process,'comp':completed})

@login_required(login_url='login')
def task_agree(request,pid):
    task=Task.objects.get(id=pid)
    rec=ReceiverTask(task=task,start_time=datetime.datetime.now())
    rec.save()
    return redirect('tasks_display')
    
@login_required(login_url='login') 
def task_finish(request,pid):
    task=Task.objects.get(id=pid)
    task.completed=True
    task.end_time=datetime.datetime.now()
    task.save()
    rec=ReceiverTask.objects.get(task=task)
    rec.end_time=datetime.datetime.now()
    rec.save()
    return redirect('task')


@login_required(login_url='login')
def ticket(request):
    customer = request.user.customer
    form = TicketForm(user=customer,request=request)
    
    if request.method == 'POST':
        form = TicketForm(request.POST,user=customer,request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket Submitted')
            return redirect('ticket')
    context = {'form':form}
    return render(request,'ticket.html',context)

@login_required(login_url='login')
def ticket_display(request):
    try:
        task=Ticket.objects.filter(send_to=request.user.customer,completed=False)
        print(task)
        return render(request,"ticket_display.html",{'task':task})
    except:
        print("NOOOOO TAKSSSSSSSSSSSSSS")
        return render(request,"ticket_display.html")
    
@login_required(login_url='login')
def ticket_view(request,pid):
        ticket=Ticket.objects.get(id=pid)
        chats=TicketResponse.objects.filter(ticket=ticket)
        context={'ticket':ticket,'chats':chats}
        print(chats)
        if request.method=='POST':
            res=request.POST.get('response')
            print(res)
            obj=TicketResponse(ticket=ticket,message=res,send_to=ticket.sent_by,sent_by=request.user.customer)
            obj.save()
            return redirect('/')
        return render(request,"ticket_view.html",context)

@login_required(login_url='login')
def mytickets(request):
    cust=request.user.customer
    ticket=Ticket.objects.filter(sent_by=cust,completed=False)
    return render(request,'mytickets.html',{'task':ticket})

@login_required(login_url='login')
def end_ticket(reqest,pid):
    ticket=Ticket.objects.get(id=pid)
    ticket.completed=True
    ticket.completed_at=datetime.datetime.now()
    ticket.save()
    return redirect('ticket')

@login_required(login_url='login')
def pro_analysis(request,pid):
    pro=Process.objects.get(id=pid)
    print(pro)
    f=str(pro.start_time)
    e=str(pro.end_time)
    print(f[11:19])
    print(f,e)
    time=time_diff(f[11:19],e[11:19])
    time=sec_to_day(time)
    print('{{{{{{{{{{{{{{{{{{{{{{{{{')
    print(time)
    total_timetaken=str(date_time_diff(str(pro.start_time)[0:10],str(pro.end_time)[0:10]).days)+'days'+str(time)+'sec'
    t=Task.objects.filter(process=pro).order_by('published_at')
    # tr=ReceiverTask.objects.filter(task=pro)
    trlist=[]
        

    l=list()
    for i in range(len(t)):
        tr=ReceiverTask.objects.get(task=t[i])
        d=dict()
        d['task']=t[i].task_title
        time=time_diff(str(t[i].published_at)[11:19],str(t[i].end_time)[11:19])
        d['time']=str(date_time_diff(str(t[i].published_at)[0:10],str(t[i].end_time)[0:10]).days)+'days'+str(time)+'sec'
        d['person']=t[i].person.name
        time=time_diff(str(t[i].published_at)[11:19],str(tr.start_time)[11:19])
        d['timetostart']=str(date_time_diff(str(t[i].published_at)[0:10],str(tr.start_time)[0:10]).days)+'days'+str(time)+'sec'
        l.append(d)
    print(l)


    return render(request,'pro_analysis.html',{'total_timetaken':total_timetaken,'tasks':l,'process':pro})

@login_required(login_url='login')
def ajax_load_persons(request):
    team_id = request.GET.get('team')
    print(team_id)
    persons = Customer.objects.filter(team__id=team_id)
    return render(request, 'ajax_load_persons.html', {'persons': persons})

@login_required(login_url='login')
def create_org(request,pid=None):
    if(pid==None):
        pid = request.user.customer.company.ceo_id
    print(pid)
    lead = Customer.objects.get(id=pid)
    ob = Customer.objects.filter(works_under=lead)
    print(ob)
    context={'ob':ob,'lead':lead}
    return render(request,"trial.html",context)

@login_required(login_url='login')
def orgchart(request):
    pid=request.GET.get('pid')
    lead = Customer.objects.get(id=pid)
    ob = Customer.objects.filter(works_under=lead)
    co =request.GET.get('count')

    print("::::::::::::::::::::::::")    

    context={'o':ob,'lead':lead,'co':co}
    return render(request,"orgchart.html",context)

@login_required(login_url='login')
def user_info(request,id):
    customer=Customer.objects.get(id=id)
    return render(request,'user_info.html',{'customer':customer})
            
#for leaves approval and rejection
@login_required(login_url='login')
def leaveslist(request):
    cust=request.user.customer
    lobj=Leave.objects.filter(seen=False)
    context={'leaves':lobj}
    return render(request,'leavelist.html',context)

@login_required(login_url='login')
def approve_leave(request,id):
    k=Leave.objects.get(id=id)
    cust=Customer.objects.get(id=k.user.id)
    # print(c)
    if k.leave_type=="Casual":
        cust.casual_leaves-=1
        cust.total_leaves-=1
    elif k.leave_type=="Sick":  
        cust.sick_leaves-=1
        cust.total_leaves-=1
    elif k.leave_type=="Optional":
        cust.optional_leaves-=1
        cust.total_leaves-=1
    cust.save()
    k.accepted=True
    k.seen=True
    k.save()
    return redirect('leaveslist')

@login_required(login_url='login')
def disapprove_leave(request,id):
    leave=Leave.objects.get(id=id)
    leave.seen=True
    leave.save()
    return redirect('leaveslist')

@login_required(login_url='login')
def myleaves(request):
    obj=Leave.objects.filter(user=request.user.customer)[::-1]
    print(obj)
    if len(obj)>5:
        obj=obj[:5]
    print(obj)

    return render(request,'myleaves.html',{'leaves':obj})

@login_required(login_url='login')
def salary(request):
    userall = Customer.objects.filter(company=request.user.customer.company)
    if request.method == 'POST':
            user1 = int(request.POST.get('user'))
            user1=User.objects.get(id=user1)
            try:
                working_days=int(request.POST.get('working_days'))
            except:
                working_days=user1.customer.company.total_working_days
            print(working_days)

            obj = Timesheet.objects.filter(user=user1.customer)
            today = str(user1.customer.company.payroll_date)
            print(today)
            year =int(today[:4])
            day = int(today[8:])
            # print(day)
            count = 0
            month=int(str(datetime.datetime.now().date())[5:7])
            print(month)
            for i in obj:
                date = str(i.date)
                yr = int(date[:4])
                # print(yr)
                mo = int(date[5:7])
                # print(mo)
                # d = date[8:]
                if mo == month-1 and yr >= year:
                        count+=1
                elif month==1 and mo==12:
                        count+=1
            lobj=Leave.objects.filter(user=user1)
            for i in range(0,len(lobj)):
                date = str(lobj[i].date)
                mo = int(date[5:7])
                if mo == int(month)-1 and yr >= year:
                        count+=1
                elif month==1 and mo==12:
                        count+=1

            sal=Customer.objects.get(user=user1)
            sal=sal.salary
            print(sal)
            print(count)
            print(count/working_days)
            sal_to_paid=sal*(count/working_days)
            return HttpResponse(sal_to_paid)

    return render(request,"salary.html",{'user':userall})

@login_required(login_url='login')
def overtimelist(request):
    cust=request.user.customer
    lobj=SelectOvertime.objects.filter(seen=False,accepted=False)
    context={'overtime':lobj}
    return render(request,'overtimelist.html',context)

@login_required(login_url='login')
def approve_overtime(request,id):
    k=SelectOvertime.objects.get(id=id)
    k.accepted=True
    k.seen=True
    k.save()
    return redirect('overtimelist')

@login_required(login_url='login')
def disapprove_overtime(request,id):
    overtime=SelectOvertime.objects.get(id=id)
    overtime.seen=True
    overtime.save()
    return redirect('overtimelist')

@login_required(login_url='login')
def myovertimes(request):
    try:
        obj=SelectOvertime.objects.filter(person=request.user.customer)[::-1]
        print(obj)
        if len(obj)>5:
            obj=obj[:5]
        print(obj)
        return render(request,'myovertime.html',{'overtime':obj})
    except:
        return HttpResponse("No overtimes")

@login_required(login_url='login')
def abc(request):
    idlist=Customer.objects.filter(company=request.user.customer.company)
    ids=dict()
    print(idlist)
    for i in idlist:
        print(i.works_under)
        if i.works_under==None:
            continue
        elif i.works_under.id in ids:
            ids[i.works_under.id]+=[i.id]
        else:
            print("KKKKKKK")
            ids[i.works_under.id]=[i.id]

    dictid=[]
    for i in idlist:
        d=dict()
        d['head']=i.name
        d['id']=i.id
        d['contents']=i.designation

        # d['children']=[]
        dictid.append(d)
    print('dictidd=',dictid)
    child={}
    for k,v in ids.items():
        for j in v:
            for a in dictid:
                if a['id']==j:
                    if k in child:
                        child[k]+=[a]
                    else:
                        child[k]=[a]
    print('child=',child)
    newchild={}
    for k in child:
        for j in dictid:
            if k==j['id']:
                if 'children' in j:
                    j['children']+=child[k]
                else:
                    j['children']=child[k]
    print('dictid=',dictid)
        
    







        

    # org=[]
    # for i in idlist:
    #     if not i.works_under is None:
    #         d=dict()
    #         d['id']=i.id
    #         d['pid']=i.works_under.id
    #         d['name']=i.name
    #         org.append(d)
    # print(org)
    # neworg=[]
    # for i in org:
    #     json_object =dumps(i) 
    #     neworg.append(json_object)
    # context={"info":neworg}




    # for i in ids:



    json_object =dumps(dictid[0]) 
    context={"info":json_object}


    
    print(json_object)
    # return HttpResponse(json_object)
    return render(request,'jHTree.html',context)