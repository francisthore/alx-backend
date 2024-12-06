import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const products = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

const findItemById = (id) => products.find(item => item.itemId === id);

const app = express();
const client = createClient();
const port = 1245;

const reserveStockById = async (itemId, stock) => 
  promisify(client.set).bind(client)(`item.${itemId}`, stock);

const getCurrentReservedStockById = async (itemId) => 
  promisify(client.get).bind(client)(`item.${itemId}`);

app.get('/list_products', (_, res) => {
  res.json(products);
});

app.get('/list_products/:itemId(\\d+)', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const product = findItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = parseInt(await getCurrentReservedStockById(itemId) || '0', 10);
  res.json({
    ...product,
    currentQuantity: product.initialAvailableQuantity - reservedStock,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const product = findItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = parseInt(await getCurrentReservedStockById(itemId) || '0', 10);
  if (reservedStock >= product.initialAvailableQuantity) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  await reserveStockById(itemId, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

const resetStock = async () => {
  await Promise.all(
    products.map(item => promisify(client.set).bind(client)(`item.${item.itemId}`, 0))
  );
};

app.listen(port, async () => {
  await resetStock();
  console.log(`API available on localhost port ${port}`);
});

export default app;
