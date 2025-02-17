

Skip to content
Using Meeting Wolf Mail with screen readers
Enable desktop notifications for Meeting Wolf Mail.
   OK  No thanks


Signing contracts made easy
Request electronic signatures and easily manage vendor agreements, customer contracts, stakeholder sign-off, and more - all without leaving Google Workspace.
Try nowDismiss
Conversations
 
Program Policies
Powered by Google
Last account activity: 7 hours ago
Details
import datetime
import os.path
import mysql.connector

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.

  db = mysql.connector.MySQLConnection(host = "127.0.0.1", user = "root", password = "Asuafbf4kzAd", database = "meetingwolf_main")

  mycursor = db.cursor()

  mycursor.execute("SELECT * FROM customer")

  myresult = mycursor.fetchall()

  for x in myresult:
    print(x)

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "test.json", SCOPES
      )
      creds = flow.run_local_server(port=0, open_browser=False)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    calendar = service.calendars().get(calendarId='primary').execute()

    print(calendar)

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(error)


if __name__ == "__main__":
  main()
gCalInteractions.py
Displaying gCalInteractions.py.
