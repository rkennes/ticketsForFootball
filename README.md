# Tickets For Football API

This project is a **FastAPI**-based backend for managing ticket models, sectors, and service events.

## Documentation 
https://www.notion.so/ticketsForFootball-246911f3e17c80269026d39939f71a51

## Table of Contents

- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
  - [Event Service](#event-service)
  - [Sector](#sector)
  - [Ticket Model](#ticket-model)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

Make sure you have [Poetry](https://python-poetry.org/docs/) installed. Then clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/ticketsforfootball.git
cd ticketsforfootball
poetry install
```

---

## Running the Project

Create a `.env` file with the required environment variables and run the server:

```bash
poetry run uvicorn src.main:app --reload
```

The interactive API documentation will be available at:  
http://localhost:8000/docs

---

## API Endpoints

### Event Service

| Method | Route                                        | Description                          |
|--------|----------------------------------------------|--------------------------------------|
| GET    | `/event_service/{cnpj}`                      | List all service events by CNPJ      |
| POST   | `/event_service/`                            | Create a new service event           |
| PUT    | `/event_service/{cnpj}/{event_service_id}`   | Update an existing service event     |
| DELETE | `/event_service/{cnpj}/{event_service_id}`   | Delete a specific service event      |

---

### Sector

| Method | Route                                  | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| POST   | `/sector`                               | Create a new sector                    |
| GET    | `/sector/{cnpj}?limit=10&skip=0`        | List sectors for a given CNPJ          |
| PUT    | `/sector/{sector_id}`                   | Update a sector                        |
| DELETE | `/sector/{cnpj}/{sector_id}`            | Delete a specific sector               |

---

### Ticket Model

| Method | Route                                                              | Description                                       |
|--------|---------------------------------------------------------------------|---------------------------------------------------|
| POST   | `/ticket_model`                                                    | Create a new ticket model                         |
| GET    | `/ticket_model/{cnpj}?limit=10&skip=0`                             | List ticket models by CNPJ                        |
| PUT    | `/ticket_model/{cnpj}/{ticket_model_id}`                          | Update a ticket model                             |
| DELETE | `/ticket_model/{cnpj}/{ticket_model_id}`                          | Delete a ticket model                             |
| DELETE | `/ticket_model/{cnpj}/{ticket_model_id}/sector/{sector_id}`       | Remove a specific sector from a ticket model      |
| POST   | `/ticket_model/{cnpj}/{ticket_model_id}/sector`                   | Add sectors to a ticket model                     |

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).