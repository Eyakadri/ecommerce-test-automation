# E-Commerce Test Automation

A clean and professional UI test automation project for SauceDemo built with Selenium, pytest, and the Page Object Model (POM). The suite validates the core shopping journey, including login, product viewing, cart actions, and checkout.

## Project Overview

This project is designed to demonstrate reliable browser automation for an e-commerce website using modern Python testing practices. It focuses on practical end-to-end scenarios and keeps the test structure maintainable and easy to extend.

## Covered Test Areas

The current suite includes automated tests for:

- Login
- Product details
- Cart operations
- Checkout flow

## Tech Stack

- Python 3.8+
- Selenium
- pytest
- pytest-html
- webdriver-manager
- python-dotenv
- Faker

## Project Structure

- pages/: page object classes for the application pages
- tests/: test cases and pytest fixtures
- utils/: configuration and screenshot utilities
- reports/: generated HTML test reports
- screenshots/: screenshots captured for failed tests

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create the environment file:

```bash
cp .env.example .env
```

## Running Tests

Run the full test suite:

```bash
pytest -v
```

Run a specific suite:

```bash
pytest -m login -v
pytest -m product -v
pytest -m cart -v
pytest -m checkout -v
```

Generate an HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```

## Notes

- Screenshots for failed tests are stored in the screenshots folder.
- HTML reports are generated in the reports folder.
- The project is suitable for local execution and CI usage.
