# Take Home - Emotive Exam

## Getting Started
I have used the skeleton provided to create this, so basically having docker and
docker compose installed and running `docker compose up` sets everything up.

### Dependencies:
* Docker - See [Get Docker](https://docs.docker.com/get-docker/)
* Docker Compose - Installed with Docker Desktop, See [Install Docker Compose](https://docs.docker.com/compose/install/)

### Running:
With the dependencies installed, running the project is as simple as running:
```bash
docker compose up
```

This will pull the required Docker images and spin up a container running your service on http://localhost:8000.

To end the service, press `Ctrl+C`

### The project:
The main goal of this project is to provide a two-factor authentication service using the Twilio API.

In the root directory there is a file called thunder-collection-emotive-exam.json wich contains the API calls for testing.
As i'm using the free tier of the API only my phone number will work.

### Endpoints:
There are two endpoints:
    - `api/api/two-factor-auth/send-verification-token/` it receives a post method with the phone_number in the body.
    - `api/api/two-factor-auth/check-verification-token/` it receives a post method with the phone_number and the code in the body.



