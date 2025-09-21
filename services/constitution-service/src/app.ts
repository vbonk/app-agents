import express from 'express';
import pool from './db';

const app = express();

app.use(express.json());

app.post('/constitutions', async (req, res) => {
  console.log("POST /constitutions received with body:", req.body);
  try {
    const { name, description, rules } = req.body;
    console.log("Destructured body:", { name, description, rules });
    const newConstitution = await pool.query(
      'INSERT INTO constitutions (name, description, rules) VALUES ($1, $2, $3) RETURNING *',
      [name, description, rules]
    );
    console.log("Database response:", newConstitution.rows[0]);
    res.json(newConstitution.rows[0]);
  } catch (err: any) {
    console.error("Error in POST /constitutions:", err);
    res.status(500).send('Server Error');
  }
});

app.get('/constitutions', async (req, res) => {
  console.log("GET /constitutions received");
  try {
    const allConstitutions = await pool.query('SELECT * FROM constitutions');
    console.log("Database response:", allConstitutions.rows);
    res.json(allConstitutions.rows);
  } catch (err: any) {
    console.error("Error in GET /constitutions:", err);
    res.status(500).send('Server Error');
  }
});

app.get('/constitutions/:id', async (req, res) => {
  console.log(`GET /constitutions/${req.params.id} received`);
  try {
    const { id } = req.params;
    const constitution = await pool.query('SELECT * FROM constitutions WHERE id = $1', [
      id,
    ]);
    console.log("Database response:", constitution.rows[0]);
    res.json(constitution.rows[0]);
  } catch (err: any) {
    console.error(`Error in GET /constitutions/${req.params.id}:`, err);
    res.status(500).send('Server Error');
  }
});

app.put('/constitutions/:id', async (req, res) => {
  console.log(`PUT /constitutions/${req.params.id} received with body:`, req.body);
  try {
    const { id } = req.params;
    const { name, description, rules } = req.body;
    const updateConstitution = await pool.query(
      'UPDATE constitutions SET name = $1, description = $2, rules = $3 WHERE id = $4 RETURNING *',
      [name, description, rules, id]
    );
    console.log("Database response:", updateConstitution.rows[0]);
    res.json(updateConstitution.rows[0]);
  } catch (err: any) {
    console.error(`Error in PUT /constitutions/${req.params.id}:`, err);
    res.status(500).send('Server Error');
  }
});

app.delete('/constitutions/:id', async (req, res) => {
  console.log(`DELETE /constitutions/${req.params.id} received`);
  try {
    const { id } = req.params;
    await pool.query('DELETE FROM constitutions WHERE id = $1', [id]);
    console.log("Database response: Constitution deleted");
    res.json('Constitution was deleted!');
  } catch (err: any) {
    console.error(`Error in DELETE /constitutions/${req.params.id}:`, err);
    res.status(500).send('Server Error');
  }
});

export default app;

