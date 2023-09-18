from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from app.models import Loan
from app.services.database import Session
from app.services.database import query_database
from app.utils import format_date

loans_blueprint = Blueprint('loans', __name__)


@loans_blueprint.route('/<int:loan_id>', methods=['GET'])
def get_loan_data(loan_id):
    try:
        loan = Session.query(Loan).filter_by(id=loan_id).one()
        loan_data = {
            "id": loan.id,
            "amount": loan.amount,
            "client_id": loan.client_id,
            "created_on": format_date(loan.created_on),
            "duration": loan.duration,
            "matured_on": format_date(loan.matured_on) if loan.matured_on else None,
            "status": loan.status,
            "updated_on": format_date(loan.updated_on) if loan.updated_on else None
        }
        return jsonify(loan_data)
    except NoResultFound:
        return jsonify({"error": "Loan not found"}), 404


@loans_blueprint.route('/<int:loan_id>/payments', methods=['GET'])
def get_payments_by_loan(loan_id):
    data = query_database(text("SELECT * FROM public.payment WHERE loan_id = :loan_id"), {"loan_id": loan_id})

    if data:
        payments = []
        for row in data:
            payment = {
                "id": row[0],
                "loan_id": row[1],
                "amount": row[2],
                "principle": row[3],
                "interest": row[4],
                "status": row[5],
                "created_on": row[6].strftime('%a, %d %b %Y %H:%M:%S GMT')
            }
            payments.append(payment)
        return jsonify(payments)
    else:
        return jsonify({"error": "No payments found for the given loan ID"}), 404
