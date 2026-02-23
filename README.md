# Sales By Twilight API

A RESTful e-commerce API built with Python and Flask for the Coding Black Females Academy assessment.

## Description

Sales By Twilight is an e-commerce backend API that manages categories, products, customers, and orders.

## Features

- Category management
- Product management
- Customer management
- Order management
- MySQL database integration

## Technologies Used

- Python 3.x
- Flask
- MySQL
- pytest (for testing)

## Installation

1. Clone the repository:
```
   git clone https://github.com/nkemjp2/sales-by-twilight.git
   cd sales-by-twilight
```

2. Create and activate virtual environment:
```
   python -m venv sales-by-twilight
   source sales-by-twilight/bin/activate
```

3. Install dependencies:
```
   pip install -r requirements.txt
```

4. Set up the database:
```
   mysql -u root < db/schema.sql
```

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update database credentials

## API Endpoints

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /categories | Get all categories |
| GET | /categories/<id> | Get a single category |

*More endpoints will be documented as they are implemented.*

## Running the Application
```
python run.py
```

## Running Tests
```
pytest tests/ -v
```

## Project Structure
```
sales-by-twilight/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base_model.py
│   └── routes/
├── db/
│   └── schema.sql
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Author

Nkem

## License

This project is for educational purposes as part of the Coding Black Females Academy.