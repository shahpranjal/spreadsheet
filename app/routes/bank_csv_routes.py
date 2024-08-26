from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models.bank_csv import BankCsv
from app.forms import BankCsvForm

bank_csv_bp = Blueprint('bank_csv_bp', __name__)


@bank_csv_bp.route('/banks', methods=['GET', 'POST'])
def manage_banks():

    form = BankCsvForm()
    if form.validate_on_submit():
        bank = BankCsv.query.filter_by(bank_name=form.bank_name.data).first()
        if bank:
            # Update existing bank
            bank.date_column = form.date_column.data
            bank.debit_column = form.debit_column.data
            bank.credit_column = form.credit_column.data
            bank.description_column = form.description_column.data
            flash(f'Updated {form.bank_name.data}', 'success')
        else:
            # Create new bank
            bank = BankCsv(
                bank_name=form.bank_name.data,
                date_column=form.date_column.data,
                debit_column=form.debit_column.data,
                credit_column=form.credit_column.data,
                description_column=form.description_column.data
            )
            db.session.add(bank)
            flash(f'Created {form.bank_name.data}', 'success')
        db.session.commit()
        return redirect(url_for('bank_csv_bp.manage_banks'))

    banks = BankCsv.query.all()
    return render_template('manage_banks.html', form=form, banks=banks)


@bank_csv_bp.route('/edit-bank/<int:bank_id>', methods=['GET', 'POST'])
def edit_bank(bank_id):
    bank = BankCsv.query.get_or_404(bank_id)
    form = BankCsvForm(obj=bank)
    if form.validate_on_submit():
        bank.bank_name = form.bank_name.data
        bank.date_column = form.date_column.data
        bank.debit_column = form.debit_column.data
        bank.credit_column = form.credit_column.data
        bank.description_column = form.description_column.data
        db.session.commit()
        flash(f'Updated {bank.bank_name}', 'success')
        return redirect(url_for('bank_csv_bp.manage_banks'))

    return render_template('edit_bank.html', form=form, bank=bank)
