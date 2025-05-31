# users_manager

`users_manager` is a microservice responsible for managing user accounts, authentication metadata, and organizational roles in the **BarberShop API** platform. It integrates with Auth0 to handle identity and access management operations such as user creation, organization assignment, and token validation support.

This service is part of a distributed microservices system and communicates exclusively through the [`gateway_barbershop`](https://github.com/Kar977/gateway_barbershop).

## Features

- Integration with Auth0 for user and organization management  
- Assigning roles and metadata to employees and customers  
- Managing tenant domains and user permissions  
- Uses isolated PostgreSQL database  
- Protected by JWT authentication (validated by the API Gateway)

## Technologies

- Python 3.11  
- FastAPI 0.111.0
- PostgreSQL 15  
- Docker Docker 24.0.7
- Pydantic 2.7  
- Httpx 0.27  
- Pytest  8.3.5 / Pytest-asyncio 0.26.0  
- Pika (RabbitMQ client)  
- Uvicorn 0.30.1

## Environment Variables / Secrets

The following secrets must be configured (via GitHub Secrets or a `.env` file):

- `POSTGRES_NAME`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `TENANT_DOMAIN`, `DATABASE_ID_CONNECTION`, `MANAGEMENT_API_TOKEN`,
- `CLIENT_ID`, `ORGANIZATION_IDENTIFIER`
- `MAIL_GUN_API_KEY`

## ⚙️ Local Development
1. **Clone the repository**
   ```
   git clone https://github.com/Kar977/users_manager.git
   cd users_manager
   ```
2. **Build and run using Docker**
   ```
   docker build -t users_manager .
   docker run --env-file .env -p 8002:8002 users_manager

   ```
   The service will be available at:
   `http://localhost:8002`

>In production, the service is accessible only through the API Gateway.
### Running Tests
Run all tests using
```
python -m pytest
```

### Deployment
This microservice is containerized and deployed via AWS ECR and Portainer on EC2.

### CI/CD Workflow (GitHub Actions)
1. Lint & Test
Validates code and runs unit/integration tests.

2. Smoke Test
Builds and runs the container to verify basic functionality.

3. Build & Push
Pushes Docker image to AWS ECR.

Final deployment on EC2 is handled manually through Portainer.
