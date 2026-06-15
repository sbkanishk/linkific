# Week 1 API Testing & Debugging Suite — Day 10

## 🚀 Interactive API Documentation
👉 **[View Live Postman Documentation Portal](https://documenter.getpostman.com/view/55692291/2sBXwtooTv)**

---

## 📋 Overview
This repository contains the complete backend testing suite and architectural setup for the Week 1 APIs. The system features modular resource structures, robust error handling with FastAPI validation, and fully automated authentication test chaining via Postman.

## 📂 Project Structure
* **`Auth/` Folder:** Handles secure registration (`/auth/register`) and login (`/auth/login`) operations.
* **`Products/` Folder:** Contains protected endpoints (`/items/`) requiring valid session credentials.

## 🔐 Automated Testing Approach
1. **Dynamic Environment Masking:** All routes utilize the `{{base_url}}` variable to seamlessly switch execution profiles.
2. **Automated Token Chaining:** A Post-response JavaScript snippet extracts the bearer `access_token` upon successful user login and automatically maps it to the active environment's `{{token}}` table.
3. **Protected Endpoint Validation:** Subsequent requests automatically inject the stored runtime token inside the Bearer Auth header stack.

## 🛠️ Debugging & Performance Implementation
* **FastAPI Logging:** Structured tracking via Python's built-in `logging` module maps runtime application traffic (`INFO`, `ERROR`) out to the terminal layout.
* **Breakpoint Inspection:** The codebase is fully configured for VS Code debugger integration, enabling engineers to pause execution and inspect local memory states during live requests.