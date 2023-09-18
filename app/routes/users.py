import pandas as pd
import xgboost as xgb
from flask import current_app
from flask import jsonify, Blueprint
from joblib import load
from sqlalchemy.exc import SQLAlchemyError

from app.models import User, Loan, Payment
from app.services.database import Session
from app.utils import format_date

users_blueprint = Blueprint('users', __name__)

model = xgb.Booster()

# Check file existence and accessibility
model_path_v1 = 'app/routes/model_v1.pk1'
model_path_v2 = 'app/routes/model_v2.joblib'
model = load(model_path_v2)


@users_blueprint.route('/<personal_code>', methods=['GET'])
def get_user_data(personal_code):
    try:
        user = Session.query(User).filter_by(personal_code=personal_code).first()

        if user:
            return jsonify({
                "id": user.id,
                "created_on": format_date(user.created_on),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "birth_date": format_date(user.birth_date),
                "personal_code": user.personal_code
            })
        else:
            return jsonify({"message": "User not found"}), 404

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error occurred"}), 500
    finally:
        Session.remove()


@users_blueprint.route('/<int:client_id>/loans', methods=['GET'])
def get_loans_by_user(client_id):
    try:
        loans_query = Session.query(Loan).filter_by(client_id=client_id).all()

        if loans_query:
            loans = [{
                "amount": loan.amount,
                "client_id": loan.client_id,
                "created_on": format_date(loan.created_on),
                "duration": loan.duration,
                "id": loan.id,
                "matured_on": format_date(loan.matured_on),
                "status": loan.status,
                "updated_on": format_date(loan.updated_on)
            } for loan in loans_query]
            return jsonify(loans)
        else:
            return jsonify({"message": "No loans found for the given user ID"}), 404

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        Session.remove()


@users_blueprint.route('/<int:client_id>/payments', methods=['GET'])
def get_payments_by_user(client_id):
    try:
        payments_query = Session.query(Payment).join(Loan).filter(Loan.client_id == client_id).all()

        if payments_query:
            payments = [{
                "id": payment.id,
                "loan_id": payment.loan_id,
                "amount": payment.amount,
                "principle": payment.principle,
                "interest": payment.interest,
                "status": payment.status,
                "created_on": format_date(payment.created_on)
            } for payment in payments_query]
            return jsonify(payments)
        else:
            return jsonify({"message": "No payments found for the given user ID"}), 404

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        Session.remove()


@users_blueprint.route('/<int:client_id>/unpaid_loans', methods=['GET'])
def get_unpaid_loans_by_user(client_id):
    try:
        loans_query = Session.query(Loan).filter_by(client_id=client_id, status="overdue").all()

        if loans_query:
            loans = [{
                "amount": loan.amount,
                "client_id": loan.client_id,
                "created_on": format_date(loan.created_on),
                "duration": loan.duration,
                "id": loan.id,
                "matured_on": format_date(loan.matured_on),
                "status": loan.status,
                "updated_on": format_date(loan.updated_on)
            } for loan in loans_query]
            return jsonify(loans)
        else:
            return jsonify({"message": "No unpaid loans found for the given user ID"}), 404

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        Session.remove()


@users_blueprint.route('/<int:client_id>/predict', methods=['GET'])
def predict(client_id):
    try:
        # Fetch User, Loan, and Payment information for the given client_id
        user_query = Session.query(User).filter_by(id=client_id).first()
        loans_query = Session.query(Loan).filter_by(client_id=client_id).all()
        payments_query = Session.query(Payment).join(Loan, Loan.id == Payment.loan_id).filter(
            Loan.client_id == client_id).all()

        # Check if records exist
        if not user_query or not loans_query:
            return jsonify({"message": "No user or loan records found for the given user ID"}), 404

        # Extract relevant data
        current_year = pd.Timestamp.now().year
        age = current_year - user_query.birth_date.year

        amount = sum([loan.amount for loan in loans_query])
        duration = sum([loan.duration for loan in loans_query if loan.status in ['paid', 'overdue']])

        # Calculate principal and interest based on payments
        principle = sum([payment.principle for payment in payments_query])
        interest = sum([payment.interest for payment in payments_query])

        # Payment status
        late_payments = len([payment for payment in payments_query if payment.status == 'late'])
        on_time_payments = len([payment for payment in payments_query if payment.status == 'on_time'])
        no_payments = len(loans_query) - late_payments - on_time_payments

        # Predefined list of features based on the training dataset
        features = ['amount_x', 'duration', 'age', 'principle', 'interest', 'status_y_late', 'status_y_no_payment',
                    'status_y_on_time']

        # Create a data dictionary initialized with zeros for all features
        data = {feature: 0 for feature in features}

        # Update the necessary features based on the fetched data
        data["amount_x"] = amount
        data["duration"] = duration
        data["age"] = age
        data["principle"] = principle
        data["interest"] = interest
        data["status_y_late"] = late_payments
        data["status_y_on_time"] = on_time_payments
        data["status_y_no_payment"] = no_payments

        # Convert data to DataFrame, ensuring the columns are in the correct order
        df = pd.DataFrame([data], columns=features)
        prediction = model.predict(df)

        result = int(prediction[0])
        # Return the prediction outcome
        message = "Loan Approved" if result == 1 else "Loan Denied"
        return jsonify({"outcome": str(result), "message": message, "client_id": client_id})

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        Session.remove()
