# Constitution Service

This service manages the constitutions that govern the behavior of AI agents in the Spec-Driven Development Platform.

## API

The service exposes a REST API for managing constitutions. The API is defined in `src/app.ts`.

### Endpoints

* `POST /constitutions`: Create a new constitution.
* `GET /constitutions`: Get all constitutions.
* `GET /constitutions/:id`: Get a constitution by ID.
* `PUT /constitutions/:id`: Update a constitution.
* `DELETE /constitutions/:id`: Delete a constitution.

## Running the Service

To run the service, first install the dependencies:

```bash
npm install
```

Then, build and start the service:

```bash
npm run build
npm start
```

## Testing

To run the tests, use the following command:

```bash
npm test
```

