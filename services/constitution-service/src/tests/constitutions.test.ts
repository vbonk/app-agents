import request from 'supertest';
import app from '../app'; // Import the app
import pool from '../db';

// Mock the entire db module
jest.mock('../db', () => ({
  __esModule: true,
  default: {
    query: jest.fn(),
    on: jest.fn(),
  },
}));

describe('Constitutions API', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should get all constitutions', async () => {
    const mockConstitutions = [{ id: 1, name: 'Test Constitution' }];
    (pool.query as jest.Mock).mockResolvedValue({ rows: mockConstitutions });

    const res = await request(app).get('/constitutions');

    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual(mockConstitutions);
    expect(pool.query).toHaveBeenCalledWith('SELECT * FROM constitutions');
  });

  it('should create a new constitution', async () => {
    const newConstitution = { name: 'New Constitution', description: 'A new one', rules: {} };
    (pool.query as jest.Mock).mockResolvedValue({ rows: [{ id: 2, ...newConstitution }] });

    const res = await request(app)
      .post('/constitutions')
      .send(newConstitution);

    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual({ id: 2, ...newConstitution });
    expect(pool.query).toHaveBeenCalledWith(
      'INSERT INTO constitutions (name, description, rules) VALUES ($1, $2, $3) RETURNING *',
      [newConstitution.name, newConstitution.description, newConstitution.rules]
    );
  });
});




  it('should get a constitution by id', async () => {
    const mockConstitution = { id: 1, name: 'Test Constitution' };
    (pool.query as jest.Mock).mockResolvedValue({ rows: [mockConstitution] });

    const res = await request(app).get('/constitutions/1');

    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual(mockConstitution);
    expect(pool.query).toHaveBeenCalledWith('SELECT * FROM constitutions WHERE id = $1', ["1"]);
  });

  it('should update a constitution', async () => {
    const updatedConstitution = { name: 'Updated Constitution', description: 'Updated', rules: {} };
    (pool.query as jest.Mock).mockResolvedValue({ rows: [{ id: 1, ...updatedConstitution }] });

    const res = await request(app)
      .put('/constitutions/1')
      .send(updatedConstitution);

    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual({ id: 1, ...updatedConstitution });
    expect(pool.query).toHaveBeenCalledWith(
      'UPDATE constitutions SET name = $1, description = $2, rules = $3 WHERE id = $4 RETURNING *',
      [updatedConstitution.name, updatedConstitution.description, updatedConstitution.rules, "1"]
    );
  });

  it('should delete a constitution', async () => {
    (pool.query as jest.Mock).mockResolvedValue({ rows: [] });

    const res = await request(app).delete('/constitutions/1');

    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual('Constitution was deleted!');
    expect(pool.query).toHaveBeenCalledWith('DELETE FROM constitutions WHERE id = $1', ["1"]);
  });

