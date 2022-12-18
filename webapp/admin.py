from django.contrib import admin

from .models import *

# # Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(CompanyAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
         
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
     readonly_fields = [
        'user'
    ]
     def get_queryset(self, request):
          queryset = super(CustomerAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               print(customer.company)
               return queryset.filter(company=customer.company)
     
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "works_under":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "team":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)
            

     def get_form(self, request, obj=None, **kwargs):
          form = super().get_form(request, obj, **kwargs)   
          try:
               form.base_fields['company'].initial = request.user.customer.company
               form.base_fields['company'].disabled = True
          except:
               pass
          return form
            
     
# admin.site.register(Timesheet) 

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
     readonly_fields = [
        'company'
    ]
     def get_queryset(self, request):
          queryset = super(TimesheetAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
     
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "user":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     # def get_form(self, request, obj=None, **kwargs):
     #    form = super().get_form(request, obj, **kwargs)
     #    form.base_fields['company'].initial = request.user.customer.company
     #    form.base_fields['company'].disabled = True
     #    return form
     def save_model(self, request, obj, form, change):
          obj.company = request.user.customer.company
          super().save_model(request, obj, form, change)

     
          
# admin.site.register(Leave)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
     readonly_fields = [
        'company'
    ]
     def get_queryset(self, request):
          queryset = super(LeaveAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
     
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "user":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
     def save_model(self, request, obj, form, change):
          obj.company = request.user.customer.company
          super().save_model(request, obj, form, change)

# admin.site.register(Workitem)

@admin.register(Workitems)
class WorkitemsAdmin(admin.ModelAdmin):
     readonly_fields = [
        'company'
    ]
     def get_queryset(self, request):
          queryset = super(WorkitemsAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
          
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "user":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def save_model(self, request, obj, form, change):
          obj.company = request.user.customer.company
          super().save_model(request, obj, form, change)

# admin.site.register(PolicyUpdate)

@admin.register(PolicyUpdate)
class PolicyUpdateAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(PolicyUpdateAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "customer":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    # return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "team":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          
          return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form

# admin.site.register(Event)
# admin.site.register(Teams)


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
#      readonly_fields = [
#         'company'
#     ]
     def get_queryset(self, request):
          queryset = super().get_queryset(request)
          # print(queryset)
          # queryset = super(self).all()
          print(queryset)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:

          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form

# admin.site.register(Hierarchy)

@admin.register(Hierarchy)
class HierarchyAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(HierarchyAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "manager":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    # return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "team_type":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form

# admin.site.register(UserCalender)

@admin.register(UserCalender)
class UserCalenderAdmin(admin.ModelAdmin):
     exclude = ('google_link','location')

     def get_queryset(self, request):
          queryset = super(UserCalenderAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "customer":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form
          
# admin.site.register(User_Event)

@admin.register(User_Event)
class User_EventAdmin(admin.ModelAdmin):
     exclude = ('google_link','location')
     def get_queryset(self, request):
          queryset = super(User_EventAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "customer":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form
          
# admin.site.register(Task)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  
     readonly_fields = [
            'company'
          ]
     def get_queryset(self, request):
          queryset = super(TaskAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
          
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "sent_by":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "team":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)

               if db_field.name == "process":
                    kwargs["queryset"] = Process.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "person":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def save_model(self, request, obj, form, change):
          try:
               obj.company = request.user.customer.company
          except:
               pass
          super().save_model(request, obj, form, change)
# admin.site.register(ReceiverTask)

@admin.register(ReceiverTask)
class ReceiverTaskAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(ReceiverTaskAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:

               if db_field.name == "task":
                    kwargs["queryset"] = Task.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form
          
# admin.site.register(Ticket)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(TicketAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "sent_by":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "team":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)

               if db_field.name == "send_to":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form
          

# admin.site.register(TicketResponse)

@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(TicketResponseAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)


     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "ticket":
                    kwargs["queryset"] = Ticket.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "sent_by":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "send_to":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form

# admin.site.register(Process)

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
          queryset = super(ProcessAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
     
     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form

# admin.site.register(OverTimeSchedule)

@admin.register(OverTimeSchedule)
class OverTimeScheduleAdmin(admin.ModelAdmin):
     exclude = ('google_link','location')
     def get_queryset(self, request):
          queryset = super(OverTimeScheduleAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "team_type":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form


# admin.site.register(SelectOvertime)
@admin.register(SelectOvertime)
class SelectOvertimeAdmin(admin.ModelAdmin):
     exclude = ('google_link','location')
     def get_queryset(self, request):
          queryset = super(SelectOvertimeAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "person":
                    kwargs["queryset"] = Customer.objects.filter(company=request.user.customer.company)
                    return super().formfield_for_foreignkey(db_field, request, **kwargs)
               if db_field.name == "overtime":
                    kwargs["queryset"] = OverTimeSchedule.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form
     

@admin.register(Template_cal)
class TemplateAdmin(admin.ModelAdmin):
     readonly_fields = [
          'company'
     ]
     exclude = ('google_link','location')
     def get_queryset(self, request):
          queryset = super(TemplateAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)

     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "team_type":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def save_model(self, request, obj, form, change):
          try:
               obj.company = request.user.customer.company
          except:
               pass
          super().save_model(request, obj, form, change)

     
@admin.register(Event)
class TeamsAdmin(admin.ModelAdmin):
     exclude = ('google_link',)
     def get_queryset(self, request):
          queryset = super(TeamsAdmin, self).get_queryset(request)
          if request.user.is_superuser:
               return queryset
          else:
               customer = request.user.customer
               return queryset.filter(company=customer.company)
     def formfield_for_foreignkey(self, db_field, request, **kwargs):
          try:
               if db_field.name == "team_type":
                    kwargs["queryset"] = Teams.objects.filter(company=request.user.customer.company)
          except:
               pass
          return super().formfield_for_foreignkey(db_field, request, **kwargs)

     def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
          form.base_fields['company'].initial = request.user.customer.company
          form.base_fields['company'].disabled = True
        except:
          pass
        return form