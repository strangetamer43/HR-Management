# Generated by Django 4.1.1 on 2022-12-04 15:19

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True, unique=True)),
                ('payroll_date', models.DateField(blank=True, null=True)),
                ('total_working_days', models.IntegerField(blank=True, null=True)),
                ('ceo_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='userprofile.png', null=True, upload_to='images')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('total_leaves', models.IntegerField(blank=True, default=20, null=True)),
                ('casual_leaves', models.IntegerField(blank=True, default=10, null=True)),
                ('sick_leaves', models.IntegerField(blank=True, default=5, null=True)),
                ('optional_leaves', models.IntegerField(blank=True, default=5, null=True)),
                ('status', models.CharField(default='Not Available', max_length=200, null=True)),
                ('level', models.IntegerField(blank=True, default=1, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('salary_to_be_paid', models.IntegerField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='OverTimeSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('no_of_slots', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('google_link', models.CharField(blank=True, max_length=150, null=True)),
                ('fcfs', models.BooleanField(blank=True, default=False, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_title', models.CharField(blank=True, max_length=200, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_type', models.CharField(max_length=50, null=True)),
                ('target', models.CharField(blank=True, max_length=100, null=True)),
                ('work_per_day', models.IntegerField(blank=True, null=True)),
                ('work_per_hour', models.IntegerField(blank=True, null=True)),
                ('cal_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('cal_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('send_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
                ('sent_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_by', to='webapp.customer')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
        ),
        migrations.CreateModel(
            name='Workitems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='UserCalender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cal_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('cal_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='User_Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('count', models.IntegerField(null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('google_link', models.CharField(blank=True, max_length=150, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('entry', models.TimeField(blank=True, null=True)),
                ('break1', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('break1_end', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('meet', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('endmeet', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('systemissue', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('endsystemissue', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('lunch', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('lunch_end', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), blank=True, default=list, null=True, size=None)),
                ('out', models.TimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='TicketResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('send_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
                ('sent_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_by1', to='webapp.customer')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Template_cal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(blank=True, max_length=50, null=True)),
                ('summary', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('count', models.IntegerField(null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('google_link', models.CharField(blank=True, max_length=150, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('team_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to='webapp.customer')),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.process')),
                ('sent_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
            options={
                'ordering': ('-published_at',),
            },
        ),
        migrations.CreateModel(
            name='SelectOvertime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overtimedate', models.DateField()),
                ('accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('seen', models.BooleanField(blank=True, default=False, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('overtime', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.overtimeschedule')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiverTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.task')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
        ),
        migrations.AddField(
            model_name='overtimeschedule',
            name='team_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams'),
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('leave_type', models.CharField(choices=[('Casual', 'Casual'), ('Sick', 'Sick'), ('Optional', 'Optional')], max_length=200, null=True)),
                ('accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('seen', models.BooleanField(blank=True, default=False, null=True)),
                ('applied_at', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer')),
                ('team_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('count', models.IntegerField(null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('google_link', models.CharField(blank=True, max_length=150, null=True)),
                ('weekoff', multiselectfield.db.fields.MultiSelectField(choices=[('MO', 'Monday'), ('TU', 'Tuesday'), ('WE', 'Wednesday'), ('TH', 'Thursday'), ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')], default='TU', max_length=20)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.company')),
                ('team_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.teams'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='works_under',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.customer'),
        ),
    ]
