# Event Management REST API

This is a simple Django REST API for managing events and event registrations.

It allows users to:
- Register and log in
- Create, update, and delete events
- Search events by title
- Register for events
- Receive email notification after registration

---

## Tech Used

- Django + Django REST Framework
- PostgreSQL (Docker)
- Token Authentication
- Swagger (drf-yasg)
- Resend SMTP (test mode)
- Docker + docker-compose

## Features

### Authentication
- User registration
- User login with token

### Event Management
- Create events
- List events
- Retrieve event details
- Update events (only by creator)
- Delete events (only by creator)

### Search
- Search events by title:
http://127.0.0.1:8000/swagger/


### Event Registration
- Register for an event
- View own registrations
- Cancel registration

### Email Notification
- Sends event registration confirmation email
- Uses Resend SMTP in test mode (no domain required)

## API Documentation

http://127.0.0.1:8000/swagger/

---

## How to Run

1. Clone the project:
```bash
git clone 
cd django_rest_event
```

2. Create .env file:
```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=
ALLOWED_TEST_EMAIL=
```

3. Start project:
```bash
docker-compose up --build
```