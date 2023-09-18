from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.services.database import Base


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey('loan.id'), nullable=False)
    amount = Column(Float, nullable=False)
    principle = Column(Float, nullable=False)
    interest = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)

    # Relationship to track associated loan
    loan = relationship("Loan", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, loan_id={self.loan_id}, amount={self.amount})>"
