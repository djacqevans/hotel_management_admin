# Hotel Management System

A FastAPI-based system for managing hotel rooms and customers, containerized with Docker.

## Features

- Manage rooms and customers
- PostgreSQL database integration
- Dockerized for easy deployment

## Quick Start

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd hotel_management
   ```

2. **Start the application:**

   ```bash
   docker compose up -d
   ```

   Access the app at `http://localhost:8050`

## API Endpoints

- `GET /`: Welcome message
- `GET /rooms`: List rooms
- `POST /rooms`: Create a room
- `GET /customers`: List customers
- `POST /customers`: Create a customer

## Development Setup

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   python run.py
   ```

## Project Structure

- `app/`: Application code
- `docker-compose.yml`: Docker configuration
- `Dockerfile`: Docker image setup

## Core Technologies

- **FastAPI**: A modern, fast Python web framework for building APIs
- **PostgreSQL**: The database system used to store hotel data
- **Docker**: Used for containerization and easy deployment

## Deployment Options

1. **Docker Deployment** (Recommended)
   ```bash
   docker compose up -d
   ```
   Access the app at `http://localhost:8050`

2. **Local Development**
   - Use Python virtual environment for isolation
   - Requires manual setup of dependencies
   - Run directly with Python (`python run.py`)
