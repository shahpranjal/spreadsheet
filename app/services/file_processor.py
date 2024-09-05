import io
import re

from app.models import File, Transaction, db
from dateutil import parser as date_parser
import csv


class FileProcessor:
    def __init__(self, file, user, bank_csv):
        self.file = file
        self.user = user
        self.bank_csv = bank_csv
        self.start_date = None
        self.end_date = None
        self.transactions = []

    def parse_line(self, line):
        try:
            csv_file = io.StringIO(line)
            columns = next(csv.reader(csv_file))
            date_index = self.bank_csv.date_column - 1
            debit_index = self.bank_csv.debit_column - 1
            credit_index = self.bank_csv.credit_column - 1
            description_index = self.bank_csv.description_column - 1
            date = date_parser.parse(columns[date_index])
            debit = self.parse_amount(columns[debit_index]) if columns[debit_index] else 0.0
            credit = self.parse_amount(columns[credit_index]) if columns[credit_index] else 0.0
            if self.start_date is None or self.start_date > date:
                self.start_date = date
            if self.end_date is None or self.end_date < date:
                self.end_date = date
            if debit_index == credit_index:
                if debit < 0:
                    debit = 0
                if credit > 0:
                    credit = 0
            if credit > 0 or debit < 0:
                return "All credit values must be < 0 and debit values must be > 0"
            transaction = Transaction(
                date=date,
                debit=debit,
                credit=credit,
                description=columns[description_index].title(),
                user_id=self.user.id,
                bank_id=self.bank_csv.id
            )
            return transaction
        except Exception as e:
            return str(e)  # Return the error message

    def process(self):
        try:
            for line_num, line in enumerate(self.file, start=1):
                line = line.decode('utf-8').strip().lower()
                transaction = self.parse_line(line)
                if isinstance(transaction, str):
                    if line_num == 1 and 'date' in transaction:
                        continue
                    return {"error": transaction}

                self.transactions.append(transaction)

            # If all lines are processed without errors, store the transactions
            db.session.add_all(self.transactions)

            # Create and store the File object
            file_record = File(
                type='csv',
                user_id=self.user.id,
                bank_id=self.bank_csv.id,
                start_date=self.start_date,
                end_date=self.end_date,
                filename=self.file.filename
            )
            db.session.add(file_record)

            # Commit the transactions and file to the database
            db.session.commit()

            return {"message": "File processed successfully"}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def parse_amount(amount_str):
        amount_str = amount_str.strip()
        pattern = r'[^\d.,-]+'  # Remove anything that is not a digit, comma, period, or minus

        # Remove currency symbols or extra characters like '$', '€', etc.
        cleaned_amount = re.sub(pattern, '', amount_str)

        # Replace commas with periods if necessary
        if ',' in cleaned_amount and '.' not in cleaned_amount:
            cleaned_amount = cleaned_amount.replace(',', '.')

        # Remove thousands separators (commas or periods in some locales)
        cleaned_amount = cleaned_amount.replace(',', '')

        # Convert to float
        try:
            return float(cleaned_amount)
        except ValueError:
            raise ValueError(f"Unable to parse the amount: {amount_str}")
