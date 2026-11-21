from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


STATUSES = ("pending", "paid", "shipped", "cancelled")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total >= 0"),
        CheckConstraint("status IN ('pending','paid','shipped','cancelled')"),
        {"sqlite_autoincrement": True},
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def to_dict(self):
        return {"id": self.id, "customer": self.customer, "status": self.status,
                "total": self.total, "created_at": self.created_at.isoformat(timespec="microseconds") + "Z"}
