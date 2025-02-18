﻿# PasswordManager
 
This project is a simple password manager that securely stores and retrieves usernames and passwords for websites. It uses a Flask backend API to handle the storage and encryption of credentials, and a Chrome extension to interface with the backend. The passwords are encrypted using the cryptography.fernet library for security.

## Features
- **Login**: Secure user authentication via JWT (JSON Web Token).
- **Save Credentials**: Save website credentials securely in an SQLite database with encryption.
- **Retrieve Credentials**: Retrieve stored usernames and passwords for websites.
- **Remove Credentials**: Delete credentials from the database.
- **Cross-origin Resource Sharing (CORS)**: Enabled for flexibility in usage across different origins.

## Tech Stack
- **Frontend**: Chrome Extension (HTML, JavaScript, jQuery)
- **Backend**: Flask (Python), SQLite, cryptography (Fernet encryption), JWT for authentication
- **Database**: SQLite
