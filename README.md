# Tasker-SleepAsAndroid-Alarm-Reader
This task can read out the [alarm content provider](https://docs.sleep.urbandroid.org/devs/content_provider_api.html) from the SleepAsAndroid app.
Launching the app with launch data set will prompt it to read out the alarms, and subsequently send an intent with the data (which can then be processed within Tasker).

## Installation
- Install the apk directly, or convert the `Read_Content_Provider_Alarms.xml` task to an app yourself using Tasker app factory (i.e. if you want a different splitter between data columns). If you do so, in the export screen, add the extra permission `com.urbandroid.sleep.READ`.
- After installing, go to the Read Content Provider App info --> permissions --> Additional Permissions and allow the `Read Sleep Data` permission.

## Usage
The two xml files in the `profile examples` folder give two tasks that work concurrently to read out the alarms automatically whenever you change an alarm in the SleepAsAndroid app. These are just examples to show how it works, however. The `call_reader.xml` task simply launches the app when a reschedule happens, which prompts the app to read out the database and send the intent with the data. The profile `receive_and_process_intent.xml` receives the intent, and subsequently splits up the data rows and columns. In my case, the attached app figures out the next alarm so I can display it on my home screen (I don't like the widget the app provides). 
However I also have a task that sends the data to Home Assistant, so I can show my alarms in there.
