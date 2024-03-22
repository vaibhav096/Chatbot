# Django Chatbot

This project is a chatbot application built with Django and utilizes a generative AI model for providing responses.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

Chatbot Project is a web application designed to provide conversational interaction with users. It utilizes advanced AI techniques to generate responses based on user input.

## Features

- Conversational chat interface
- Utilizes generative AI model for response generation
- User authentication system
- Chat history tracking

## Installation

To run the Chatbot Project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/Chatbot.git```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Set up environment variables:

- Create a .env file in the project root directory and add your Google API key:

```bash
GOOGLE_API_KEY=your_google_api_key
```

1. Run migrations:

```bash
python manage.py migrate
```
1. Run the development server:

```bash
python manage.py runserver
```
1. Access the application at http://localhost:8000 in your web browser.

## Usage
Once the application is running, users can interact with the chatbot by typing messages in the input field and pressing Enter. The chatbot will generate responses based on the input provided by the user.

