import time
import datetime

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

today = datetime.date.timedelta(days=1)
lastweek = today - datetime.timedelta(days=7)


class GarminModule:
    def __init__(self, config):
        self.invalid = False
        print("Garmin Module has been initiated")

        ## Initialize Garmin api with your credentials
        try:
            client_id = config["Garmin"]["email"]
            client_password = config["Garmin"]["password"]
            self.api = Garmin(client_id, client_password)
            self.api.login()

        except Exception as e:
            print("[Garmin Module] error trying to authenticate", e)
            self.invalid = True

    def getLastActivity(self):
        last_activity = self.api.get_last_activity()
        return (
            last_activity["distance"],
            last_activity["duration"],
            last_activity["averageSpeed"],
            last_activity["averageHR"],
            last_activity["averageRunningCadenceInStepsPerMinute"],
        )

    def getSleedData(self):
        sleep_data = self.api.get_sleep_data(today.isoformat())
        print("[Garmin Module] getSleedData called")
        print(today)
        print(sleep_data["dailySleepDTO"])
        print("DEEP SLEEP " + str(sleep_data["dailySleepDTO"]["deepSleepSeconds"]))
        return (
            sleep_data["dailySleepDTO"]["unmeasurableSleepSeconds"],
            sleep_data["dailySleepDTO"]["deepSleepSeconds"],
            sleep_data["dailySleepDTO"]["lightSleepSeconds"],
            sleep_data["dailySleepDTO"]["remSleepSeconds"],
        )
