# Lazada Test Automation Framework

## Overview

This is a comprehensive test automation framework for testing the Lazada E-Commerce platform using Selenium WebDriver and Pytest.

## Project Structure

```
test-lazada/
├── src/
│   ├── reports/              # Test reports and screenshots
│   ├── test_data/            # Test data files
│   ├── tests/                # Test modules
│   │   ├── auth/            # Authentication tests
│   │   ├── cart/            # Cart management tests
│   │   ├── search/          # Search functionality tests
│   │   ├── review/          # Review and rating tests
│   │   └── security/        # Security tests
│   └── utils/               # Utility modules
│       ├── base_test.py     # Base test class
│       └── helpers.py       # Helper functions
├── config.py                # Configuration settings
├── run.py                   # Test runner
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
├── .env                     # Environment variables (not in git)
└── .gitignore              # Git ignore file
```

## Setup Instructions

### 1. Install Python

Ensure Python 3.8+ is installed on your system.

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Setup

```bash
python setup.py
```

### 6. Configure Environment Variables

Edit `.env` file with your test credentials:

```
TEST_EMAIL=your_email@example.com
TEST_PASSWORD=YourPassword123!
HEADLESS=False
BROWSER=chrome
```

## Running Tests

### Interactive Menu

```bash
python run.py
```

### Command Line

```bash
# Run all tests
python run.py all

# Run specific module
python run.py auth
python run.py cart
python run.py search
python run.py review
python run.py security

# Run specific test file
python run.py src/tests/auth/test_user_login.py
```

## Test Modules

### 1. Authentication Module (auth/)

- User Login (5 test cases)
- User Registration (5 test cases)

### 2. Cart Management Module (cart/)

- Add to Cart (5 test cases)
- Update Cart Items (5 test cases)

### 3. Search Module (search/)

- Product Search (5 test cases)
- Filter and Sort (5 test cases)

### 4. Review Module (review/)

- Submit Review (5 test cases)
- Filter Reviews (5 test cases)

### 5. Security Module (security/)

- SQL Injection Prevention (5 test cases)
- DoS Attack Prevention (5 test cases)

## Test Reports

Test reports are generated in `src/reports/` directory:

- HTML reports: `test_report.html`, `{module}_report.html`
- Screenshots: `{test_name}.png`

## Technologies Used

- **Python 3.8+**
- **Selenium WebDriver** - Browser automation
- **Pytest** - Testing framework
- **pytest-html** - HTML report generation
- **WebDriver Manager** - Automatic driver management
- **python-dotenv** - Environment variable management

## Contributing

This project follows ISO/IEC/IEEE 29119-3 standards for software testing.

## Team Members

- Kok Xiang Yue (24WMR06949) - Project Manager
- Ho Shuang Quan (24WMR01947) - Test Lead
- Chillien Chung (24WMR03401) - Manual Tester
- Daniel Chong Chan Yip - Manual Tester
- Harry Liow Siang Yi (24WMR03396) - Performance & Security Tester

## License

Educational Project - BMSE2003 Software Testing

```

```
