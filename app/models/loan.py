from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.services.database import Base


class Loan(Base):
    __tablename__ = 'loan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    client_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    matured_on = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    updated_on = Column(DateTime, nullable=True)

    # Relationship to track associated payments
    payments = relationship("Payment", back_populates="loan")

    def __repr__(self):
        return f"<Loan(id={self.id}, amount={self.amount}, client_id={self.client_id})>"
