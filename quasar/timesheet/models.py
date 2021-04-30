
#from datetime import datetime
from django.contrib.admin import filters
from django.contrib.admin.sites import AdminSite, DefaultAdminSite
from django.db import models
from django.contrib import admin
from django.http.response import HttpResponse

from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Min, Max, constraints
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from nested_admin import NestedModelAdmin, NestedTabularInline
from django.forms import TextInput, Textarea

'''
from django.db.models import Deferrable, UniqueConstraint
from django import db
from django.db import transaction, IntegrityError
from django.template.response import TemplateResponse
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponseNotAllowed, HttpResponse
'''
import django





class Tag(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self):
        return self.name

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = (['name'])
    list_filter = (['name'])
    
class Timesheet(models.Model):
    date = models.DateTimeField('Timesheet Date', default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique_for_date=date)
    approved = models.BooleanField(default=False)
    note = models.TextField(blank=True) 


    def __str__(self):
        return str(self.date.strftime("%d %B, %Y"))
    
    def tasks(self):  
        return Timesheet.objects.filter(task__timesheet__exact = self.id).aggregate(Count('task'))['task__count'] 
    
    def duration(self):
        seconds = type(self).objects.filter(task__timesheet__exact = self.id).aggregate(Sum('task__seconds'))['task__seconds__sum']
        if seconds:
            return timedelta(seconds=seconds)
        return timedelta(seconds=0)
    
    def timesheet_date(self):
        return self.date 
    
    
    
    '''
    class Meta:
        unique_together = ['user','date']
    
    def clean(self) -> None:
        ts_exist = Timesheet.objects.filter(user_id = self.user_id, date = self.date).first()
        if ts_exist:
            
            print('TS exist **********************************', ts_exist)
            raise ValidationError('This Timesheet already exist!')    
        return super().clean(self)
    '''

  
class Project(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=70, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    user = models.ManyToManyField(User, related_name='user_activity')

    def __str__(self):
        return self.name + ' for ' + str(self.project)
    
    def get_queryset(self, request):
        print('queryset--------------------------Activity')
        qs = super(Activity, self).get_queryset(request) 
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def last_activity(self, request):
        user=request.user
        activity = type(self).objects.filter(user = user).order_by(self.from_time, 'asc').first()

        return activity


from datetime import timedelta, datetime

class Task(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True) 

    activity = models.ForeignKey(Activity, null=False, on_delete=models.CASCADE)

    item = models.CharField(max_length=70, help_text='Document code or any other Item ID.', default='')
    reference = models.CharField(max_length=70, help_text='Transmitall number or any other project reference.')

    #from_time = models.TimeField(default=now().strftime("%H:%M:%S"))
    #to_time = models.TimeField(default=now().strftime("%H:%M:%S"))
    #from_time = models.TimeField(auto_now_add=True, editable=True)
    from_time = models.TimeField('from',default=django.utils.timezone.now)
    to_time = models.TimeField('to',default=django.utils.timezone.now)
    
    seconds = models.IntegerField()

    approved = models.BooleanField(default=False)
    attachments = models.FileField(blank=True) 
    
    
    note = models.TextField(blank=True) 
    

    class Meta:
        ordering = ['from_time']

    '''
    def save_model(self, request, obj, form, change):
        pass
        
        obj.user = request.user
        super(Task, self).save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        formset.save() # this will save the children
        form.instance.save() # form.instance is the parent
    
    def get_queryset(self, request):
        qs = super(Task, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    '''
    

    def __str__(self):
        
        return str(self.from_time) + ' - ' + str(self.to_time) + ' | ' + str(self.activity)

    def search_task(self):
        return str(self.project) 
    

    
    def duration(self):
        
        # Create datetime objects for each time (a and b)
        dateTimeA = datetime.combine(datetime.today(), self.from_time)
        dateTimeB = datetime.combine(datetime.today(), self.to_time)
        # Get the difference between datetimes (as timedelta)
        dateTimeDifference = dateTimeB - dateTimeA
        # Divide difference in seconds by number of seconds in hour (3600)  
        #dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
        return dateTimeDifference 
    
    def duration_seconds(self):
        # Create datetime objects for each time (a and b)
        dateTimeA = datetime.combine(datetime.today(), self.from_time)
        dateTimeB = datetime.combine(datetime.today(), self.to_time)
        # Get the difference between datetimes (as timedelta)
        dateTimeDifference = dateTimeB - dateTimeA
        # Divide difference in seconds by number of seconds in hour (3600)  
        #dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
        #return (dateTimeDifference.total_seconds()/3600) 
        return dateTimeDifference.total_seconds()

    
    '''
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(user=request.user)
    '''


class Comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    text = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    level = models.CharField(choices=[('I','info'),('A','action'),('!','warning')], default='I', max_length=3)

    def __str__(self):
        return self.text


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = (['activity__name','activity__project__name'])
    list_filter = (['timesheet__date','tags','activity__project__name','activity'])
    exclude = ['user']
    list_display = ['timesheet', 'from_time','activity', 'duration', 'attachments','approved']
    #raw_id_fields = ('user', 'task')
    def save_model(self, request, obj, form, change):
        print('model--------------------------TaskAdmin')
        obj.user = request.user
        obj.seconds = 1
        super(TaskAdmin, self).save_model(request, obj, form, change)
        
    def get_queryset(self, request):
        print('queryset--------------------------TaskAdmin')
        qs = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True 
        return obj.user == request.user or request.user.is_superuser
    

class CommentsInline(NestedTabularInline):
    model = Comments
    extra = 0
    fields = ['text','level']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':50})},
    }

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass

class TaskInline(NestedTabularInline):
    model = Task
    extra = 0
    inlines = [CommentsInline]
    #list_filter = ([UserFilter])
    #readonly_fields = ('from_time',)
    fields = ['from_time','to_time','activity', 'item','reference']
    #exclude = ['note','tags']
    sortable_by = ['activity' ,'to_time']
    date_hierarchy = 'from_time'
    search_fields = (['note'])
    
    
    def get_queryset(self, request):
        print('queryset--------------------------TaskInline')
        qs = super(TaskInline, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print('formfield--------------------------TaskInline')
        if db_field.name == "activity":
            kwargs["queryset"] = Activity.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


from django.db import connection
from django.shortcuts import redirect, render



@admin.register(Timesheet)
class TimesheetView(NestedModelAdmin):
    search_fields = (['date'])
    fields= ['date']
    list_display = ['date','user','tasks','duration']
    #fk_name='user'
    list_filter = (['date'])
    #list_filter = ([UserFilter])
    change_form_template = 'timesheet_form.html'
    inlines = [
        TaskInline
    ]
    
    #@transaction.atomic
    def save_model(self, request, obj, form, change):
        #sid = transaction.savepoint()
        print('form-save_model--------------------------TimesheetView 1')
        obj.user = request.user
    
        return super().save_model(request, obj, form, change)
        
          
    #@transaction.atomic
    def save_formset(self, request, form, formset, change):
        print('formset--------------------------TimesheetView')
        if form.is_valid():
            
            form_obj = form.save(commit=False)
            print(form_obj, form_obj.date)
            
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for task in instances:
                task.user = request.user
                task.seconds = task.duration_seconds()
                task.save()
            
            formset.save_m2m()
        
    
    def get_queryset(self, request):
        print('queryset--------------------------TimesheetView')
        qs = super(TimesheetView, self).get_queryset(request) 
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_fields(self, request, obj):
        
        return super().get_fields(request, obj=obj)
    
    
     
    
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    
    #raw_id_fields = ('user', 'task')
    '''
    def save_model(self, request, obj, form, change):
        print('model--------------------------ActivityAdmin')
        obj.user.set(request.user) 
        super(ActivityAdmin, self).save_model(request, obj, form, change)
    '''   
    def get_queryset(self, request):
        print('queryset--------------------------ActivityAdmin')
        qs = super(ActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser: 
            return qs
        return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True 
        return obj.user == request.user or request.user.is_superuser






#
# Employee User detail
#


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    day_hours = models.IntegerField(default=8,help_text='Expected working hours per day.')


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


