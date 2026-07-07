# E-Commerce Test Automation

A UI test automation framework for **SauceDemo** built with **Python, Selenium, and Pytest**. The framework follows the **Page Object Model (POM)** design pattern to provide a clean, maintainable, and scalable structure for end-to-end web testing.

## Project Overview

This project automates the core shopping workflow of an e-commerce application, covering important user journeys from login to order completion.

It demonstrates modern test automation practices, including reusable page objects, Pytest fixtures, custom test markers, HTML reporting, and automatic screenshot capture for failed tests.

## Features

- Page Object Model (POM) architecture
- End-to-end UI automation with Selenium WebDriver
- Test execution with Pytest
- Custom Pytest markers for better test organization
- HTML test reports using pytest-html
- Automatic screenshots on test failures
- Environment configuration using python-dotenv
- Maintainable and scalable test structure

## Test Coverage

The automation suite currently covers:

- ✅ Login functionality
- ✅ Product details validation
- ✅ Shopping cart operations
- ✅ Checkout workflow

## Tech Stack

- **Python 3.8+**
- **Selenium WebDriver**
- **Pytest**
- **pytest-html**
- **webdriver-manager**
- **python-dotenv**
- **Faker**

## Project Structure

```text
ecommerce-test-automation/
│
├── pages/              # Page Object classes
├── tests/              # Test cases and pytest fixtures
├── utils/              # Configuration and helper utilities
├── reports/            # Generated HTML test reports
├── screenshots/        # Screenshots captured from failed tests
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variables template
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd ecommerce-test-automation
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file:

```bash
cp .env.example .env
```

Update the values according to your environment.

## Running Tests

Run the complete test suite:

```bash
pytest -v
```

Run tests by category:

```bash
pytest -m login -v
```

```bash
pytest -m product -v
```

```bash
pytest -m cart -v
```

```bash
pytest -m checkout -v
```

Run smoke tests:

```bash
pytest -m smoke -v
```

## Generate HTML Report

Generate a detailed HTML test report:

```bash
pytest --html=reports/report.html --self-contained-html
```

The report will be available inside the `reports/` directory.

## Configuration

The project uses `pytest.ini` for:

- Test discovery configuration
- Custom test markers
- Logging settings
- Default pytest execution options

## Future Improvements

- Add CI/CD pipeline using GitHub Actions
- Add cross-browser testing support
- Enable parallel test execution with pytest-xdist
- Add Docker support
- Improve test data management

## License

This project is created for learning and portfolio purposes.
