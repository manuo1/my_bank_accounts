import re
import dateparser

from bank_account_statements.constants import DATE_FORMAT

def get_date_in_filename(filename, date_formats):
    raw_date = re.findall("\d{1,4}[-/_]\d{1,4}[-/_]\d{1,4}",filename)
    if raw_date and date_formats:
        return dateparser.parse(raw_date[0],languages=[date_formats])

def formated_date(date):
    if date:
        return date.strftime(DATE_FORMAT)