# Secure Password Manager

## Overview

Secure Password Manager is a secure desktop application built using Python and CustomTkinter that allows users to generate, store, search, and manage passwords safely.

The application uses encryption to protect stored credentials and provides a modern graphical user interface for easy password management.

---

## Features

### Master Password Protection

* Secure login system
* Master password authentication
* Protected credential vault

### Encrypted Storage

* Credentials encrypted using Fernet encryption
* Secure local storage
* Password data protected from unauthorized access

### Password Generator

* Generate strong random passwords
* Includes:

  * Uppercase letters
  * Lowercase letters
  * Numbers
  * Special characters

### Password Strength Indicator

* Weak
* Medium
* Strong

### Copy Password

* One-click password copy to clipboard

### Search Credentials

* Search saved accounts instantly
* Retrieve stored usernames and passwords

### Modern User Interface

* Built using CustomTkinter
* Dark mode design
* User-friendly layout

---

## Technologies Used

* Python
* CustomTkinter
* Cryptography (Fernet Encryption)
* Pyperclip
* JSON Storage

---

## Project Structure

```text
Secure_Password_Manager
│
├── password_manager.py
├── requirements.txt
├── README.md
├── assets
├── screenshots
└── vault
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/manoharmax/OIBSIP.git
```

### Navigate to Project

```bash
cd Secure_Password_Manager
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python password_manager.py
```

---

## Screenshots

### Login Screen

(Add screenshot)

### Dashboard

(Add screenshot)

### Password Generator

(Add screenshot)

### Search Credentials

(Add screenshot)

---

## Security Note

This project stores credentials locally using encryption.

For educational and internship purposes, the application demonstrates secure password management concepts and encrypted credential storage.

---

## Author

**Manohar**

Oasis Infobyte Internship Project

---

## License

This project is developed for educational and internship purposes.
