import './tracing.js';
import express from 'express';
import axios from 'axios';
import { trace } from '@opentelemetry/api';

const app = express();
app.use(express.json());

const tracer = trace.getTracer('api-gateway');

app.get('/health', (req, res) => {
  res.status(200).json({ status: "UP" });
});

app.post('/api/orders', async (req, res) => {
  const span = trace.getActiveSpan();
  const traceId = span.spanContext().traceId;

  try {
    const { userId, items, email } = req.body;

    for (const item of items) {
      await axios.post(`${process.env.INVENTORY_SERVICE_URL}/inventory/reserve`, {
        sku: item.sku,
        quantity: item.quantity
      });
    }

    const orderResponse = await axios.post(`${process.env.ORDER_SERVICE_URL}/orders`, {
      userId,
      items
    });

    await axios.post(`${process.env.NOTIFICATION_SERVICE_URL}/notify`, {
      email,
      orderId: orderResponse.data.orderId
    });

    res.status(201).json({
      orderId: orderResponse.data.orderId,
      status: "CREATED",
      traceId
    });

  } catch (error) {
    res.status(400).json({
      error: error.message,
      traceId
    });
  }
});

app.listen(8080, () => {
  console.log("API Gateway running on port 8080");
});
