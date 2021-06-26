import datetime

from utility.HourPicker import HourPicker


class HourPickerImpl(HourPicker):
    def getHour(self):
        now = datetime.datetime.now()
        return "{:02d}:{:02d}".format(now.hour, now.minute)
