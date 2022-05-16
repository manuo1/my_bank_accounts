import re
import dateparser
import pdfplumber

from datetime import date
from decimal import Decimal, InvalidOperation


from bank_account_statements.constants import (
    CA_CHECKSUM_KEY_WORD, 
    CA_HEADER_ROW_INDICATOR, 
    CA_NEW_BALANCE_KEY_WORD, 
    CA_NEW_ROW_INDICATOR, 
    CA_OLD_BALANCE_KEY_WORD, 
    DATE_FORMAT
    )

def get_date_in_filename(filename, date_formats):
    raw_date = re.findall("\d{1,4}[-/_]\d{1,4}[-/_]\d{1,4}",filename)
    if raw_date and date_formats:
        return dateparser.parse(raw_date[0],languages=[date_formats])

def get_base_date_format(date):
    if date:
        return date.strftime(DATE_FORMAT)


class CreditAgricolPdfStatement:
    

    def _tables_in_pdf(self, pdf_path):
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    tables.append(table)
        return tables
    

    def _row_is_a_starting_row(self, row):
        return row[-1] == CA_NEW_ROW_INDICATOR

    def _row_is_lablel_row(self, row):
        return row[-1] == CA_HEADER_ROW_INDICATOR

    def _string_value_to_decimal(self, string_value):
        value = None
        string_value = string_value.replace(',', '.').replace(' ', '')
        try:
            value = Decimal(string_value)
        except InvalidOperation:
            print(f"Impossible de convertir {string_value} en decimal")
        return value

    def _get_all_rows_in_pdf(self, pdf_path):
        page_rows = []
        for table in self._tables_in_pdf(pdf_path):
            for row in table:
                if not self._row_is_lablel_row(row):
                    page_rows.append(row)
        return page_rows

    def _group_multi_line_descriptions(self, page_rows):
        while '' in [row[-1] for row in page_rows]:
            for row_number, row in enumerate(page_rows):
                if not self._row_is_a_starting_row(row):
                    page_rows[row_number-1][2] = (
                        page_rows[row_number-1][2]
                        + " "
                        + row[2]
                    )
                    page_rows.pop(row_number)
                    break

    def _remove_newline_character(self, label):
        label = label.replace('\n',' ')
        return label

    def _get_checksum(self, all_rows):
        checksum = 0
        for row in all_rows:
            if CA_CHECKSUM_KEY_WORD in row[2]:
                try:
                    checksum = (
                        self._string_value_to_decimal(row[4])
                        - self._string_value_to_decimal(row[3])
                    )
                    all_rows.remove(row)
                except ValueError:
                    print("Problème dans le calcul du CheckSum")
        return checksum

    def _get_start_and_end_periods(self, all_rows):
        start_date = None
        end_date = None
        for row in all_rows:
            if CA_OLD_BALANCE_KEY_WORD in row[2]:
                start_date = dateparser.parse(row[2][-10:],languages=['fr'])
                all_rows.remove(row)
            if CA_NEW_BALANCE_KEY_WORD in row[2]:
                end_date = dateparser.parse(row[2][-10:],languages=['fr'])
                all_rows.remove(row)

        return start_date, end_date

    def _build_row_date(self, all_rows, start_date , end_date):
        for row in all_rows:
            row_day , row_month = row[0].split(".")
            row_year = start_date.year
            # row month < start date month we changed year, it's january
            if int(row_month) < start_date.month:
                row_year = end_date.year
            row[0] = date(row_year, int(row_month), int(row_day))

    def _format_list(self, all_rows):
        formated_list = []
        for row in all_rows:
            value = row[4]
            if row[3]:
                value = f"-{row[3]}"
            formated_list.append([row[0], self._remove_newline_character(row[2]) ,self._string_value_to_decimal(value)])
        return formated_list

    def _formatted_list_is_valid(self, formatted_list, checksum):
        operation_sum = 0
        for row in formatted_list:
            operation_sum += row[-1]
        if operation_sum == checksum:
            return True
        return False

    def get_transactions(self, pdf_path):
            all_rows = self._get_all_rows_in_pdf(pdf_path)
            checksum = self._get_checksum(all_rows)
            start_date , end_date = self._get_start_and_end_periods(all_rows)
            self._group_multi_line_descriptions(all_rows)
            self._build_row_date(all_rows, start_date , end_date)
            formatted_list = self._format_list(all_rows)
            if self._formatted_list_is_valid(formatted_list, checksum):
                return formatted_list
            return []

class CreditMutuelPdfStatement:
    
    def get_transactions(self, pdf_path):
        return []
