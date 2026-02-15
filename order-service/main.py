import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from database import SessionLocal, init_db, Order, engine
from tracing import setup_tracing

app = FastAPI()

setup_tracing(app, engine)
init_db()

tracer = trace.get_tracer(__name__)

class Item(BaseModel):
    sku: str
    quantity: int
    price: float

class OrderRequest(BaseModel):
    userId: int
    items: list[Item]

@app.get("/health")
def health():
    return {"status": "UP"}

@app.post("/orders")
def create_order(order: OrderRequest):
    with tracer.start_as_current_span("process_order") as span:

        order_id = str(uuid.uuid4())

        total_price = sum(item.quantity * item.price for item in order.items)

        span.set_attribute("user.id", order.userId)
        span.set_attribute("order.id", order_id)
        span.add_event("inventory_checked")

        db: Session = SessionLocal()

        db_order = Order(
            id=order_id,
            user_id=order.userId,
            total_price=total_price
        )

        db.add(db_order)
        db.commit()
        db.close()

        span.set_status(Status(StatusCode.OK))

        return {"orderId": order_id}
