from datetime import timedelta

def format_date(date):
    return (date + timedelta(hours=7)).strftime("%d-%m-%Y %H:%M:%S")
