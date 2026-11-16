# 🍕 Domino's Pizza Clone – Console-Based Application

## Project Overview

The Domino's Pizza Clone is a console-based food ordering application developed using Python and SQLite.

The application allows customers to register, log in, explore the available food menu, add food items to their cart, view their cart, and generate their order bill.

The project follows a modular programming approach by separating database operations, models, and business logic into different modules.

## Technologies Used

- **Programming Language:** Python
- **Database:** SQLite
- **Database Connectivity:** Python sqlite3
- **Programming Concepts:** Object-Oriented Programming (OOP), Modular Programming
- **Version Control:** Git and GitHub

## Features

### Customer Management
- Customer Registration
- Customer Login
- Customer-specific order sessions
- Logout functionality

### Food Menu
- Display available food items
- View item names, prices, and descriptions
- Menu items include pizza, garlic sticks, beverages, and desserts

### Order Management
- Create a new order
- Add food items to cart
- Select item quantities
- View cart details

### Billing
- Calculate individual item prices
- Calculate the total order amount
- Display the final bill

## Project Structure

```text
Dominos_Clone_Console/
│
├── database/
│   └── db_manager.py
│
├── models/
│   ├── customers.py
│   ├── menu.py
│   └── order.py
│
├── services/
│   ├── authorization.py
│   ├── bill_ser.py
│   ├── login.py
│   ├── menu_ser.py
│   ├── order_ser.py
│   └── register.py
│
├── utility/
│   └── helper.py
│
├── app.py
├── Dominos.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/insanedingo23/Dominos-Clone-Console.git
```

### 2. Navigate to the Project Directory

```bash
cd Dominos-Clone-Console
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Run the Application

```bash
python app.py
```

The application uses Python's built-in SQLite3 module. No external Python packages are currently required.

## Database Details

The project uses SQLite for storing customer and menu information.

The database manager automatically creates the following tables:

**1. Customers Table**
- customer_id
- name
- email
- password

**2. Menu Items Table**
- item_id
- name
- price
- description

The SQLite database file is created locally when the application runs.

## Application Workflow

1. Start the application.
2. Register as a new customer.
3. Log in using your registered credentials.
4. Explore the food menu.
5. Select food items and quantities.
6. Add items to your cart.
7. View your cart.
8. Generate and view the final bill.
9. Log out.

## Future Enhancements

- Password hashing and improved authentication security
- Order history management
- Remove items from cart
- Update cart quantities
- Payment gateway integration
- Improved console interface
- Admin panel for menu management

## Project Status

Currently under development.

## Author

**Developed as a Python and SQLite learning project.**