# from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import datetime
import random

from .models import Event,Teams,User,Customer,UserCalender,User_Event,OverTimeSchedule
from django.db.models.signals import post_delete, post_save


SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'


def test_calendar():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    return service

def handle_event(sender, created, instance, **kwargs):
        """this function creates the events in the google agenda and updates them if changed in the website"""
        service = test_calendar()
        event = instance
        # if not event.end_date:
        #     event.end_date = event.start_date
        if not event.end_time and event.start_time:
            event.end_time = event.start_time
        elif not event.end_time:
            event.end_time = datetime.datetime.min.time()
        if not event.start_time:
            event.start_time = datetime.datetime.min.time()
        # if event.end_date < event.start_date:
        #     event.end_date, event.start_date = event.start_date, event.end_date
        queryset = Event.objects.filter(
            id=event.id
        ) 
        team=Teams.objects.get(team_type=event.team_type,company=event.company)
        CAL_ID=team.cal_id
        color=random.randint(1, 11)
        days=['MO','TU','WE','TH','FR','SA','SU']
        for i in event.weekoff:
            days.remove(i)   
        k=','.join(days)    
        rec='RRULE:FREQ=DAILY;COUNT='
        rec+=str(instance.count)+';BYDAY='+k
        print(rec)
        event = {
            "summary": event.summary,
            "location": event.location or "",
            "description": (event.description),
            "start": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.start_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.end_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "recurrence": [rec],
            "reminders": {},
            'colorId':color,
        }
        # customer=Customer.objects.get(user=request.user)

        if created or not instance.google_link:
            try:
                event = (
                    service.events()
                    .insert(
                        calendarId=CAL_ID,
                        body=event,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("An error occurred: %s" % error)
                pass
        else:
            try:
                event = (
                    service.events()
                    .update(
                        calendarId=CAL_ID,
                        body=event,
                        eventId=instance.google_link,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                # print("An error occurred: %s" % error)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                pass
        return event    

def delete_event(sender, instance, **kwargs):
    """this function deletes an event from google agenda when deleted in the website"""
    team=Teams.objects.get(team_type=instance.team_type)
    CAL_ID=team.cal_id
    try:
        service = test_calendar()
        service.events().delete(
            calendarId=CAL_ID,
            eventId=instance.google_link,
        ).execute()
    except:
        pass


post_save.connect(handle_event, sender=Event)
post_delete.connect(delete_event, sender=Event)


#user calendar functions
def user_handle_event(sender, created, instance, **kwargs):
        """this function creates the events in the google agenda and updates them if changed in the website"""
        service = test_calendar()
        event = instance
        # if not event.end_date:
        #     event.end_date = event.start_date
        if not event.end_time and event.start_time:
            event.end_time = event.start_time
        elif not event.end_time:
            event.end_time = datetime.datetime.min.time()
        if not event.start_time:
            event.start_time = datetime.datetime.min.time()
        # if event.end_date < event.start_date:
        #     event.end_date, event.start_date = event.start_date, event.end_date
        queryset = User_Event.objects.filter(
            id=event.id
        )
        try:
            customer=UserCalender.objects.get(customer=event.customer)
        except:
            pass
        CAL_ID=customer.cal_id
        rec='RRULE:FREQ=DAILY;COUNT='
        rec+=str(instance.count)
        color=random.randint(1, 11)


        event = {
            "summary": event.summary,
            "location": event.location or "",
            "description": (event.description),
            "start": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.start_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.end_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            'recurrence': [rec],
            "reminders": {},
            'colorId':color,

        }
        # customer=Customer.objects.get(user=request.user)

        if created or not instance.google_link:
            try:
                event = (
                    service.events()
                    .insert(
                        calendarId=CAL_ID,
                        body=event,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                # print("An error occurred: %s" % error)
                pass
        else:
            try:
                event = (
                    service.events()
                    .update(
                        calendarId=CAL_ID,
                        body=event,
                        eventId=instance.google_link,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                # print("An error occurred: %s" % error)
                pass
        return event    

def user_delete_event(sender, instance, **kwargs):
    """this function deletes an event from google agenda when deleted in the website"""
    try:
        customer=UserCalender.objects.get(customer=instance.customer)
    except:
        pass
    CAL_ID=customer.cal_id
    try:
        service = test_calendar()
        service.events().delete(
            calendarId=CAL_ID,
            eventId=instance.google_link,
        ).execute()
    except:
        pass


post_save.connect(user_handle_event, sender=User_Event)
post_delete.connect(user_delete_event, sender=User_Event)


#overtime functions
def overtime_calendar():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    return service

def overtime_handle_event(sender, created, instance, **kwargs):
        """this function creates the events in the google agenda and updates them if changed in the website"""
        service = overtime_calendar()
        event = instance
         # if not event.end_date:
         #     event.end_date = event.start_date
        if not event.end_time and event.start_time:
            event.end_time = event.start_time
        elif not event.end_time:
            event.end_time = datetime.datetime.min.time()
        if not event.start_time:
            event.start_time = datetime.datetime.min.time()
#         # if event.end_date < event.start_date:
#         #     event.end_date, event.start_date = event.start_date, event.end_date
        queryset = OverTimeSchedule.objects.filter(
            id=event.id
        )
        team=Teams.objects.get(team_type=event.team_type)
        CAL_ID=team.cal_id
        # rec='RRULE:FREQ=DAILY;COUNT='
        # rec+=str(instance.count)
        s="Number of slots available are "+ str(event.no_of_slots)
          # https://stackoverflow.com/questions/1555060/how-to-save-a-model-without-sending-a-signal
        # this is used so that we can update the google event within this signal without reshooting this signal(signals shot every time an object is saved)
        event = {
            "summary": event.summary,
            "location": event.location or "",
            "description": s,
            "start": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.start_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": datetime.datetime.combine(
                    event.start_date, event.end_time
                ).isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "recurrence": [],
            "reminders": {},
        }

        if created or not instance.google_link:
            try:
                event = (
                    service.events()
                    .insert(
                        calendarId=CAL_ID,
                        body=event,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                # print("An error occurred: %s" % error)
                pass
        else:
            try:
                event = (
                    service.events()
                    .update(
                        calendarId=CAL_ID,
                        body=event,
                        eventId=instance.google_link,
                    )
                    .execute()
                )
                queryset.update(google_link=event["id"])
            except HttpError as error:
                # print("An error occurred: %s" % error)
                pass
        # print("#############ADDED NEW       #############")


def overtime_delete_event(sender, instance, **kwargs):
    """this function deletes an event from google agenda when deleted in the website"""
    team=Teams.objects.get(team_type=instance.team_type)
    CAL_ID=team.cal_id
    try:
        service = overtime_calendar()
        service.events().delete(
            calendarId=CAL_ID,
            eventId=instance.google_link,
        ).execute()
    except:
        pass


post_save.connect(overtime_handle_event, sender=OverTimeSchedule)
post_delete.connect(overtime_delete_event, sender=OverTimeSchedule)