import datetime
def datetime_validation(date_text):
        try:
            datetime.datetime.strptime(date_text.replace("'", ""), "D:%Y%m%d%H%M%S%z")
            return True
        except ValueError:
            return False

