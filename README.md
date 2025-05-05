# RESTful API Testing

This project contains postman and automation scripts for testing RESTful APIs on: 
```https://restful-booker.herokuapp.com/apidoc/index.html ```

## Folder Structure

```
Automation_Projects/
└── restfull-api-testing/
    ├── README.md       # Project documentation
    ├── tests/          # Test scripts
    ├── reports/        # Test reports
    ├── config/         # Configuration files
    └── utils/          # Utility scripts
```

## Prerequisites

- Python 3.x
- Postman
- `requests` library
- `pytest` framework
- `uv` Python package and project manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/restfull-api-testing.git
   ```
2. Navigate to the project directory:
   ```bash
   cd restfull-api-testing
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run all tests using `pytest`:
```bash
pytest tests/
```

## Reporting

Test reports will be generated in the `C:/reports/` folder.
