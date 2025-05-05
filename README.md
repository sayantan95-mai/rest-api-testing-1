# RESTful API Testing

<img src=".md\uv_logo.png" alt="uv" style="width:100px;"/><img src=".md\pytest.png" alt="pytest" style="width:50px;"/><img src=".md\png-transparent-postman-hd-logo-thumbnail.png" alt="postman" style="width:50px;"/>


This project contains postman and automation scripts for testing RESTful APIs on: 
```https://restful-booker.herokuapp.com/apidoc/index.html ```.

Also used the new `uv` python package and project manager to improve dependence and virtual environment creaction.

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

1. Install uv `Powershell`:
   ```powershell
   python -V ; pip -V
   pip install uv
   ```
2. Clone the repository:
   ```powershell
   git clone https://github.com/your-repo/restfull-api-testing.git
   ```
2. Navigate to the project directory:
   ```powershell
   cd .\restfull-api-testing\
   ```
3. Install dependencies:
   ```powershell
   uv sync
   OR
   try: uv sync --all-groups
   ```

## Running Tests

Run all tests using `pytest`:
```powershell
pytest
OR
pytest tests/
```

## Reporting

Test reports will be generated in the `C:/reports/` folder.
