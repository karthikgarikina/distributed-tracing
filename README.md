# 🚀 Distributed Tracing Microservices Project

## 📌 Overview

This project demonstrates **Distributed Tracing** across multiple
microservices using:

-   API Gateway (Node.js + Express)
-   Inventory Service (Node.js + Express)
-   Order Service (FastAPI + PostgreSQL)
-   Notification Service (FastAPI)
-   PostgreSQL Database
-   Jaeger (OpenTelemetry Collector + UI)

All services are fully dockerized and communicate internally using
Docker networking.\
Tracing is implemented using **OpenTelemetry** and exported to
**Jaeger**.

------------------------------------------------------------------------

# 🏗 Architecture

Client\
↓\
API Gateway (8080)\
↓\
Inventory Service (8000)\
↓\
Order Service (8000 + PostgreSQL)\
↓\
Notification Service (8000)\
↓\
Jaeger (16686)

Each request generates a single traceId that propagates across all
services.

------------------------------------------------------------------------

# 🐳 How To Run The Project

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd distributed-tracing
```
## 2️⃣ Build and Start Services
```bash
docker-compose up --build
```
Wait until all services show **healthy** status.
------------------------------------------------------------------------

# 🌐 Service URLs

  Service       URL
  ------------- ------------------------
  API Gateway   http://localhost:8080
  Jaeger UI     http://localhost:16686
  PostgreSQL    localhost:5432

------------------------------------------------------------------------

# 📮 API Endpoints

## 🔹 Health Checks

GET /health

Available in: - API Gateway - Inventory Service - Order Service -
Notification Service

------------------------------------------------------------------------

## 🔹 Create Order

POST http://localhost:8080/api/orders

### Request Body:

``` json
{
  "userId": "user-1",
  "email": "test@example.com",
  "items": [
    {
      "sku": "SKU123",
      "quantity": 1
    }
  ]
}
```

### Response:

``` json
{
  "orderId": "generated-uuid",
  "status": "CREATED",
  "traceId": "generated-trace-id"
}
```

------------------------------------------------------------------------

# 🔍 Viewing Traces in Jaeger

1.  Open: http://localhost:16686
2.  Select Service: **api-gateway**
3.  Click **Find Traces**
4.  Open a trace to see full request flow across services.

------------------------------------------------------------------------

# 📊 analyze-traces.sh Script

This script analyzes traces using Jaeger API.

## Usage (Linux / Git Bash):

``` bash
chmod +x analyze-traces.sh
./analyze-traces.sh 100
```

This prints trace IDs with duration greater than the threshold (in
milliseconds).

------------------------------------------------------------------------

# 🗄 Database

-   PostgreSQL 15
-   Tables auto-created on startup using SQLAlchemy
-   No manual seeding required
-   Orders are created dynamically when API is called

------------------------------------------------------------------------

# 🔄 Trace Flow

When POST /api/orders is called:

1.  API Gateway creates root span
2.  Calls Inventory Service (reserve stock)
3.  Calls Order Service (save to DB)
4.  Calls Notification Service (send notification)
5.  All spans share the same traceId

------------------------------------------------------------------------

# 📦 Docker Services

-   api_gateway
-   inventory_service
-   order_service
-   notification_service
-   postgres
-   jaeger

All services are connected using Docker internal network.

------------------------------------------------------------------------

# 🎥 Demo Video

📹 Demo Video Link:\
(Add your demo video link here)

------------------------------------------------------------------------

# 📄 Submission Notes

-   All services are dockerized
-   Distributed tracing implemented using OpenTelemetry
-   Jaeger UI exposed on port 16686
-   analyze-traces.sh included
-   No hardcoded traceId (generated dynamically at runtime)

