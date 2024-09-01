from app.models import File, Transaction, db
from dateutil import parser as date_parser


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
            columns = line.split(',')
            date_index = self.bank_csv.date_column - 1
            debit_index = self.bank_csv.debit_column - 1
            credit_index = self.bank_csv.credit_column - 1
            description_index = self.bank_csv.description_column - 1
            date = date_parser.parse(columns[date_index])
            if self.start_date is None or self.start_date > date:
                self.start_date = date
            if self.end_date is None or self.end_date < date:
                self.end_date = date
            transaction = Transaction(
                date=date,
                debit=float(columns[debit_index]) if columns[debit_index] else 0.0,
                credit=float(columns[credit_index]) if columns[credit_index] else 0.0,
                description=columns[description_index],
                user_id=self.user.id,
                bank_id=self.bank_csv.id
            )
            return transaction
        except Exception as e:
            return str(e)  # Return the error message

    def process(self):
        try:
            for line in self.file:
                line = line.decode('utf-8').strip()
                transaction = self.parse_line(line)
                if isinstance(transaction, str):  # Check if an error was returned
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
