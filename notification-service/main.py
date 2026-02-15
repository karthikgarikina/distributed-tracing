import time
import os
from fastapi import FastAPI
from pydantic import BaseModel

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

resource = Resource(attributes={
    "service.name": os.getenv("SERVICE_NAME")
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTLP_EXPORTER_ENDPOINT"),
    insecure=True
)

provider.add_span_processor(BatchSpanProcessor(exporter))
FastAPIInstrumentor.instrument_app(app)

class NotificationRequest(BaseModel):
    email: str
    orderId: str

@app.get("/health")
def health():
    return {"status": "UP"}

@app.post("/notify")
def notify(request: NotificationRequest):
    time.sleep(0.1)
    print(f"Email sent to {request.email} for order {request.orderId}")
    return {"status": "SENT"}
