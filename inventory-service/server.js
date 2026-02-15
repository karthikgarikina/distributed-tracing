import './tracing.js';
import express from 'express';
import { trace, SpanStatusCode } from '@opentelemetry/api';

const app = express();
app.use(express.json());

const stock = {
  "SKU123": 10,
  "SKU999": 0
};

app.get('/health', (req, res) => {
  res.status(200).json({ status: "UP" });
});

app.post('/inventory/reserve', (req, res) => {
  const span = trace.getActiveSpan();
  const { sku, quantity } = req.body;

  if (!stock[sku] || stock[sku] < quantity) {
    if (span) {
      span.setStatus({ code: SpanStatusCode.ERROR });
      span.setAttribute("error", true);
    }
    return res.status(400).json({ error: "Out of stock" });
  }

  stock[sku] -= quantity;
  res.status(200).json({ status: "RESERVED" });
});

app.listen(8000, () => {
  console.log("Inventory Service running on port 8000");
});
