# Code Quality and Pre-commit Hooks

This project uses automated code quality tools that run before each commit to ensure consistent code style and prevent broken code from being committed.

## Tools Used

- **Black**: Code formatter that ensures consistent Python code style
- **isort**: Import sorter that organizes imports in a standardized way
- **flake8**: Linter that checks for code style issues and potential bugs
- **pre-commit**: Framework that runs all tools automatically before commits

## Installation

The development dependencies are already included in `requirements-dev.txt`. To set up the pre-commit hooks:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Manual Usage

You can run the tools manually:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code with flake8
flake8

# Run all pre-commit hooks
pre-commit run --all-files
```

## How It Works

When you try to commit code, the pre-commit hooks will automatically:

1. **Format your code** with Black and isort
2. **Check for linting issues** with flake8
3. **Fix common issues** like trailing whitespace and missing newlines
4. **Run tests** to ensure your changes don't break existing functionality

If any tool finds issues or makes changes, the commit will be blocked and you'll need to review and commit the changes again.

## Configuration

- **Black & isort**: Configured in `pyproject.toml`
- **flake8**: Configured in `.flake8`
- **pre-commit**: Configured in `.pre-commit-config.yaml`
