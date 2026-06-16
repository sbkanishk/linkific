# 🎓 FastAPI & MongoDB Student Management System

An asynchronous REST API built with FastAPI and MongoDB using the Motor driver. This project covers core NoSQL concepts including dynamic schemas, embedded/referenced document patterns, and database indexing.

---

## 🚀 Quick Setup Instructions

### 1. Prerequisites
Ensure you have the following installed on your machine:
* Python 3.10+
* Visual Studio Code
* Docker Desktop (with WSL2 enabled)

### 2. Run the Database Instance
Launch the background MongoDB container via Docker:
```bash
docker run -d --name local-mongo -p 27017:27017 mongo:latest