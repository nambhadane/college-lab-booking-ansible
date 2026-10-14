# Automated Deployment of a College Lab Resource Booking API

**DevOps Project | Ansible | AWS EC2 | Python Flask**

## Project Overview

This project demonstrates automated deployment of a College Lab Resource Booking REST API using Ansible on an Ubuntu-based Amazon EC2 instance.

The application allows users to view laboratories, create bookings, retrieve booking records, and prevents overlapping reservations for the same laboratory and date.

## Objectives

- Automate server configuration using Ansible.
- Deploy a Flask REST API on AWS EC2.
- Manage application dependencies and services automatically.
- Verify deployment using health checks.
- Demonstrate lab booking and conflict validation.

## Technologies Used

- **Ansible** — Configuration management and deployment automation
- **AWS EC2** — Cloud hosting
- **Ubuntu on WSL** — Ansible control node
- **Python and Flask** — REST API development
- **SSH** — Secure remote access
- **systemd** — Application service management
- **curl** — API testing

## Project Structure

```text
lab-booking-ansible/
├── inventory.ini
├── site.yml
├── README.md
└── files/
    ├── app.py
    └── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Application health check |
| GET | `/labs` | List laboratories |
| POST | `/bookings