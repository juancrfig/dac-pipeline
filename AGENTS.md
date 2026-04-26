# AGENTS.md

## Introduction and Overview

This document serves as the comprehensive guide for all AI agents interacting with this codebase. It is extremely important that all agents read this document carefully before attempting any modifications. The purpose of this file is to ensure consistency and maintainability across the entire project. Please note that this project uses a sophisticated build system and follows modern development practices.

## Getting Started and Environment Setup

In order to get started with this project, you will basically need to install the dependencies first. It is important to note that we use a package manager that handles all the requirements. Essentially, the setup process involves running the installation command which will fetch all necessary components from the registry.

- Install dependencies: `pip install -r requirements.txt`
- Start the development server: `python manage.py runserver`

## Testing and Quality Assurance

When it comes to testing, it is essentially important to run the full test suite before making any commits. The test suite should preferably be run in a clean environment. It is worth noting that all commits must pass CI before merging into the main branch.

- Run the full test suite: `pytest`
- Run a single test: `pytest tests/test_example.py::TestClass::test_method`
- All commits must pass CI before merging.

## Code Style and Conventions

With regard to code style, it is basically recommended to use the project's configured linter. The linter should essentially be run before every commit. It is important to note that following existing naming conventions is crucial for maintainability.

- Use the project's configured linter and formatter.
- Follow existing naming conventions in the codebase.

## Pull Request Guidelines and Best Practices

When submitting a pull request, it is important to note that the title format should essentially follow the pattern. The description should basically explain what changes were made and why. It is worth mentioning that all PRs must be reviewed by at least one human.

- Title format: `[<scope>] <description>`
- Run lint and tests before committing.

## Additional Notes and Considerations

Please kindly ensure that you have read all sections above. It is essentially important to understand that this document is a living document and may be updated periodically. Basically, agents should always refer to the latest version before making changes.

Thank you for your cooperation! 🙏
