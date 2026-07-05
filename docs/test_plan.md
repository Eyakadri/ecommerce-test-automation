# Test Plan

## Objective

This project validates the main user journeys of the SauceDemo application through automated UI tests.

## Scope

The current automation scope includes:
- Login flow
- Product detail flow
- Cart operations
- Checkout flow

## Approach

Tests are implemented with Selenium and pytest using the Page Object Model to keep the suite maintainable and readable.

## Execution Notes

- Tests are run locally with pytest.
- Failure screenshots are stored in the screenshots folder.
- HTML reports are generated in the reports folder.
