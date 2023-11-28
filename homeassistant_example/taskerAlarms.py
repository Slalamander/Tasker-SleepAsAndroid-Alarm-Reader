from datetime import datetime as dt, timedelta

#Alarm query results indices:
#[0]: ?
#[1]: some null value idk
#[2]: ?
#[3]: Alarm Label
#[4]: Boolean, for enabled/disabled
#[5]: -1 for everything; some setting
#[6]: Alarm Hour
#[7]: ? some integer but feels too inconsistent to be the minutes
#[8]:  Some link to the directory or something
#[9]: -1 for everything; some setting
#[10]: Unix timestamp in milliseconds; always corresponds to set time (i.e., includes skips and postpone)
#[11]: -1 if alarm not skipped, otherwise timestamp with original timestamp
#[12]: integer; I think the alarm ID

@service("pyscript.tasker_sleep_alarms")
def process_sleepAsAndroid_Alarms_Tasker(alarm_query_res = None, person=None, persist=False, show_disabled=True, include_unnamed=True):
    """yaml
name: Process SleepAsAndroid Alarms Tasker
description: Processes the alarms from the Tasker grab into readable form.
fields:
  alarm_query_res:
     name: Alarm Query Result
     description: The result from the sql query the tasker kid app performed
     required: true
     selector:
        text:
  fromApp:
     name: Send From App
     description: App which send the message. Mainly to prevent accidentally calling the service
     example: Tasker
     required: false
     selector:
        text:
  persist:
     title: Persistent Entities
     description: Make the sensors persistent pyscript entities
     required: false
     selector:
        boolean:
  show_disabled:
     title: Show Disabled Alarms
     description: Show disabled Alarms in the all alarms sensor (categorised as enabled/disabled)
     required: false
     selector:
        boolean:
  include_unnamed:
     title: Include Unnamed Alarms
     description: Include Unnamed Alarms in the all alarms sensor (Enabled Unnamed Alarms are always taken into account for the next alarm sensor)
     required: false
     selector:
        boolean:
"""
    #log.warning(f"From {fromApp} got logcat {alarm_logcat}")
    alarms_list = alarm_query_res.split(",")
    column_divider = "|"
    all_alarms = {"enabled": {}, "disabled": {}}
    on_alarms = {}
    unnamed_alarms = 0

    dom = "pyscript" if persist else "sensor"

    if person != None:
        entity_id_all = f"{dom}.sleepAlarms_{person}"
        friendly_name_all = f"Sleep as Android Alarms {person}"
        entity_id_next = f"{dom}.next_sleepAlarm_{person}"
        friendly_name_next = f"Next Sleep as Android Alarm {person}"
    else:
        entity_id_all = f"{dom}.sleepAlarms"
        friendly_name_all = f"Sleep as Android Alarms"
        entity_id_next = f"{dom}.next_sleepAlarm"
        friendly_name_next = f"Next Sleep as Android Alarm"

    for alarm_str in alarms_list:
        alarm_lst = alarm_str.split(column_divider)
        alarm_dict = {}
        if alarm_lst[3] != "":
            alarm_name = alarm_lst[3] 
        else:
            if unnamed_alarms == 0:
                unnamed_alarms += 1
                alarm_name = "Unnamed Alarm"
            elif unnamed_alarms == 1:
                print("Found a second unnamed alarm")
                
                if "Unnamed Alarm" in all_alarms["enabled"]:
                    all_alarms["enabled"]["Unnamed Alarm 1"] = all_alarms["enabled"].pop("Unnamed Alarm")
                elif "Unnamed Alarm" in all_alarms["disabled"]:
                     all_alarms["disabled"]["Unnamed Alarm 1"] = all_alarms["disabled"].pop("Unnamed Alarm")
                unnamed_alarms += 1
                alarm_name = f"Unnamed Alarm {unnamed_alarms}"
            else:
                unnamed_alarms += 1
                alarm_name = f"Unnamed Alarm {unnamed_alarms}"

        alarm_dict["alarm_id"] = alarm_lst[12]
        al_timestamp = float(alarm_lst[10])
        dt_alarm = dt.fromtimestamp(al_timestamp/1000)
        
        #alarm_time = dt_alarm.strftime("%a %H:%M")
        delta = dt.today() - dt_alarm
        if delta.days == 0:
             alarm_time = f'Today {dt_alarm.strftime("%H:%M")}'
        elif delta.days == 1:
             alarm_time = f'Tomorrow {dt_alarm.strftime("%H:%M")}'
        elif delta.days > 6:
            alarm_time = dt_alarm.strftime("%d %b %H:%M")
        else:
            alarm_time = dt_alarm.strftime("%a %H:%M")

        alarm_dict["time"] = alarm_time
        alarm_dict["timestamp"] = alarm_lst[10]
        
        if alarm_lst[4] == "1":
            alarm_dict["enabled"] = True
            dict_cat = "enabled"
            on_alarms[alarm_name] = float(alarm_lst[10])
        else:
            alarm_dict["enabled"] = False
            dict_cat = "disabled"

        if int(alarm_lst[11]) != -1:
            alarm_dict["skipped"] = True
            alarm_time_or = dt.fromtimestamp(float(alarm_lst[11])/1000)
            alarm_time_or = alarm_time_or.strftime("%a %H:%M")
            alarm_dict["original_time"] = alarm_time_or
        else:
            alarm_dict["skipped"] = False

        #print(f"{line_lst[3]}: {len(line_lst)}")
        if alarm_name != "":
            #log.warning(f"Got a named alarm processed as {alarm_dict}")
            all_alarms[dict_cat][alarm_name] = alarm_dict
        elif include_unnamed:
            all_alarms[dict_cat][alarm_name] = alarm_dict
        

    all_alarms["unit_of_measurement"] = "Alarms"
    all_alarms["friendly_name"] = friendly_name_all
    
    if not show_disabled:
        all_alarms.pop("disabled")

    state.set(entity_id_all, value=len(all_alarms["enabled"].keys()), new_attributes=all_alarms)

    if not on_alarms:
        state_next = "None Set"
        next_attr = {"friendly_name": friendly_name_next}
    else:
        next_alarm = min(on_alarms, key=on_alarms.get)
        next_alarm_dict =  all_alarms["enabled"][next_alarm]
        state_next = next_alarm_dict["time"]
        next_attr = {
            "friendly_name": friendly_name_next,
            "alarm_name": next_alarm,
            "timestamp": next_alarm_dict["timestamp"]
        }
        if next_alarm_dict["skipped"]:
            next_attr["skipped"] = True
            next_attr["original_time"] = next_alarm_dict["original_time"]
    
    state.set(entity_id_next, value=state_next, new_attributes=next_attr)

@service("pyscript.delete_sleep_alarms_entity")
def delete_sleepAlarm(entity_id=None):
    """yaml
name: Delete Pyscript Alarm Entity
description: Processes the alarms from the Tasker grab into readable form.
fields:
  entity_id:
     name: sleepAlarm entity
     description: The sleepAlarm entity to delete
     required: true
     selector:
        entity:
"""

    if "sleepalarms" in entity_id:
        state.delete(entity_id)
    else:
        log.error(f"{entity_id} is does not belong to the sleepalarms pyscripts")