# SVGTeamFinder
SVGTeamFinder is a Python backend application aimed at simplifying the retrieval of high-quality SVG emblems for football teams. The project emphasizes the implementation of CLEAN CODE and SOLID principles within the backend context for consuming football API data.


# Objectives of Study:
The primary goals of this project are to exercise CLEAN CODE and SOLID methodologies in a backend environment while interfacing with football APIs. By adhering to these principles, the project seeks to enhance code quality, readability, and maintainability.


# Getting Started:
**To run the project:**

Clone this repository.

Install Flask by running pip install flask.

Create an account at API-Futebol and obtain an API key.

Replace my key in 'API_KEY' with your API key in app.py.

Execute python app.py in your terminal to start the application.


# Technologies Used:
**Python:** Backend logic and API consumption.

**Flask:** Web framework for building the backend API.

**Requests:** HTTP library for making requests to external APIs.


# SOLID in our code

In this project, we applied the SOLID principles to improve the quality, readability, and maintainability of the code. Here is how each principle was applied:

## Single Responsibility Principle (SRP)

We created the `API` class to handle API requests and the `TeamDataAPI` class to handle the retrieval of specific team data. In this way, each class has only one responsibility.

## Open-Closed Principle (OCP)

If we want to add more methods to fetch data from the API, we can extend the `API` class and add the methods in the new class, without modifying the `API` class. This keeps the `API` class closed for modification but open for extension.

## Liskov Substitution Principle (LSP)

The `TeamDataAPI` class is a derived class from `API` and can replace `API` without changing the behavior of the program. This ensures that derived classes can replace their base classes.

## Interface Segregation Principle (ISP)

All functions in our code are necessary, so this principle is already being followed. No client is forced to depend on interfaces they do not use.

## Dependency Inversion Principle (DIP)

The Flask routes in our code depend on the abstract `API` class, not the concrete functions to fetch data. This ensures that we depend on abstractions, not concretions.


# License:
This project is licensed under the **MIT** License. See LICENSE for more details.