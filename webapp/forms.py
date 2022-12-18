from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


from .models import *

class CustomerForm(ModelForm):          
	class Meta:
		model = Customer                 
		fields = '__all__'
		exclude = ['user','leave_type','total_leaves','casual_leaves',
		'sick_leaves','optional_leaves','leave_type','status','team',
		'designation','level','works_under','company','salary','salary_to_be_paid']
		widgets ={'name': forms.TextInput(attrs={'class': "form-control"}),
		'phone': forms.TextInput(attrs={'class': "form-control"}),
		'email': forms.EmailInput(attrs={'class': "form-control"}),
		'profile_pic': forms.FileInput(attrs={'class': "form-control"}),
		}

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','password1', 'password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class CompanyForm(ModelForm):
	class Meta:
		model=Company
		fields='__all__' 
		widgets = {'payroll_date':DateInput()} 

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['date','leave_type']
        widgets = {'date':DateInput()} 

class WorkItemForm(ModelForm):
	class Meta:
		model = Workitems
		fields = '__all__'
		exclude = ['user','date','company']
		widgets ={'work_title': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter workitem title'}),
		'description': forms.Textarea(attrs={'class': "form-control",'placeholder': 'Enter workitem description'}),
		}

class TeamsForm(ModelForm):
	class Meta:
		model = Teams
		fields = '__all__'
		exclude = ['company']
		widgets ={'team_type': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter team name'}),
		'target': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter target for the team'}),
		'work_per_day': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Work Items per day'}),
		'work_per_hour': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Work Items per hour'}),
		'cal_id': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter Calendar ID'}),
		'cal_link': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter Calendar link'})}

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = '__all__'
		exclude = ['location','google_link','company']
		widgets = {
		'summary': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter team name'}),
		'description': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter team name'}),
		'start_date':DateInput(),'end_date':DateInput(),'start_time': forms.TimeInput(attrs={'type': 'time'}),
		'end_time': forms.TimeInput(attrs={'type': 'time'})}

	def __init__(self, *args, **kwargs):
		request=kwargs.pop('request')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.company=request.user.customer.company
		
		self.fields['team_type'].queryset = Teams.objects.filter(company=request.user.customer.company)


class PolicyForm(ModelForm):
	class Meta:
		model = PolicyUpdate
		fields = '__all__'
		exclude = ['company','customer','slug','time']
		widgets ={'policy_title': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter policy name'}),
		'description': forms.Textarea(attrs={'class': "form-control",'placeholder': 'Enter policy description'}),
		}

	def __init__(self, *args, **kwargs):
		request=kwargs.pop('request')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.company=request.user.customer.company
		
		self.fields['team'].queryset = Teams.objects.filter(company=request.user.customer.company)



class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = '__all__'
		exclude=['sent_by','completed','end_time','process','published_at','company']
		widgets ={'team': forms.Select(attrs={'class': "form-control", 
                }),
				'person': forms.Select(attrs={'class': "form-control", 
                }),
				'task_title': forms.TextInput(attrs={'placeholder': 'Enter task title','class': "form-control", 
                }),
				'description': forms.Textarea(attrs={'placeholder': 'Enter task description','class': "form-control", 
                }),
				}
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.sent_by = user
		self.fields['person'].queryset = Customer.objects.none()
		self.fields['team'].queryset = Teams.objects.filter(company=user.company)
		
		if 'team' in self.data:
			try:
				team_id=int(self.data.get('team'))
				self.fields['person'].queryset=Customer.objects.filter(team_id=team_id)
			except:
				pass
		elif self.instance.pk:
			self.fields['person'].queryset=self.instance.team.person_set

class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = '__all__'
		exclude=['sent_by','completed','completed_at','company']
		widgets ={'team': forms.Select(attrs={'class': "form-control", 
                }),
				'send_to': forms.Select(attrs={'class': "form-control", 
                }),
				'task_title': forms.TextInput(attrs={'placeholder': 'Enter task title','class': "form-control", 
                }),
				'description': forms.Textarea(attrs={'placeholder': 'Enter task description','class': "form-control", 
                }),
				}
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		request=kwargs.pop('request')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.sent_by = user
		self.instance.company=request.user.customer.company
		self.fields['team'].queryset = Teams.objects.filter(company=self.instance.company)
		self.fields['send_to'].queryset = Customer.objects.none()
		
		if 'team' in self.data:
			try:
				team_id=int(self.data.get('team'))
				self.fields['send_to'].queryset=Customer.objects.filter(team_id=team_id)
			except:
				pass
		elif self.instance.pk:
			self.fields['send_to'].queryset=self.instance.team.person_set 	

class OverTimeForm(ModelForm):
	class Meta:
		model = OverTimeSchedule
		fields = '__all__'
		exclude=['google_link','location','company']
		widgets = {'team_type': forms.Select(attrs={'class': "form-control", }),
		'start_date':DateInput(),'start_time': forms.TimeInput(attrs={'class': "form-control",'type': 'time'}),
		'end_time': forms.TimeInput(attrs={'class': "form-control",'type': 'time'}),
		'summary': forms.TextInput(attrs={'class': "form-control",'placeholder': 'Enter summary/description'}),
		'no_of_slots': forms.TextInput(attrs={'class': "form-control",'placeholder': 'number of slots available'})}

	def __init__(self, *args, **kwargs):
		request=kwargs.pop('request')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.company=request.user.customer.company
		
		self.fields['team_type'].queryset = Teams.objects.filter(company=request.user.customer.company)

class SelectOvertimeForm(ModelForm):
	class Meta:
		model = SelectOvertime
		fields = '__all__'
		exclude=['person','company','seen','accepted']
		widgets = {'overtimedate':DateInput(),'overtime': forms.Select(attrs={'placeholder': 'Enter task title','class': "form-control", 
                }),}

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.instance.person = user
		self.fields['overtime'].queryset = Customer.objects.none()
		
		if 'overtimedate' in self.data:
			# try:
				team_id=self.data.get('overtimedate')
				print(team_id)
				k=OverTimeSchedule.objects.filter(start_date=team_id,no_of_slots__gt=0,company=user.company)
				print("?????????????????????????????????????")
				print(user.company)
				# if k.no_of_slots>0:
				self.fields['overtime'].queryset=k
			# except:
				# print("?????????????????????????????????????")
				# pass
		# elif self.instance.pk:
		# 	self.fields['send_to'].queryset=self.instance.team.person_set 