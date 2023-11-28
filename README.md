# Tasker-SleepAsAndroid-Alarm-Reader
This task can read out the [alarm content provider](https://docs.sleep.urbandroid.org/devs/content_provider_api.html) from the SleepAsAndroid app.
Launching the app with launch data set will prompt it to read out the alarms, and subsequently send an intent with the data (which can then be processed within Tasker).

## Installation
- Install the apk directly, or convert the `Read_Content_Provider_Alarms.xml` task to an app yourself using Tasker app factory (i.e. if you want a different splitter between data columns). If you do so, in the export screen, add the extra permission `com.urbandroid.sleep.READ`.
- After installing, go to the Read Content Provider App info --> permissions --> Additional Permissions and allow the `Read Sleep Data` permission.

## Usage
The two xml files in the `profile examples` folder give two tasks that work concurrently to read out the alarms automatically whenever you change an alarm in the SleepAsAndroid app. These are just examples to show how it works, however. The `call_reader.xml` task simply launches the app when a reschedule happens, which prompts the app to read out the database and send the intent with the data. The profile `receive_and_process_intent.xml` receives the intent, and subsequently splits up the data rows and columns. In my case, the attached app figures out the next alarm so I can display it on my home screen (I don't like the widget the app provides). 
However I also have a task that sends the data to Home Assistant, so I can show my alarms in there.

## Other Notes
Although the docs from SleepAsAndroid show the supposed indices for the retrieved data, upon experimenting I found it to have 12 indices in total, and the indices did not seem to correspond. Below is what I found in the indices so far. I did this in python, hence the index starts at 0, however Tasker has its arrays start at 1. At least those years of Matlab in uni are paying off now.
```
Alarm query results indices:
[0]: ?
[1]: some null value idk
[2]: ?
[3]: Alarm Label
[4]: Boolean, for enabled/disabled
[5]: -1 for everything; some setting
[6]: Alarm Hour
[7]: ? some integer but feels too inconsistent to be the minutes
[8]:  Some link to the directory or something
[9]: -1 for everything; some setting
[10]: Unix timestamp in milliseconds; always corresponds to set time (i.e., includes skips and postpone)
[11]: -1 if alarm not skipped, otherwise timestamp with original timestamp
[12]: integer; I think the alarm ID
```
