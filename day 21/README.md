# Day 21: High-Performance Asynchronous Python Sandbox 🚀

This project demonstrates the core patterns of Asynchronous Programming in Python using **FastAPI**, **SQLAlchemy (Async)**, **HTTPX**, and **WebSockets**.

## 📊 Core Concepts Implemented

* **Concurrency vs Parallelism:** Juggling tasks on a single thread vs running them on multiple cores.
* **Non-blocking Architecture:** Utilizing the Python Event Loop to switch contexts during I/O waits.
* **Thread Offloading:** Observing how FastAPI uses worker threads to prevent standard `def` routes from freezing the loop.

## 🛠️ Tech Stack & Async Drivers Used

* **Framework:** FastAPI (with Uvicorn ASGI server)
* **Database Driver:** `sqlite+aiosqlite` via SQLAlchemy Async Engine
* **HTTP Client:** `httpx.AsyncClient` (Concurrent API fetching)
* **File Operations:** `aiofiles` (Non-blocking logging)

## 🏃‍♂️ How to Run the Project

1. Activate the environment:
   ```bash
   .\async_env\Scripts\Activate.ps1
