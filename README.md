### Objective

Your assignment is to implement a bookstore REST API using Python and Django.

### Brief

Lohgarra, a Wookie from Kashyyyk, has a great idea. She wants to build a marketplace that allows her and her friends to
self-publish their adventures and sell them online to other Wookies. The profits would then be collected and donated to purchase
medical supplies for an impoverished Ewok settlement.

### Tasks

- Implement assignment using:
  - Language: **Python**
  - Framework: **Django**
- Implement a REST API returning JSON or XML based on the `Content-Type` header
- Implement a custom user model with a "author pseudonym" field
- Implement a book model. Each book should have a title, description, author (your custom user model), cover image and price
  - Choose the data type for each field that makes the most sense
- Provide an endpoint to authenticate with the API using username, password and return a JWT
- Implement REST endpoints for the `/books` resource
  - No authentication required
  - Allows only GET (List/Detail) operations
  - Make the List resource searchable with query parameters
- Provide REST resources for the authenticated user
  - Implement the typical CRUD operations for this resource
  - Implement an endpoint to unpublish a book (DELETE)
- Implement API tests for all endpoints

### Evaluation Criteria

- **Python** best practices
- If you are using a framework make sure best practices are followed for models, configuration and tests
- Write API tests for all implemented endpoints
- Make sure that users may only unpublish their own books
- Bonus: Make sure the user _Darth Vader_ is unable to publish his work on Wookie Books

### CodeSubmit

Please organize, design, test and document your code as if it were
going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The InvisAlert Team

# Project Name

Bookstore App

## Getting Started

To get started with contributing or running the project locally, follow the steps below.

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.11
- Micromamba package manager
- Visual Studio Code (VSCode)

### Setting Up Development Environment

1. **Cloning the Repository**:

   Clone this repository to your local machine using Git:

   ```
   git clone http://invisalert-bcjetl@git.codesubmit.io/invisalert/wookie-books-nfscgv
   ```

2. **Creating a Virtual Environment**:

   We use Micromamba for managing virtual environments. If you don't have Micromamba installed, you can install it following the instructions [here](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).

   ```
   micromamba create -n invis_task_py3.11 python=3.11
   ```

3. **Activating the Virtual Environment**:

   Activate your virtual environment using Micromamba:

   ```
   micromamba activate invis_task_py3.11
   ```

4. **Installing Dependencies**:

   Install project dependencies within the activated virtual environment:

   ```bash
   micromamba install -n invis_task_py3.11 -c conda-forge --file requirements.txt
   ```

   Additionally, install npm dependencies specified in package.json:

   ```bash
   npm install
   ```

   For development purposes, you may also need to install additional
   dependencies. Install these using:

   ```bash
   micromamba install -n invis_task_py3.11 -c conda-forge --file dev-requirements.txt
   ```

   This will install development dependencies such as pre-commit required for linting and formatting checks.

### Development Guidelines

- **Editor**: We recommend using Visual Studio Code (VSCode) for development. If you haven't already, download and install VSCode from [here](https://code.visualstudio.com/).

- **Code Formatting and Linting**:
  - We enforce code formatting and linting using predefined settings. Ensure that you have the following extensions installed in your code editor:
    - ms-python.python
    - ms-python.vscode-pylance
    - ms-python.debugpy
    - ms-python.black-formatter
    - ms-python.flake8
    - ms-python.isort
    - joshbolduc.commitlint
  - Configure your VSCode to use these extensions for Python files.
  - Our `settings.json` and `.pre-commit-config.yaml` files define the formatting and linting rules. Ensure that your changes adhere to these rules before committing.

### Commit Message Guidelines and Hook Setup

We follow the conventional commit message format with additional rules enforced by `commitlint`. Our commit messages must adhere to the following guidelines:

- **Header**: Limited to 50 characters.
- **Body**: Limited to 72 characters per line.
- **Blank Line**: Ensure that there is a blank line after the header.

For more information on the conventional commit message format, refer to the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).

To enforce these rules, ensure the following configurations are present in your project:

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'header-max-length': [2, 'always', 50],
    'body-max-line-length': [2, 'always', 72],
    'body-empty': [2, 'always'], // Ensure that there is a blank line after the header
  },
};
```

#### Setting Up the Commit Message Hook

To ensure commit messages meet our standards, we use `commitlint` with a pre-commit hook. Follow these steps to set up the `commit-msg` hook in your local development environment:

1. **Install Pre-commit**:
   If not already installed, use pip to install `pre-commit`:

   ```bash
   pip install pre-commit
   ```

2. **Configure Pre-commit Hooks**:
   Verify that the `.pre-commit-config.yaml` file in your project's root directory includes the necessary configuration for `commitlint`.

3. **Install the `commit-msg` Hook**:
   Run the following command in the project's root directory to install the `commit-msg` hook:

   ```bash
   pre-commit install --hook-type commit-msg
   ```

This setup automatically checks your commit messages against the defined rules each time you commit. To test the hook, try making a commit with a non-compliant message; the hook should prevent the commit and display an error.
